import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import yaml


class GoogleServices:
    ROOT_DIR: str = "KML_IMAGES"
    folderParentID: str = None
    auth: GoogleAuth = None
    drive: GoogleDrive = None

    def __init__(self):
        print("Inicializando Google Services...")
        # Init Google Auth
        self.auth = GoogleAuth()
        # Check if file exists
        if os.path.exists("creds.json"):
            # Try to load saved client credentials
            self.auth.LoadCredentialsFile("creds.json")
            print("Credentials loaded")
        if self.auth.credentials is None:
            # Authenticate if they're not there
            print("Authenticating")
            try:
                authorization = self.auth.LocalWebserverAuth()
                print(authorization)
            except Exception as e:
                print("Authentication failed with error: " + e.args[0])
                exit()
        elif self.auth.access_token_expired:
            # Refresh them if expired
            self.auth.Refresh()
        else:
            # Initialize the saved creds
            self.auth.Authorize()
        # Save the current credentials to a file
        self.auth.SaveCredentialsFile("creds.json")
        print("Credentials saved")
        # Initialize the Drive API
        self.drive = GoogleDrive(self.auth)
        print("Google Drive initialized")

        # Create a new folder on Google Drive if it doesn't exist
        print("Creating root folder...")
        self.folderParentID = self.makeDirectory(self.ROOT_DIR, self.folderParentID)

        # Save the settings to a file
        # with open("settings.yaml", "a") as f:
        #     yaml.dump({"folderID": self.folderParentID}, f)
        #     print(f"Folder ID saved: {self.folderParentID}")

        # Set the folder ID
        self.folderParentID = self.folderParentID
        print(f"Folder ID: {self.folderParentID}")

    # Create a new folder on Google Drive
    def makeDirectory(self, folderName, parentFolderId=None) -> str:
        # Check if the folder already exists
        folder = self.getFolderByName(folderName)

        if folder is not None:
            # Folder already exists
            print("Folder already exists")
            return folder["id"]
        else:
            print(f"Creating folder: {folderName}")
            file_metadata = {
                "title": folderName,
                "mimeType": "application/vnd.google-apps.folder",
            }

            if not parentFolderId is None:
                file_metadata["parents"] = [{"id": parentFolderId}]

            folder = self.drive.CreateFile(file_metadata)
            folder.Upload()
            return folder["id"]

    # Upload an image to Google Drive
    def uploadImage(self, imagePath: str, directory: str):
        # Get the name of the image
        fileName = imagePath.split("/")[-1]
        # create a new folder on Google Drive
        folderId = self.makeDirectory(directory, self.folderParentID)

        # Check if the image already exists
        image = self.getFileByName(folderId, fileName)
        if image:
            return image["thumbnailLink"]

        # upload the image
        print(f"Uploading image: {fileName}")
        file = self.drive.CreateFile({"title": fileName, "parents": [{"id": folderId}]})
        file.SetContentFile(imagePath)
        file.Upload()

        # return the thumbnail link
        return file["thumbnailLink"]

    # Check if a folder exists on Google Driver by ID
    def getFolderByID(self, folderID) -> dict | None:
        # res = self.drive.files().get(fileId=folderID, fields="id, name").execute()

        # Query Google Drive
        qr = f"id='{folderID}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        # Get the list of files
        file_list = self.drive.ListFile({"q": qr}).GetList()

        # Return None if the list is empty
        if file_list == []:
            return None

        # Return the first file
        return file_list[0]

    # Check if a folder exists on Google Drive by Name
    def getFolderByName(self, folderName, parentFolderId=None) -> dict | None:
        # Query Google Drive
        qr = f"title='{folderName}' and mimeType='application/vnd.google-apps.folder' and trashed=false"

        # If the parent ID is set
        if parentFolderId:
            qr += f" and '{parentFolderId}' in parents"

        # Get the list of files
        file_list = self.drive.ListFile({"q": qr}).GetList()

        # Return None if the list is empty
        if file_list == []:
            return None

        # Return the first file
        return file_list[0]

    # Check if a file exists on Google Drive
    def getFileByName(self, folderId, fileName):
        file_list = self.drive.ListFile(
            {"q": f"'{folderId}' in parents and title='{fileName}' and trashed=false"}
        ).GetList()

        if len(file_list) == 0:
            return None

        return file_list[0]
