from typing import Dict
from urllib.parse import urlparse
from .base import BaseAction

METHODS = set(["GET","POST"])

class HttpAction(BaseAction):
    """
    HTTP接続を行うActionを定義するClass. 
    """
    # Todo: Cookieの対応
    # Todo: HTTPレスポンス処理のハンドル

    def __init__(self, name: str, uri: str, method: str):
        super().__init__(name)
        self.type = "Http"
        if method not in METHODS:
            raise ValueError("Unsupported method type")
        self.method:str = method
        ## insert validation
        self.uri:str = uri
        self.body:str = None
        self.headers:Dict = None
        self.cookie:str = None

    def set_body(self, body:str):
        self.body = body
    
    def set_headers(self, headers:dict):
        self.headers = headers

    def set_cookie(self, cookie:str):
        self.cookie = cookie

    def export(self) -> Dict:
        d = {}
        inputs = {}
        
        inputs["method"] = self.method
        inputs["uri"] = self.uri
        if self.body:
            inputs["body"] = self.body
        if self.headers:
            inputs["headers"] = self.headers
        if self.cookie:
            inputs["cookie"] = self.cookie
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = inputs

        return d