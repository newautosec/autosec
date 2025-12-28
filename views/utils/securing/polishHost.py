import requests

def polishHost(host: str, amsc: str) -> str:

    data = requests.get(
        url = "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=21&ct=1708978285&rver=7.5.2156.0&wp=SA_20MIN&wreply=https://account.live.com/proofs/Add?apt=2&uaid=0637740e739c48f6bf118445d579a786&lc=1033&id=38936&mkt=en-US&uaid=0637740e739c48f6bf118445d579a786",
        headers = {
            "cookie": f"__Host-MSAAUTH={host}; amsc=${amsc}"
        },
        allow_redirects = False
    )

    if "__Host-MSAAUTH" in data.cookies:
        print("[+] - Got Polished MSAAUTH")
        return data.cookies["__Host-MSAAUTH"]
    
    elif "working to restore all services" in data.text:
        print("[X] - Microsoft is down")
        return "Down"
    
    else:
        print("[-] - Failed to get polish MSAAUTH. Returning MSAAUTH")
        return host