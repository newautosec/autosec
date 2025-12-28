import requests

def getGamertag(xbl: str) -> str:

    gamertag = requests.post(
        url = "https://xsts.auth.xboxlive.com/xsts/authorize",
        headers = {
            "content-type": "application/json",
            "Accept": "*/*"
        },
        json = {
            "Properties" : {
                "SandboxId" : "RETAIL",
                "UserTokens" : [
                    xbl
                ]
            },
            "RelyingParty": "http://xboxlive.com",
            "TokenType": "JWT"
        }
    )

    print(gamertag.text)