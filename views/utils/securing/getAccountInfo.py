import requests

def getAccountInfo() -> dict:
    """
    Fetches Microsoft account owner information.

    Returns:
        {
            firstName,
            lastName,
            fullName,
            region,
            birthday
        }
    """

    default = {
        "firstName": "Failed to Get",
        "lastName": "Failed to Get",
        "fullName": "Failed to Get",
        "region": "Failed to Get",
        "birthday": "Failed to Get"
    }

    try:
        
        # Your Code...
        # 
        # 
        # 
        # 
        # 
        # 
        # 

        info = {}

        if not info:
            return default

        return {
            "firstName": info.get("firstName", default["firstName"]),
            "lastName": info.get("lastName", default["lastName"]),
            "fullName": info.get("fullName", default["fullName"]),
            "region": info.get("region", default["region"]),
            "birthday": info.get("birthday", default["birthday"]),
        }

    except Exception as e:
        print(f"[x] Failed to fetch account owner info: {e}")
        return default
