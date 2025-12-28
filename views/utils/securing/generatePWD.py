from os import urandom

def generatePWD() -> str:
    
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(chars[c % len(chars)] for c in urandom(8))
    