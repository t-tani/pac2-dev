from typing import Dict
from .base import BaseAction
from .actions import Actions
from .condition import Condition

class IfStatement(BaseAction):
    """
    If statementを定義するためのクラス.
    """
    def __init__(self, name: str, condition: Condition):
        super().__init__(name)
        self.type:str = "If"
        self.condition:Condition = condition
        self.true_actions: Actions = None
        self.false_actions: Actions = None

    def set_true_actions(self, actions:Actions):
        self.true_actions = actions

    def set_false_actions(self, actions:Actions):
        self.false_actions = actions
    
    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["expression"] = self.condition.export()
        d["actions"] = self.true_actions.export()
        d["else"] = {"actions": self.false_actions.export()}
        return d


class ForeachStatement(BaseAction):
    """
    Foreach statementを定義するためのクラス
    """
    def __init__(self, name:str, foreach:str):
        super().__init__(name)
        self.type:str = "Foreach"
        self.foreach:str = foreach
        self.actions: Actions = None

    def set_actions(self, actions: Actions):
        self.actions = actions

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["foreach"] = self.foreach
        d["actions"] = self.actions.export()
        return d


class ScopeStatement(BaseAction):
    """
    Scope statementを定義するためのクラス
    """
    def __init__(self, name:str, actions:Actions):
        super().__init__(name)
        self.type:str = "Scope"
        self.actions:Actions = actions

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["actions"] = self.actions.export()
        return d

class DoUntilStatement(BaseAction):
    """
    do_until statementを定義するためのクラス
    expressionには以下のような式関数が入ることが期待される。
    
    express: "@equals(variables('count'), 10)"
    """
    def __init__(self, name:str, actions:Actions, expression:str, limit_count:int=60):
        super().__init__(name)
        self.type:str = "Until"
        self.actions:Actions = actions
        self.limit = {
            "count" : limit_count,
            "timeout" : "PT1H"
        }
        self.expression = expression

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter
        d["actions"] = self.actions.export()
        d["expression"] = self.expression
        d["limit"] = self.limit
        return d