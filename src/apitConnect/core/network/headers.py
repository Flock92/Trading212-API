class HeaderCapture:
    def __init__(self):
        self.headers = {}

    async def handle_request(self, request):
        if (
            "services.trading212.com" in request.url
            or "live.trading212.com" in request.url
        ):
            headers = request.headers
            if "x-trader-client" in headers:
                if "accountId" in headers.get("x-trader-client", ""):
                    self.headers = headers