from typing import List, Dict
import uuid


class BaseTrigger:
    """
    Triggerを定義するための基底クラス.
    """
    def __init__(self, name: str):
        self.trigger_name:str = name
        self.metadata:Dict = {}
        self.metadata["operationMetadataId"] = uuid.uuid4().__str__()
        self.type:str = None

    def export(self) -> Dict:
        # 継承先のClassで実装されることを期待する
        raise NotImplementedError()
    
    def __repr__(self):
        return f"TriggerNode:{self.trigger_name}({self.type})"


class Triggers:
    """
    Trigger Nodeをリスト構造にまとめるのクラス.
    JSONスキーマ上のTriggersフィールに対応する.
    """
    def __init__(self,is_root:bool=False) -> None:
        self.nodes:List[BaseTrigger] = []

    def append(self, new_trigger: BaseTrigger):
        # Validation
        if new_trigger in self.nodes:
            raise ValueError(f"{new_trigger} already exists in Triggers")
        self.nodes.append(new_trigger)

    def export(self) -> Dict:
        d = {}
        for node in self.nodes:
            d[node.trigger_name] = node.export()
        return d


class RecurrenceTrigger(BaseTrigger):
    """
    繰り返し実行Triggerを定義するクラス
    """
    def __init__(self, name:str):
        super().__init__(name)
        self.type = "Recurrence"
        self.recurrence = {}
    
    def set_schedule(self, frequency:str, interval:int):
        self.recurrence["frequency"] = frequency
        self.recurrence["interval"] = interval
    
    def export(self):
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["recurrence"] = self.recurrence
        return d


class ManualTrigger(BaseTrigger):
    """
    マニュアル実行Triggerを定義するクラス
    """
    def __init__(self, name:str):
        super().__init__(name)
        self.type = "Request"
        self.kind = "Button"
        self.inputs = {"schema": {"type": "object", "properties": {}, "required" :[]}}

    def export(self):
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["kind"] = self.kind
        d["inputs"] = self.inputs
        return d

