import requests

def getRecoveryCode(amrp: str, apicanary: str, amsc: str, eni: str):

    data = requests.post(
        url = "https://account.live.com/API/Proofs/GenerateRecoveryCode",
        headers = {
            "canary": apicanary,
            "cookie": f"amsc={amsc}; AMRPSSecAuth={amrp};"
        },
        json = {
            "encryptedNetId": eni,
        }
    )

    return data.json()["recoveryCode"]