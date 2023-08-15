from . import connectors
import re
import json

uuid4_pattern = r"-[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

def truncate_string(input_str, max_length=20):
    if len(input_str) > max_length:
        return input_str[:max_length]
    else:
        return input_str

class Connections:
    """
    PowerAutomateが接続しているAPI情報を管理するためのクラス.
    CreateFlowActionで新たにフローを作成する際に必要となる情報を管理する.
    接続先を追加する際は、以下のような接続先文字列が入力されることを期待する.

    e.g.) shared-flowmanagemen-282bc0cf-2475-4655-8262-a6938ff6b179
    e.g.) ce9f7496f45f46649d94019c8f65693f
    """
    def __init__(self):
        self.connections = []

    def add_connections_from_json_file(self, path:str) -> int:
        self.connections = []

        with open(path,"r") as f:
            data = json.load(f)

        for item in data["value"]:
            connection = {}
            connection["connectionName"] = item["name"]
            connection["id"] = item["properties"]["apiId"]
            self.connections.append(connection)

        return len(self.connections)

    def add_connection(self, connection_name:str, id:str=None):
        d = {}
        # Conector一覧のActionsから列挙した情報から接続先情報を取得する
        # connectionNameに設定されているAPI名は20文字に丸められて、"_"が"-"に置換されている.
        apiname = re.sub(uuid4_pattern, "", connection_name)
        apiname = truncate_string(apiname).replace("-","_")

        d["connectionName"] = connection_name
        
        if not id:
            if apiname not in connectors.CONNECTORS:
                ValueError("API not found. Set id name to add_connection().")
            d["id"] = connectors.CONNECTORS[apiname]
        else:
            d["id"] = id

        self.connections.append(d)

    def export(self):
        return self.connections
