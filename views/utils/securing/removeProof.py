import requests
import codecs
import re

def removeProof(amrp: str, apicanary: str, amsc: str):
        
    proofs = requests.get(
        "https://account.live.com/proofs/manage/additional?mkt=en-US&refd=account.microsoft.com&refp=security",
        headers = {
            "host": "account.live.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-ms-apiVersion": "2",
            "x-ms-apiTransport": "xhr",
            "uiflvr": "1001",
            "scid": "100109",
            "hpgid": "201030",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Length": "383",
            "Origin": "https://account.live.com",
            "Connection": "keep-alive",
            "Referer": "https://account.live.com/proofs/Manage/additional",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
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

        requests.post(
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
