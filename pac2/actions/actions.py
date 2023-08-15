from typing import List,Dict
from .base import BaseAction, SkeltonNode
from .variable import InitVariableAction

class Actions:
    """
    Action NodeをTree構造にまとめるのクラス.
    JSONスキーマ上のActionsフィールに対応する.
    """
    # Actionsは以下の制約を持つTree構造であると定義する
    # - ルートノードは必ずSkeltonNodeである
    #   - ルートノードはExportでは出力されない
    # - ルートノードを除くすべてのノードは親ノードを1つのみ持つ
    # - ノードは0個以上の子ノードを持つ
    #
    # Note: 変数の初期化ActionをTopチェーンに持っていく方法
    # Triggerから最初に実行されるActionsをroot_actionsと定義し、
    # root_actions以外ではVariableの初期化Actionを追加できないようにする。
    # root_actionsでは、Variableの初期化Actionを最初に直列で実行するようにする。
    def __init__(self,is_root:bool=False) -> None:
        self.root_node = SkeltonNode("root")
        self.last_update_node = self.root_node
        self.is_root_actions: bool = is_root
        self.nodes:List[BaseAction] = []
        self.nodes.append(self.root_node)
        self.variable_init_nodes:List[BaseAction] = []

    def __action_validation(self, new_action: BaseAction, prev_action:BaseAction=None):
        if new_action in self.nodes:
            raise ValueError(f"{new_action} already exists in Actions")
        if new_action.prev_node:
            raise ValueError(f"{new_action} is already connected with f{new_action.prev_node}")
        if prev_action:
            if prev_action not in self.nodes:
                raise ValueError(f"{prev_action} not in Actions")
        # root_actions(Flowで定義されるactions)以外でのInitVariableを制限する
        if not self.is_root_actions and isinstance(new_action,InitVariableAction):
            raise ValueError(f"{new_action} cannot set into If/Foreach/Scope/Util Actions")


    def add_top(self, new_action: BaseAction):
        # Validation
        self.__action_validation(new_action)

        # ノード間の接続を行う
        new_action.prev_node = self.root_node
        self.root_node.next_node.append(new_action)

        # runAfterを更新する
        new_action.update_runafter()

        # ノード情報の更新
        self.last_update_node = new_action
        self.nodes.append(new_action)

    def add_after(self, new_action: BaseAction, prev_action: BaseAction, force_exec:bool=False):
        # Validation
        self.__action_validation(new_action,prev_action)

        # ノード間の接続を行う
        new_action.prev_node = prev_action
        prev_action.next_node.append(new_action)

        # runAfterを更新する
        new_action.update_runafter(force_exec)

        # ノード情報の更新
        self.last_update_node = new_action
        self.nodes.append(new_action)


    def append(self, new_action: BaseAction, force_exec:bool=False):
        # Validation
        self.__action_validation(new_action)

        # ノード間の接続を行う
        new_action.prev_node = self.last_update_node
        self.last_update_node.next_node.append(new_action)

        # runAfterを更新する
        new_action.update_runafter(force_exec)

        # ノード情報の更新
        self.last_update_node = new_action
        self.nodes.append(new_action)

    def export(self) -> Dict:
        d = {}
        for node in self.nodes:
            if isinstance(node,SkeltonNode):
                continue
            d[node.action_name] = node.export()
        return d

