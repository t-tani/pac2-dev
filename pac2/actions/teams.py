import uuid
from typing import List,Dict
from .base import BaseAction

class GetAllTeamsAction(BaseAction):
    """
    Teamsでユーザーが所属するチーム一覧を取得するアクション
    """
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_teams",
        "connectionName": "shared_teams",
        "operationId": "GetAllTeams"
    }

    def __init__(self, name:str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.inputs = {}
        self.parameters = {}
        self.inputs["host"] = GetAllTeamsAction.connection_host
        self.inputs["parameters"] = {}

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d

class GetTeamAction(BaseAction):
    """
    Teamsでチームの情報を取得するアクション
    """
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_teams",
        "connectionName": "shared_teams",
        "operationId": "GetTeam"
    }

    def __init__(self, name:str, team_id:str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.inputs = {}
        self.parameters = {}
        self.inputs["host"] = GetTeamAction.connection_host
        self.inputs["parameters"] = {
            "teamId": team_id
        }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d

class GetChannelsForGroupAction(BaseAction):
    """
    Teamsでチームのチャンネル一覧を取得するアクション
    """
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_teams",
        "connectionName": "shared_teams",
        "operationId": "GetChannelsForGroup"
    }

    def __init__(self, name:str, group_id:str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.inputs = {}
        self.parameters = {}
        self.inputs["host"] = GetChannelsForGroupAction.connection_host
        self.inputs["parameters"] = {"groupId": group_id}

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d


class GetMessagesFromChannelAction(BaseAction):
    """
    Teamsでチャンネルのメッセージを取得するアクション
    """
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_teams",
        "connectionName": "shared_teams",
        "operationId": "GetMessagesFromChannel"
    }

    def __init__(self, name:str, group_id:str, channel_id:str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.inputs = {}
        self.parameters = {}
        self.inputs["host"] = GetMessagesFromChannelAction.connection_host
        self.inputs["parameters"] = {
            "groupId": group_id,
            "channelId": channel_id
        }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d

class GetChatsAction(BaseAction):
    """
    Teamsでチャット一覧を取得するアクション
    """
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_teams",
        "connectionName": "shared_teams",
        "operationId": "GetChats"
    }

    def __init__(self, name:str, chat_type:str="all", topic:str="all"):
        """
        args: 
            name:  任意の名前
            chat_type: "all","group","meeting","oneOnOne" から選択
            topic: "all" から選択
        """
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.inputs = {}
        self.parameters = {}
        self.inputs["host"] = GetChatsAction.connection_host
        self.inputs["parameters"] = {
            "chatType": chat_type,
            "topic": topic
        }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d


class ListMembersAction(BaseAction):
    """
    Teamsでチャット一覧を取得するアクション
    """
    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_teams",
        "connectionName": "shared_teams",
        "operationId": "ListMembers"
    }

    def __init__(self, name:str, id:str, thread_type:str="groupchat"):
        """
        args: 
            name:  任意の名前
            id: chat idを入力、GetChatsActionの結果に対してforeachして、idを取得する. 
                e.g.) @items('foreach')?['id']
            thread_type: "groupchat"
            i
        """
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.inputs = {}
        self.parameters = {}
        self.inputs["host"] = ListMembersAction.connection_host
        self.inputs["parameters"] = {
            "threadType": thread_type,
            "body/recipient": id
        }

    def export(self) -> Dict:
        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = self.inputs
        return d