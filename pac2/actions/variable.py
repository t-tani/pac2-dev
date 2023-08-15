from typing import Dict
from .base import BaseAction

class VariableTypes:
    string = "string"
    integer = "integer"
    boolean = "boolean"
    float = "float"
    array = "array"
    object = "object"


class InitVariableAction(BaseAction):
    """
    変数の初期化アクションを定義するクラス
    """
    def __init__(self, name:str, var_name:str, var_type:str, value=None):
        super().__init__(name)
        self.type = "InitializeVariable"
        self.inputs = {}
        self.variables = []
        var = {
            "name": var_name,
            "type": var_type
        }
        if value:
            var["value"] = value
        self.variables.append(var)
        self.inputs["variables"] = self.variables

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d


class SetVariableAction(BaseAction):
    """
    変数を更新するアクションを定義するクラス
    """
    def __init__(self, name:str, var_name:str, value):
        super().__init__(name)
        self.type = "SetVariable"
        self.inputs = {
            "name": var_name,
            "value": value
        }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d


class AppendStringToVariableAction(BaseAction):
    """
    変数に文字列を追加するアクションを定義するクラス
    """
    def __init__(self, name:str, var_name:str, value:str):
        super().__init__(name)
        self.type = "AppendToStringVariable"
        self.inputs = {
            "name": var_name,
            "value": value
        }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d


class IncrementVariableAction(BaseAction):
    """
    変数の値を増やすアクションを定義するクラス
    """
    def __init__(self, name:str, var_name:str, value:str):
        super().__init__(name)
        self.type = "IncrementVariable"
        self.inputs = {
            "name": var_name,
            "value": value
        }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d


class DecrementVariableAction(BaseAction):
    """
    変数の値を減らすアクションを定義するクラス
    """
    def __init__(self, name:str, var_name:str, value:str):
        super().__init__(name)
        self.type = "DecrementVariable"
        self.inputs = {
            "name": var_name,
            "value": value
        }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d