import requests
import time
import re

def getEmailCode(email: str, key: str) -> str:
    
    email_id = email.split("@")[0]

    emails = requests.get(
       url = f"https://donarev419.com/api/emails/all",
       headers = {
           "Authorization": key
       }
    ).json()

    for email in emails["content"]:
        if email["local"] == email_id:

            while True:

                emailData = requests.get(
                    url = f"https://donarev419.com/api/emails/inbox/{email["id"]}",
                    headers = {
                        "Authorization": key
                    }
                ).json()

                if emailData["content"]:

                    finalData = requests.get(
                        url = f"https://donarev419.com/api/emails/{emailData["content"][0]["id"]}",
                        headers = {
                            "Authorization": key
                        }
                    ).json()

                    code = re.search(r"Security code:\s*<\/?[^>]*>\s*(\d{6})", finalData["content"]["html"]).group(1)

                    return code

                else:
                    # Prevent Ratelimiting
                    time.sleep(0.8)
                    continue
