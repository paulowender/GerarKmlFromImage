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
            # Obtem os metadados da imagem
            metadata = get_image_metadata(image_path)
            # Caso tenha os metadados
            if metadata:
                # Obtem as informações de GeoLocalização
                gps_info = extract_gps_info(metadata)
                # Caso tenha dados de GeoLocalização
                if gps_info:
                    # Obtem a latitude e longitude
                    latitude, longitude = gps_info
                    # Adiciona à lista de coordenadas
                    coordinates.append((latitude, longitude))
                    # Adiciona à lista de coordenadas para o polygono
                    polygonCoordinates.append((longitude, latitude))
                    # Renomeia o arquivo
                    newImagePath = rename_file(image_path, f"{count}")
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

                # Caso não tenha dados de GeoLocalização
                else:
                    # Printa no console uma mensagem de aviso
                    showWarning(
                        "As informações de GPS não estão disponíveis na imagem",
                        image_path,
                    )

            # Caso não tenha os metadados na imagem
            else:
                # Printa no console uma mensagem de aviso
                showError("Erro ao extrair informações de imagem", image_path)

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
