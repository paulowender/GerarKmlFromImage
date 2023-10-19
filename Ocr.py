from easygui import msgbox
import pytesseract
from PIL import Image

from FileManager import saveFile, selectFiles
from Logger import saveLog

# Select images
paths = selectFiles()

# File contents
contents = ""

# Loop through each image
for path in paths:
    # Open the image file
    image = Image.open(path)

    # Perform OCR using PyTesseract
    text = pytesseract.image_to_string(image, nice=1)

    # Append the extracted text to the contents
    contents += "\n" + text

# Select output file
outputPath = saveFile(alt="Arquivo de Texto", type="*.txt")

# If no output file was selected, exit
if not outputPath:
    exit()

# If the output file does not end with .txt, add it
if not outputPath.endswith(".txt"):
    outputPath += ".txt"

# Save the contents to the output file
saveLog(text, outputPath)
