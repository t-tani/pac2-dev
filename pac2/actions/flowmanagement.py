import uuid
from typing import List,Dict
from .base import BaseAction
from .connections import Connections

class CreateFlowAction(BaseAction):
    """
    フロー作成アクションを定義するクラス
    定義されているString変数をJsonに変換し、フローを作成することを期待する。
    """
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_flowmanagement",
        "connectionName": "shared_flowmanagement",
        "operationId": "CreateFlow"
        }

    def __init__(self, name:str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.inputs = {}
        self.parameters = {}
        self.inputs["host"] = CreateFlowAction.connection_host
        self.inputs["parameters"] = {}

    def set_parameters(self,display_name:str, var_name:str, connection_ref:Connections):
        self.parameters["environmentName"] = "@workflow()?['tags/environmentName']"
        self.parameters["Flow/properties/displayName"] = display_name
        self.parameters["Flow/properties/definition"] = f"@json(variables('{var_name}'))"
        self.parameters["Flow/properties/state"] = "Started"
        self.parameters["Flow/properties/connectionReferences"] = connection_ref.export()
        self.inputs["parameters"] = self.parameters

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d


class DeleteFlowAction(BaseAction):
    """
    フロー削除アクションを定義するクラス
    """
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_flowmanagement",
        "connectionName": "shared_flowmanagement",
        "operationId": "DeleteFlow"
        }

    def __init__(self, name:str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.inputs = {}
        self.parameters = {}
        self.inputs["host"] = DeleteFlowAction.connection_host
        self.inputs["parameters"] = {
                    "environmentName": "@workflow()?['tags/environmentName']",
                    "flowName": "@workflow()?['tags']?['logicAppName']"
                }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["runAfter"] = self.runafter        
        d["type"] = self.type
        d["inputs"] = self.inputs
        return d


class ListConnectionsAction(BaseAction):
    """
    アカウントで有効化されているコネクション一覧を取得するアクションを定義するクラス
    """
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_flowmanagement",
        "connectionName": "shared_flowmanagement",
        "operationId": "ListConnections"
        }

    def __init__(self, name:str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.inputs = {}
        self.parameters = {}
        self.inputs["host"] = ListConnectionsAction.connection_host
        self.inputs["parameters"] = {
                    "environmentName": "@workflow()?['tags/environmentName']",
                }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["runAfter"] = self.runafter        
        d["type"] = self.type
        d["inputs"] = self.inputs
        return d

class ListUserEnvironmentsAction(BaseAction):
    """
    アカウントで有効化されているコネクション一覧を取得するアクションを定義するクラス
    """
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_flowmanagement",
        "connectionName": "shared_flowmanagement",
        "operationId": "ListUserEnvironments"
        }

    def __init__(self, name:str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.inputs = {}
        self.parameters = {}
        self.inputs["host"] = ListUserEnvironmentsAction.connection_host
        self.inputs["parameters"] = {}

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["runAfter"] = self.runafter        
        d["type"] = self.type
        d["inputs"] = self.inputs
        return d
