import json
from ..actions import BaseAction, Actions
from ..triggers import BaseTrigger, Triggers

DEFALUT_PARAMETER = {
    "$connections": {
        "defaultValue": {},
        "type": "Object"
    },
    "$authentication": {
        "defaultValue": {},
        "type": "SecureObject"
    }
}

DEFAULT_SCHEMA = "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#"
DEFAULT_VERSION = "1.0.0.0"


class Flow:
    """
    PowerAutomateのFlowを管理するクラス.
    """
    schema:str = DEFAULT_SCHEMA
    contentVersion:str = DEFAULT_VERSION
    parameters:dict = DEFALUT_PARAMETER

    def __init__(self):
        self.triggers:BaseTrigger = Triggers()
        self.root_actions:BaseAction = Actions(True)

    def set_trigger(self, trigger: BaseTrigger):
        self.triggers.append(trigger)

    def append_action(self, action: BaseAction, force_exec:bool = False, prev_action: BaseAction=None):
        if prev_action:
            self.root_actions.add_after(action,prev_action,force_exec)
        else:
            self.root_actions.append(action,force_exec)
    
    def add_top_action(self,action: BaseAction):
        self.root_actions.add_top(action)

    def export(self):
        d = {}
        d["$schema"] = Flow.schema
        d["contentVersion"] = Flow.contentVersion
        d["parameters"] = Flow.parameters
        d["triggers"] = self.triggers.export()
        d["actions"] = self.root_actions.export()
        return d

    def export_json(self, xor_key=None):
        json_str = json.dumps(self.export())

        if xor_key:
            xor_key = [int(x) for x in xor_key.split(",")]
            json_str = ",".join([str(ord(json_str[i]) ^ xor_key[i%len(xor_key)]) for i in range(len(json_str))])

        return json_str