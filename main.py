from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
from github import GithubAPI
from config import settings


WAIT_SECONDS = 60 * 1  # every minute
MAX_RUN_TIME = 60 * 60 * 5  # 5 hours
START_TIME = time.time()


def check():
    url = "https://www.dyson.com.tr/dyson-v15-detect-absolute"
    selector = "hero__pricing__sold-out"
    response = requests.get(url)
    found = False

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, features='html.parser')
        element = soup.find(attrs={"class": selector})
        print(f'Checking ... {datetime.now()}')

        if not element:
            # Sending the push notification to my phone via Pushover
            url = "https://api.pushover.net/1/messages.json"
            message = "Dyson in stock! Hurry up, buy it!"
            payload = f"token={settings.PUSHOVER_TOKEN}&user={settings.PUSHOVER_USER}&message={message}"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            requests.request("POST", url, headers=headers, data=payload)
            found = True

    return found


def stop_worker() -> bool:
    return (time.time() - START_TIME) > MAX_RUN_TIME


if __name__ == '__main__':
    while True:
        found = False

        try:
            found = check()
        except Exception as ex:
            print(ex)

        if found:
            break

        time.sleep(WAIT_SECONDS)

        if stop_worker():
            GithubAPI().workflow_dispatch()
            break
