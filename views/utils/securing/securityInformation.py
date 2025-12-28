import requests
import re

def securityInformation(amrp: str):

    data = requests.get(
        url = "https://account.live.com/proofs/Manage/additional",
        headers = {
            "Cookie": f"AMRPSSecAuth={amrp}"
        }
    )

    match = re.search(r'var\s+t0\s*=\s*(\{.*?\});', data.text, re.DOTALL)
    return match.group(1)
