import requests
import codecs
import re

def getProof(amrp: str, apicanary: str, amsc: str) -> list:
        
    proofs = requests.get(
        "https://account.live.com/proofs/manage/additional?mkt=en-US&refd=account.microsoft.com&refp=security",
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Cookie": f"AMRPSSecAuth={amrp}; amsc={amsc}",
            "Referer": "https://login.live.com/"
        },
        allow_redirects = False
    )
    
    proofIds = re.findall(r'"proofId":"([^"]+)"', proofs.text)
    decodedProofs = [codecs.decode(ID, "unicode_escape") for ID in proofIds]
    
    for proof in decodedProofs:

        rproof = requests.post(
            url = "https://account.live.com/API/Proofs/DeleteProof",
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": f"AMRPSSecAuth={amrp}; amsc={amsc}",
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json",
                "canary": apicanary
            },
            json = {
                "proofId": proof,
                "uaid": "114b68368b7b46afa44c82a8246e4a44",
                "uiflvr": 1001,
                "scid": 100109,
                "hpgid": 201030
            }
        )

        print(rproof.text)

    return decodedProofs
