from typing import List,Dict
import uuid

class State:
    """
    Actionの実行ステータスを列挙するクラス.
    """
    Aborted = "Aborted"
    Cancelled = "Cancelled"
    Failed = "Failed"
    Faulted = "Faulted"
    Ignored = "Ignored"
    Paused = "Paused"
    Running = "Running"
    Skipped = "Skipped"
    Succeeded = "Succeeded"
    Suspended = "Suspended"
    TimedOut = "TimedOut"
    Waiting = "Waiting"


class BaseAction:
    """
    Action Nodeを定義するための基底クラス.
    """

    def __init__(self, name: str):
        self.action_name:str = name
        self.type:str = ""
        self.runafter:Dict = {} # Accept 0 or 1 node
        self.metadata:Dict = {}
        self.prev_node:BaseAction = None
        self.next_node:List[BaseAction] = []
        self.metadata["operationMetadataId"] = uuid.uuid4().__str__()
        pass

    def export(self) -> Dict:
        # 継承先のClassで実装されることを期待する
        raise NotImplementedError()
    
    def update_runafter(self, force_exec:bool=False):
        state_list = [State.Succeeded]
        if force_exec:
            state_list = [State.Succeeded, State.Failed, State.Skipped, State.TimedOut]
        # Actionsの先頭ノード
        if isinstance(self.prev_node, SkeltonNode):
            self.runafter = {}
        else:
            self.runafter[self.prev_node.action_name] = state_list
    
    def __repr__(self):
        return f"ActionNode:{self.action_name}({self.type})"

class SkeltonNode(BaseAction):
    """
    ActionsクラスのTree構造の頂点ノード専用のクラス。
    ActionsのTree構造をハンドルしやすくするためのノード。
    """
    def __init__(self, name:str):
        super().__init__(name)
    
    def export(self):
        return None
