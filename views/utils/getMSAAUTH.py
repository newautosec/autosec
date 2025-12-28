from urllib.parse import quote
import requests

# Gets __Host-MSAAUTH
def getMSAAUTH(email: str, flowToken: str, data: dict, code: str = None):

    if not code:

        loginData = requests.post(
            url = data["urlPost"],
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
                "Content-Type": "application/x-www-form-urlencoded"
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
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": cookies
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