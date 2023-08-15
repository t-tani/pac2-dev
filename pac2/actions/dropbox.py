from typing import Dict
from .base import BaseAction

class DropboxCreateFileAction(BaseAction):
    """
    Dropboxで新規ファイルを作成するActionを定義するClass. 
    """

    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_dropbox",
        "connectionName": "shared_dropbox",
        "operationId": "CreateFile"
    }

    def __init__(self, name: str, folderPath: str, filename: str, body: str):
        super().__init__(name)
        self.type = "OpenApiConnection"

        self.folderPath:str = folderPath
        self.filename:str = filename
        self.body:str = body

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["folderPath"] = self.folderPath
        parameters["name"] = self.filename
        parameters["body"] = self.body

        inputs["host"] = DropboxCreateFileAction.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = inputs

        return d
    

class DropboxGetFileContentAction(BaseAction):
    """
    Dropboxでファイルを取得するActionを定義するClass. 
    """

    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_dropbox",
        "connectionName": "shared_dropbox",
        "operationId": "GetFileContent"
    }

    def __init__(self, name: str, id: str, inferContentType: bool = True):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.id:str = id
        self.inferContentType:str = str(inferContentType)

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["id"] = self.id
        parameters["inferContentType"] = self.inferContentType

        inputs["host"] = DropboxGetFileContentAction.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = inputs

        return d
    
class DropboxUpdateFileAction(BaseAction):
    """
    Dropboxでファイルを更新するActionを定義するClass. 
    """

    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_dropbox",
        "connectionName": "shared_dropbox",
        "operationId": "UpdateFile"
    }

    def __init__(self, name: str, id: str, body: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.id:str = id
        self.body:str = body

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["id"] = self.id
        parameters["body"] = self.body

        inputs["host"] = DropboxUpdateFileAction.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = inputs

        return d
    
class DropboxListFilesInFolderAction(BaseAction):
    """
    Dropboxでファイルリストを出力するActionを定義するClass. 
    """

    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_dropbox",
        "connectionName": "shared_dropbox",
        "operationId": "ListFolder"
    }

    def __init__(self, name: str, id: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.id:str = id

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["id"] = self.id

        inputs["host"] = DropboxListFilesInFolderAction.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = inputs

        return d

class DropboxListFilesInRootFolderAction(BaseAction):
    """
    Dropboxでルートのファイルリストを出力するActionを定義するClass. 
    """

    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_dropbox",
        "connectionName": "shared_dropbox",
        "operationId": "ListRootFolder"
    }

    def __init__(self, name: str):
        super().__init__(name)
        self.type = "OpenApiConnection"

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        inputs["host"] = DropboxListFilesInRootFolderAction.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = inputs

        return d

class DropboxCopyFileAction(BaseAction):
    """
    DropboxでファイルをコピーするActionを定義するClass. 
    """

    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_dropbox",
        "connectionName": "shared_dropbox",
        "operationId": "CopyFile"
    }

    def __init__(self, name: str, source: str, destination: str, overwrite: bool = False):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.source:str = source
        self.destination:str = destination
        self.overwrite:str = str(overwrite)

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["source"] = self.source
        parameters["destination"] = self.destination
        parameters["overwrite"] = self.overwrite

        inputs["host"] = DropboxCopyFileAction.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = inputs

        return d

class DropboxDeleteFileAction(BaseAction):
    """
    Dropboxでファイルを削除するActionを定義するClass. 
    """

    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_dropbox",
        "connectionName": "shared_dropbox",
        "operationId": "DeleteFile"
    }

    def __init__(self, name: str, id: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.id:str = id

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["id"] = self.id

        inputs["host"] = DropboxDeleteFileAction.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = inputs

        return d

class DropboxGetFileMetadataAction(BaseAction):
    """
    Dropboxでファイルのメタデータを取得するActionを定義するClass. 
    """

    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_dropbox",
        "connectionName": "shared_dropbox",
        "operationId": "GetFileMetadata"
    }

    def __init__(self, name: str, id: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.id:str = id

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["id"] = self.id

        inputs["host"] = DropboxGetFileMetadataAction.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = inputs

        return d

class DropboxExtractArchiveToFolderAction(BaseAction):
    """
    Dropboxでアーカイブファイルを展開するActionを定義するClass. 
    """

    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_dropbox",
        "connectionName": "shared_dropbox",
        "operationId": "ExtractFolderV2"
    }

    def __init__(self, name: str, source: str, destination: str, overwrite: bool = False):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.source:str = source
        self.destination:str = destination
        self.overwrite:str = str(overwrite)

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["source"] = self.source
        parameters["destination"] = self.destination
        parameters["overwrite"] = self.overwrite

        inputs["host"] = DropboxExtractArchiveToFolderAction.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = inputs

        return d

class DropboxGetFileContentUsingPathAction(BaseAction):
    """
    Dropboxでパスを指定してファイルを取得するActionを定義するClass. 
    """

    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_dropbox",
        "connectionName": "shared_dropbox",
        "operationId": "GetFileContentByPath"
    }

    def __init__(self, name: str, path: str, inferContentType: bool = True):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.path:str = path
        self.inferContentType:str = str(inferContentType)

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["path"] = self.path
        parameters["inferContentType"] = self.inferContentType

        inputs["host"] = DropboxGetFileContentUsingPathAction.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = inputs

        return d

class DropboxGetFileMetadataUsingPathAction(BaseAction):
    """
    Dropboxでパスを指定してファイルを取得するActionを定義するClass. 
    """

    connection_host = {
        "apiId": "/providers/Microsoft.PowerApps/apis/shared_dropbox",
        "connectionName": "shared_dropbox",
        "operationId": "GetFileMetadataByPath"
    }

    def __init__(self, name: str, path: str):
        super().__init__(name)
        self.type = "OpenApiConnection"
        self.path:str = path

    def export(self) -> Dict:
        inputs = {}
        parameters = {}

        parameters["path"] = self.path

        inputs["host"] = DropboxGetFileMetadataUsingPathAction.connection_host
        inputs["parameters"] = parameters

        d = {}
        d["metadata"] = self.metadata
        d["type"] = self.type
        d["runAfter"] = self.runafter        
        d["inputs"] = inputs

        return d












