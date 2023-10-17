import os
from tkinter import Tk, filedialog
from Alerts import showError
from PIL import Image
from PIL.ExifTags import TAGS
import simplekml


def create_file(filePath, content, override=True):
    if not os.path.exists(filePath):
        try:
            with open(filePath, "w") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Erro ao criar o arquivo: {e}")
            return False
    else:
        if override:
            try:
                with open(filePath, "w") as f:
                    f.write(content)
                return True
            except Exception as e:
                print(f"Erro ao criar o arquivo: {e}")
                return False
        else:
            return False


def rename_file(filePath, newName):
    if not os.path.exists(filePath):
        return False

    path = os.path.dirname(filePath)
    fileExtension = os.path.splitext(filePath)[1]
    newName = path + "/IMG_" + newName + fileExtension
    try:
        os.rename(filePath, newName)
        return newName
    except Exception as e:
        print(f"Erro ao renomear o arquivo: {e}")
        return False


def get_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            metadata = img._getexif()
            if metadata:
                extracted_metadata = {}
                for tag_id, value in metadata.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    extracted_metadata[tag_name] = value
                return extracted_metadata
            else:
                return None
    except Exception as e:
        showError("Erro ao extrair informações de imagem", e)
        return None


def compress_image(input_path, output_path, quality=85):
    """
    Comprime uma imagem.

    Parâmetros:
        input_path (str): Caminho da imagem de entrada.
        output_path (str): Caminho onde a imagem comprimida será salva.
        quality (int): Qualidade da compressão (0-100). Quanto menor, mais compressão.

    Retorna:
        bool: True se a compressão foi bem-sucedida, False caso contrário.
    """
    try:
        img = Image.open(input_path)
        img.save(output_path, optimize=True, quality=quality)
        return True
    except Exception as e:
        print(f"Erro ao comprimir a imagem: {e}")
        return False


def calculate_coordinates(data):
    if data and len(data) < 3:
        return None

    a = f"{data[0]}"
    b = f"{data[1]}"
    c = f"{data[2]}"

    if a == "nan" or b == "nan" or c == "nan":
        return None

    a = float(data[0])
    b = float(data[1])
    c = float(data[2])

    return (a + b / 60 + c / 3600) * -1


def extract_gps_info(imagePath):
    try:
        with Image.open(imagePath) as img:
            metadata = img._getexif()
            if metadata:
                for tag_id, value in metadata.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    if tag_name == "GPSInfo":
                        lat = calculate_coordinates(value[2])
                        lon = calculate_coordinates(value[4])
                        if lat and lon:
                            return {"latitude": lat, "longitude": lon}
            else:
                return None
    except Exception as e:
        showError("Erro ao extrair informações de imagem", e)
        return None

    # metadata = get_image_metadata(imagePath)
    # if "GPSInfo" in metadata:
    #     gps_info = metadata["GPSInfo"]
    #     try:
    #         # Obtem a latitude
    #         latitude = calculate_coordinates(gps_info[2])
    #         # Obtem a longitude
    #         longitude = calculate_coordinates(gps_info[4])

    #         # Converte para latitude sul e longitude oeste se necessário
    #         if gps_info[3] == "S":
    #             latitude = -latitude
    #         if gps_info[1] == "W":
    #             longitude = -longitude

    #         return latitude, longitude
    #     except Exception as e:
    #         showError("Erro ao extrair informações de GPS", e)
    #         return None
    # else:
    #     return None


# Abre a tela de seleção das imagens para extrair a localização
def open_file_dialog(type="*.jpg;*.png;*.jpeg"):
    root = Tk()
    root.withdraw()
    files_paths = filedialog.askopenfilenames(filetypes=[("Image files", type)])
    root.destroy()
    return files_paths


def selectFile(alt="Todos os arquivos", type="*"):
    root = Tk()
    root.withdraw()
    filePath = filedialog.askopenfilename(filetypes=[(alt, type)])
    root.destroy()
    return filePath


def saveFile(title="Salvar arquivo", alt="Todos os arquivos", type="*"):
    root = Tk()
    root.withdraw()
    filePath = (
        filedialog.asksaveasfilename(
            title=title,
            filetypes=[(alt, type)],
        ),
    )
    root.destroy()
    return filePath[0]


def create_kmz_file(latitude, longitude):
    kml = simplekml.Kml()
    kml.newpoint(name="Localização", coords=[(longitude, latitude)])
    kml_file = f"localizacao_marca.kml"
    kml.save(kml_file)

    # print(f"Arquivo KMZ gerado com sucesso: {kml_file}")
