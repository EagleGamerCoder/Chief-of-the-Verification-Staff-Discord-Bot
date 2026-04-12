'''

Info 

'''

# ------------------------------------------------------------ IMPORTS ------------------------------------------------------------

# Standard Imports
import aiohttp 

# Modules


# ------------------------------------------------------------ CLASSES ------------------------------------------------------------

class Services:
    def __init__(self):
        self.http_session: aiohttp.ClientSession | None = None

    async def ensure_http(self):
        if self.http_session is None or self.http_session.closed:
            self.http_session = aiohttp.ClientSession()

    async def close(self):
        if self.http_session and not self.http_session.closed:
            await self.http_session.close()

# ------------------------------------------------------------ MAIN ------------------------------------------------------------

http_services = Services()