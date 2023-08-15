from typing import Dict
from .base import BaseAction

class AddToTimeAction(BaseAction):
    """
    時間への追加アクションを定義するクラス
    """
    def __init__(self, name:str, timeUnit:str, interval:int, baseTime:str="@{utcNow()}"):
        super().__init__(name)
        self.type = "Expression"
        self.kind = "AddToTime"
        self.inputs = {}
        self.inputs["baseTime"] = baseTime
        self.inputs["interval"] = interval
        self.inputs["timeUnit"] = timeUnit

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["kind"] = self.kind
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d

class WaitAction(BaseAction):
    """
    待機アクションを定義するクラス
    """
    def __init__(self, name:str, count:int, unit:str):
        super().__init__(name)
        self.type = "Wait"
        
        self.interval = {}
        self.interval["count"] = count
        self.interval["unit"] = unit

        self.inputs = {}
        self.inputs["interval"] = self.interval

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d

