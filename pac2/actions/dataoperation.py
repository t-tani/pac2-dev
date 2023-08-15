from typing import List,Dict
from .base import BaseAction

class TableFormat:
    csv = "CSV"
    html = "HTML"


class SelectAction(BaseAction):
    """
    選択アクションを定義するクラス.map関数に近い動作を行う。
    args:
        input: ArrayまたはPowerAutomateでArrayとなる式
        key:   strまたはPowerAutomate上で文字列となる式 (e.g.) "@{item()}"
        value: 任意の型 (e.g.) "@item()"

    他のアクションから結果にアクセスするには以下の関数式を用いる
        @body('<name>')  // Object型
    """
    def __init__(self, name:str, inputs:List|str, key:str, value:str):
        super().__init__(name)
        self.type = "Select"
        self.inputs = {
            "from" : inputs,
            "select" : {
                key: value
            }
        }

    def __init__(self, name:str, inputs:List|str, select:str):
        super().__init__(name)
        self.type = "Select"
        self.inputs = {
            "from": inputs,
            "select": select
        }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d


class CreateTableAction(BaseAction):
    """
    テーブル作成のアクションを定義するクラス
    args:
        inputs: DictのArrayまたはPowerAutomateでObjectのArrayとなる式
        fromat: TabelFormat.csv または TableFormat.html 
    
    他のアクションから結果にアクセスするには以下の関数式を用いる
        @body('<name>')  // String型
    """
    def __init__(self, name:str, inputs:List[Dict]|str, format:str):
        super().__init__(name)
        self.type = "Table"
        self.inputs = {
            "from" : inputs,
            "format" : format
        }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d

class ComposeAction(BaseAction):
    """
    データ作成のアクションを定義するクラス
    args:
        inputs: 任意の型または関数式

    他のアクションから結果にアクセスするには以下の関数式を用いる
        @body('<name>')  // 入力した型
    """
    def __init__(self, name:str, inputs:List|Dict|str, format:str):
        super().__init__(name)
        self.type = "Compese"
        self.inputs = inputs

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d


class FileterArrayAction(BaseAction):
    """
    Arrayから条件に一致する要素を取り出すアクションを定義するクラス
    args:
        inputs: ListまたはPowerAutomate上でArrayとなる関数式
        where: PowerAutomateで値を評価する関数式 (e.g.) "@greater(int(item()),10)" 
    
    他のアクションから結果にアクセスするには以下の関数式を用いる
        @body('<name>')  // Array型
    """
    def __init__(self, name:str, inputs:List|str, where:str):
        super().__init__(name)
        self.type = "Query"
        self.inputs = {
            "from" : inputs,
            "where" : where
        }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d


class JoinAction(BaseAction):
    """
    ArrayをJoinするアクションを定義するクラス. join()のような動作
    args:
        inputs: ListまたはPowerAutomate上でArrayとなる関数式
        join_with: 結合に用いる文字列 (e.g.) ";"
    
    他のアクションから結果にアクセスするには以下の関数式を用いる。
        @body('<name>')   // String型
    """
    def __init__(self, name:str, inputs:List|str, join_with:str):
        super().__init__(name)
        self.type = "Join"
        self.inputs = {
            "from" : inputs,
            "joinWith" : join_with
        }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d
