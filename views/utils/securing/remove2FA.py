import requests

def remove2FA(amrp: str, apicanary: str, amsc: str):

    remove = requests.post(
        "https://account.live.com/API/Proofs/DisableTfa",
        headers = {
            "Cookie": f"AMRPSSecAuth={amrp}; amsc={amsc}",
            "canary": apicanary
        },
        json = {
            "uiflvr": 1001,
            "uaid": "abd2ca2a346c43c198c9ca7e4255f3bc",
            "scid": 100109,
            "hpgid": 201030
        },
        allow_redirects = False
    )

    if "apiCanary" in remove.json() and remove.status_code == 200:
        print("[+] - Disabled 2FA")
    else:
        print("[X] - Failed to disable 2FA")
