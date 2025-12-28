import requests

def getAMRP(T, amsc):

    fetchAMRP = requests.post(
        url = "https://account.live.com/proofs/Add?apt=2&wa=wsignin1.0",
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Cookie": f"amsc={amsc}; MSPAuth=Disabled; MSPProof=Disabled;"
        },
        data = {
            "t": T
        },
        allow_redirects = False
    )

    if "AMRPSSecAuth" in fetchAMRP.cookies:
        return fetchAMRP.cookies["AMRPSSecAuth"]
    else:
        return None