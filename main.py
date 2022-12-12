import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

URL = "https://www.dyson.com.tr/dyson-v15-detect-absolute"
SELECTOR = "hero__pricing__sold-out"

while True:
    response = requests.get(URL)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, features='html.parser')
        element = soup.find(attrs={"class": SELECTOR})

        if not element:
            # Send thee push notification via Pushover
            url = "https://api.pushover.net/1/messages.json"
            token = os.getenv("PUSHOVER_TOKEN")
            user = os.getenv("PUSHOVER_USER")
            message = "In stock!"
            payload = f"token={token}&user={user}&message={message}"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            requests.request("POST", url, headers=headers, data=payload)

            # Stop
            break
