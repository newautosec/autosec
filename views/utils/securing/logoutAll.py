import requests

def logoutAll(amrp: str, apicanary: str, amsc: str):

    remove = requests.post(
        "https://account.live.com/API/Proofs/DeleteDevices",
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
        print("[+] - Sucessfully Logout all devices")
    else:
        # print(f"\nStatus Code: {remove.status_code}\nResponse: {remove.text}")
        print("[X] - Failed to logout of all devices")
        print(f"Zyger: {remove.text}")
