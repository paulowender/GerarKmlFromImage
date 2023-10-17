import datetime
from Alerts import confirmAction, showError, showInfo, showWarning
from FileManager import (
    extract_gps_info,
    get_image_metadata,
    open_file_dialog,
    rename_file,
)
from GoogleServices import GoogleServices
import os
import simplekml

if __name__ == "__main__":
    # Informa o ti­tulo da janela
    showInfo("Gerando KML", "Selecione as imagens que deseja extrair a localização")
    # Abre a tela de seleção das imagens para extrair a localização
    image_paths = open_file_dialog()
    # Se houver imagens selecionadas
    if image_paths:
        # Pega o local dos arquivos
        directory = os.path.dirname(image_paths[0])
        # Lista de cordenadas (latitude, longitude)
        coordinates = []
        # Lista de cordenadas para o polygono *A ordem é invertida (longitude, latitude)
        polygonCoordinates = []
        # Cria um novo objeto kml
        kml = simplekml.Kml()
        # Nome do ultimo diretorio
        dirName = directory.split("/")[-1]
        # Contador de imagens
        count = 0
        # Pergunta se deseja adicionar as imagens ao KML
        addImages = confirmAction(
            "Adicionar imagens ao KML",
            "Deseja adicionar as imagens ao KML? Isso pode demorar um pouco.",
        )
        # Se deseja adicionar as imagens
        if addImages:
            # Cria um novo objeto GoogleServices
            google = GoogleServices()
        # Percorre as imagens selecionadas
        for image_path in image_paths:
            # Incrementa o contador
            count += 1
            # Pega o nome da imagem atual
            imageName = image_path.split("/")[-1]
            # Remove a extensão do nome da imagem
            imageName = imageName.split(".")[0]
            # Obtem as coordenadas do marcador
            location = extract_gps_info(image_path)
            # Caso não tenha informações de GeoLocalização passa para a proxima imagem
            if not location:
                continue

            # Obtem a latitude e longitude
            latitude = location["latitude"]
            longitude = location["longitude"]
            # Adiciona à lista de coordenadas
            coordinates.append((latitude, longitude))
            # Adiciona à lista de coordenadas para o polygono
            polygonCoordinates.append((longitude, latitude))
            # Renomeia o arquivo
            newImagePath = rename_file(image_path, f"{count}")
            # TODO : Verificar se a imagem foi renomeada
            if newImagePath != False:
                # Se tiver sucesso, altera o nome do marcador
                imageName = count
            # Adiciona um novo marcador ao kml com o nome da imagem e as coordenadas obtidas dela
            point = kml.newpoint(name=imageName, coords=[(longitude, latitude)])

            if addImages:
                try:
                    # Envia a imagem para
                    image_url = google.uploadImage(newImagePath, dirName)
                    # Adiciona a imagem ao marcador
                    if image_url:
                        point.description = f'<![CDATA[<img style="max-width:500px;" src="{image_url}">]]>'

                except Exception as e:
                    showError("Falha ao enviar imagem", e)

        if coordinates == []:
            showWarning(
                "Operação cancelada",
                "Nenhuma informação de localização encontrada",
            )
            exit()

        # Adiciona um polígono com o nome de "Área" ligando todos os marcadores
        polygon = kml.newpolygon(name="Área", outerboundaryis=polygonCoordinates)

        # Data e hora atual
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Arquivo kml
        kmlPath = directory + f"/{dirName}_{now}.kml"
        # Salvar arquivo kml
        kml.save(kmlPath)
        # Exibe a mensagem de operação com sucesso
        showInfo(
            "Arquivo KMZ gerado com sucesso",
            f"Arquivo gerado em:\n {kmlPath}\n\n" + "::: by Paulo Wender :::",
        )
    else:
        showInfo("Operação cancelada", "Nenhuma imagem selecionada")
