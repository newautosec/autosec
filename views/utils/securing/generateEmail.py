import requests

def generateEmail(email: str, domain: str, key: str) -> str:

    requests.post(
        url = "https://donarev419.com/api/emails/address",
        headers = {
            "Authorization": key
        },
        json = {
            "domain": domain,
            "local": email
        }
    )


    