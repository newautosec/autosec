import httpx

async def generateEmail(email: str, password: str) -> str:

    async with httpx.AsyncClient() as session:

        await session.post(
            url = "https://api.mail.tm/accounts",
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            json = {
                "address": email,
                "password": password
            }
        )

        token = await session.post(
            url = "https://api.mail.tm/token",
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            json = {
                "address": email,
                "password": password
            }
        )

        return token.json()["token"]


    