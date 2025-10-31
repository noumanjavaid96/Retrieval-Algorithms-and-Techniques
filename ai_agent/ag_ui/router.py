import json
from fastapi import Request, Response
from fastapi.routing import APIRoute

class AgUiRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request):
            response: Response = await original_route_handler(request)
            if isinstance(response, AgUiResponse):
                response.headers["Content-Type"] = "application/json"
                return response
            return response

        return custom_route_handler

class AgUiResponse(Response):
    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = self.render(content)

    def render(self, content):
        if isinstance(content, list):
            return b"[" + b",".join(self.render(item) for item in content) + b"]"
        if isinstance(content, dict):
            return json.dumps(content).encode('utf-8')
        return content
