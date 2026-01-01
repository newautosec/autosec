from views.utils.parsers.decode import decode
import requests
import re

def getCookies():
    apicanary = None
    amsc = None
    
    data = requests.get(
        url="https://account.live.com/password/reset",
        allow_redirects=False
    )
    
    apicanary = decode(re.search(r'"apiCanary":"([^"]+)"', data.text).group(1))
    
    for cookie in data.cookies:
        if cookie.name == "amsc":
            amsc = cookie.value
            break
    
    return [apicanary, amsc]