# from FileManager import open_file_dialog
from GoogleServices import GoogleServices

__name__ = "__main__"
google = GoogleServices()

f = google.getFolderByName(google.ROOT_DIR)
print(f)
# imgs = open_file_dialog()
# firstImage = imgs[0]
# firstImageName = firstImage.split("/")[-1]
# firstImagePath = firstImage.split(f"/{firstImageName}")[0]
# firstImageDirectory = firstImagePath.split("/")[-1]

# folder = google.getFolderByName(firstImageDirectory)

# if folder:
#     print("Folder already exists")
#     imgExists = google.getFileByName(folder["id"], firstImageName)

#     print(imgExists)
