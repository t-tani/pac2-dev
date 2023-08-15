from typing import List,Dict
import uuid
import json
from os import makedirs, path, walk
import shutil
import zipfile
import tempfile
from random import randint
from datetime import datetime, timezone
from ..flow import Flow

def get_timestamp() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f") + str(randint(0,9)) + "Z"

class Resource:
    """
    manifestで定義されるresouceを管理するためのクラス
    """
    def __init__(self,type:str, suggested_creation_type:str,
                creation_type: str, configurable_by:str, hierarchy:str, display_name:str, icon_uri:str=None):
        self.uuid = uuid.uuid4().__str__()
        self.dependencies = []
        self.id = None
        self.name = None
        self.type = type
        self.suggested_creation_type = suggested_creation_type
        self.creation_type = creation_type
        self.configurable_by = configurable_by
        self.hierarchy = hierarchy
        self.display_name = display_name
        self.icon_uri = icon_uri

    def set_api_info(self,id:str, name:str):
        self.id = id
        self.name = name

    def set_dependencies(self,resources:List):
        for resource in resources:
            self.dependencies.append(resource.uuid)
        self.dependencies = list(set(self.dependencies))

    def export(self):
        d = {}
        if self.id:
            d["id"] = self.id
        if self.name:
            d["name"] = self.name
        d["type"] = self.type
        d["suggestedCreationType"] = self.suggested_creation_type
        if self.creation_type:
            d["creationType"] = self.creation_type
        details = {}
        details["displayName"] = self.display_name
        if self.icon_uri:
            details["iconUri"] = self.icon_uri
        d["details"] = details
        d["configurableBy"] = self.configurable_by
        d["hierarchy"] = self.hierarchy
        d["dependsOn"] = self.dependencies
        return d
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o,Resource):
            return self.uuid == __o.uuid
        else:
            return False

    def __hash__(self):
        return hash(self.uuid)


class Package:
    """
    zip形式でimportできるPowerAutomateのフローを生成するクラス.
    以下の構成のソリューションを構成する
    
    .
    ├── Microsoft.Flow
    │   └── flows
    │       ├── 4fb1e7f2-309e-49fb-ba6e-a5ab23b65c01
    │       │   ├── apisMap.json
    │       │   ├── connectionsMap.json
    │       │   └── definition.json
    │       └── manifest.json
    └── manifest.json
    
    Web GUIからインポートする最初のペイロード生成することために利用する.
    """
    def __init__(self,display_name:str, flow:Flow):
        self.display_name = display_name
        self.__apis:List[Resource] = []
        self.__connections:List[Resource] = []
        self.__api_connection_map:Dict[Resource,Resource] = {}
        self.__exist_connections:dict = {}

        # ソリューションに定義したFlowを設定する
        self.flow = flow

        # Flow Resourceの初期化
        self.__set_flow_resource()
        # 

    def __set_flow_resource(self):
        self.__flow_resource = Resource("Microsoft.Flow/flows","New","Existing, New, Update","User","Root", self.display_name)

    def set_flow_management_connector(self, connection_name:str=None):
        # PowerAutomate Management APIの設定
        api = Resource("Microsoft.PowerApps/apis","Existing",None,"System","Child","Flow Management","https://connectoricons-prod.azureedge.net/releases/v1.0.1650/1.0.1650.3374/flowmanagement/icon.png")
        api.set_api_info("/providers/Microsoft.PowerApps/apis/shared_flowmanagement","shared_flowmanagement")

        # PowerAutomate Management Connectionの設定
        connection = Resource("Microsoft.PowerApps/apis/connections","Existing","Existing","User","Child","User","https://connectoricons-prod.azureedge.net/releases/v1.0.1644/1.0.1644.3342/flowmanagement/icon.png")

        # Connectionの依存APIの設定
        connection.set_dependencies([api])

        # 既存のconenction情報の設定
        if connection_name:
            self.__exist_connections["shared_flowmanagement"] = {
                "connectionName" : connection_name,
                "source": "Invoker",
                "id": "/providers/Microsoft.PowerApps/apis/shared_flowmanagement",
                "tier": "NotSpecified"
            }
        self.__apis.append(api)
        self.__connections.append(connection)
        self.__api_connection_map[connection] = api

    def set_dropbox_connector(self, connection_name:str=None):
        # Dropbox APIの設定
        api = Resource("Microsoft.PowerApps/apis","Existing",None,"System","Child","Dropbox","https://connectoricons-prod.azureedge.net/releases/v1.0.1651/1.0.1651.3382/dropbox/icon.png")
        api.set_api_info("/providers/Microsoft.PowerApps/apis/shared_dropbox","shared_dropbox")

        # Dropbox Connectionの設定
        connection = Resource("Microsoft.PowerApps/apis/connections","Existing","Existing","User","Child","Dropbox","https://connectoricons-prod.azureedge.net/releases/v1.0.1651/1.0.1651.3382/dropbox/icon.png")

        # Connectionの依存APIの設定
        connection.set_dependencies([api])

        # 既存のconenction情報の設定
        if connection_name:
            self.__exist_connections["shared_dropbox"] = {
                "connectionName" : connection_name,
                "source": "Invoker",
                "id": "/providers/Microsoft.PowerApps/apis/shared_dropbox",
                "tier": "NotSpecified"
            }
        self.__apis.append(api)
        self.__connections.append(connection)
        self.__api_connection_map[connection] = api

    def set_sharepoint_connector(self, connection_name:str=None):
        # SharePoint APIの設定
        api = Resource("Microsoft.PowerApps/apis","Existing",None,"System","Child","SharePoint","https://connectoricons-prod.azureedge.net/u/shgogna/globalperconnector-train1/1.0.1639.3312/sharepointonline/icon.png")
        api.set_api_info("/providers/Microsoft.PowerApps/apis/shared_sharepointonline","shared_sharepointonline")

        # SharePoint Connectionの設定
        connection = Resource("Microsoft.PowerApps/apis/connections","Existing","Existing","User","Child","SharePoint","https://connectoricons-prod.azureedge.net/u/shgogna/globalperconnector-train1/1.0.1639.3312/sharepointonline/icon.png")

        # Connectionの依存APIの設定
        connection.set_dependencies([api])

        # 既存のconenction情報の設定
        if connection_name:
            self.__exist_connections["shared_sharepointonline"] = {
                "connectionName" : connection_name,
                "source": "Invoker",
                "id": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline",
                "tier": "NotSpecified"
            }
        self.__apis.append(api)
        self.__connections.append(connection)
        self.__api_connection_map[connection] = api      

    def export_solution_manifest(self)->dict:
        # update flow dependencies
        self.__flow_resource.set_dependencies(self.__apis)
        self.__flow_resource.set_dependencies(self.__connections)

        d = {}
        d["schema"] = "1.0"
        details = {}
        details["displayName"] = self.display_name
        details["description"] = ""
        details["createdTime"] = get_timestamp()
        details["packageTelemetryId"] = uuid.uuid4().__str__()
        details["creator"] = "N/A"
        details["sourceEnvironment"] = ""
        d["details"] =  details

        resources = {}
        # Define flow resource
        resources[self.__flow_resource.uuid] = self.__flow_resource.export()
        # Define api resources
        for api in self.__apis:
            resources[api.uuid] = api.export()
        # Define connection resources
        for con in self.__connections:
            resources[con.uuid] = con.export()

        d["resources"] = resources
        return d
    
    def export_apis_map(self):
        d = {}
        for api in self.__apis:
            d[api.name] = api.uuid
        return d
    
    def export_connections_map(self):
        d = {}
        for connection in self.__connections:
            d[self.__api_connection_map[connection].name] = connection.uuid
        return d

    def export_package_manifest(self) -> dict:
        d = {}
        d["packageSchemaVersion"] = "1.0"
        d["flowAssets"] = {
            "assetPaths" : [self.__flow_resource.uuid]
        }
        return d
    
    def export_definition(self):
        d = {}
        d["name"] = uuid.uuid4().__str__()
        d["id"] = "/providers/Microsoft.Flow/flows/" + d["name"]
        d["type"] = "Microsoft.Flow/flows"
        properties = {}
        properties["apiId"] = "/providers/Microsoft.PowerApps/apis/shared_logicflows"
        properties["displayName"] = self.display_name
        properties["definition"] = self.flow.export()
        properties["connectionReferences"] = self.__exist_connections
        properties["flowFailureAlertSubscribed"] = False
        properties["isManaged"] = False
        d["properties"] = properties
        return d
    
    def __write_json_file(self, path:str, content:dict):
        with open(path, 'w') as f:
            f.write(json.dumps(content))

    def export_zipfile(self):
        work_dir = tempfile.TemporaryDirectory().name
        definition_dir = path.join(work_dir,"Microsoft.Flow","flows",self.__flow_resource.uuid)

        # ディレクトリ階層作成
        makedirs(definition_dir,exist_ok=True)
        
        # ./manifest.json
        self.__write_json_file(path.join(work_dir,"manifest.json"),self.export_solution_manifest())
        # ./Microsoft.Flow/flows/manifest.json
        self.__write_json_file(path.join(work_dir,"Microsoft.Flow","flows","manifest.json"),self.export_package_manifest())
        # ./Microsoft.Flow/flows/{uuid}/definition.json
        self.__write_json_file(path.join(definition_dir,"definition.json"),self.export_definition())
        # ./Microsoft.Flow/flows/{uuid}/apisMap.json
        self.__write_json_file(path.join(definition_dir,"apisMap.json"),self.export_apis_map())
        # ./Microsoft.Flow/flows/{uuid}/connectionsMap.json
        self.__write_json_file(path.join(definition_dir,"connectionsMap.json"),self.export_connections_map())

        #zipファイル作成
        zip_file = zipfile.ZipFile(f"{self.display_name}.zip","w",zipfile.ZIP_DEFLATED)
        for root,_,files in walk(work_dir):
            for file in files:
                zip_file.write(path.join(root,file), path.relpath(path.join(root, file), work_dir))

        zip_file.close()

        # clean-up
        shutil.rmtree(work_dir)


