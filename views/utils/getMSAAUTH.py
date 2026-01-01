from urllib.parse import quote
import requests

# Gets __Host-MSAAUTH
def getMSAAUTH(email: str, flowToken: str, data: dict, code: str = None):

    if not code:

        loginData = requests.post(
            url = data["urlPost"],
            headers = {
                "host": "login.live.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://login.live.com",
                "Connection": "keep-alive",
                "Referer": "https://login.live.com/",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Priority": "u=0, i"
            },
            cookies = data["cookies"],
            data = {
                "login": email,
                "loginfmt": email,
                "slk": flowToken,
                "psRNGCSLK": flowToken,
                "type": "21",
                "PPFT": data["ppft"]
            }
        )

    else:

        cookies = ""
        set_cookie_headers = data["headers"].get('set-cookie')
        if set_cookie_headers:
            for cookie_header in set_cookie_headers.split(','):
                cookies += cookie_header.split(";")[0] + "; "

        loginData = requests.post(
            url = data["urlPost"],
            headers = {
                "host": "login.live.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": "1213",
                "Origin": "https://login.live.com",
                "Cookie": cookies,
                "Connection": "keep-alive",
                "Referer": "https://login.live.com/",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Priority": "u=0, i"
            },
            data = {
                "login": email,
                "loginfmt": email,
                "SentProofIDE": flowToken,
                "otc": code,
                "type": "27",
                "PPFT": data["ppft"]
            }
        )

    if "__Host-MSAAUTH" in loginData.cookies:
        MSAAUTH = loginData.cookies["__Host-MSAAUTH"]
        # urlPost = re.search(r'"urlPost"\s*:\s*"([^"]+)"', loginData.text).group(1)
        # nppft = quote(re.search(r'"sFT"\s*:\s*"([^"]+)"', loginData.text).group(1), safe='-*')
    else:
        print(loginData.text)
        print(loginData.cookies)
        print(loginData.headers)
        return None

    return MSAAUTH # return [MSAAUTH, urlPost, nppft]