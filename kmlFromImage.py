import datetime
from Alerts import confirmAction, showError, showInfo, showWarning
from FileManager import (
    extract_gps_info,
    open_file_dialog,
    rename_file,
)
from GoogleServices import GoogleServices
import os
import simplekml

from Logger import saveLog

if __name__ == "__main__":
    # Informa o ti­tulo da janela
    showInfo("Gerando KML", "Selecione as imagens que deseja extrair a localização")
    # Data e hora atual
    saveLog("\n")
    saveLog("================ Operação Inicializada ================")
    saveLog(datetime.datetime.now().strftime("%d-%m-%Y - %H:%M:%S"))
    # Abre a tela de seleção das imagens para extrair a localização
    image_paths = open_file_dialog()
    # Se houver imagens selecionadas
    if image_paths:
        # Pega o local dos arquivos
        directory = os.path.dirname(image_paths[0])
        # Lista de cordenadas (longitude, latitude)
        coordinates = []
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
            saveLog("Iniciando Google Services")
            # Cria um novo objeto GoogleServices
            google = GoogleServices()
        # Percorre as imagens selecionadas
        for image_path in image_paths:
            saveLog(f"Adicionando imagem: {image_path}")
            # Incrementa o contador
            count += 1
            # Obtem as coordenadas do marcador
            location = extract_gps_info(image_path)
            saveLog(f"Localização: {location}")
            # Caso não tenha informações de GeoLocalização passa para a proxima imagem
            if not location:
                continue

            # Obtem a latitude e longitude
            coordinate = (location["longitude"], location["latitude"])
            # Adiciona à lista de coordenadas
            coordinates.append(coordinate)
            # Renomeia o arquivo
            newImagePath = rename_file(image_path, f"{count}")
            # Verificar se a imagem foi renomeada
            if newImagePath:
                # Se tiver sucesso, altera o nome do marcador
                image_path = newImagePath
                saveLog(f"Imagem renomeada para: {image_path}")
            # Adiciona um novo marcador ao kml com o nome da imagem e as coordenadas obtidas dela
            point = kml.newpoint(name=count, coords=[coordinate])

            if addImages:
                try:
                    # Envia a imagem para
                    saveLog(f"Enviando imagem: {image_path}")
                    image_url = google.uploadImage(image_path, dirName)
                    # Adiciona a imagem ao marcador
                    if image_url:
                        saveLog(f"Imagem enviada com sucesso: {image_url}")
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
        polygon = kml.newpolygon(name="Área", outerboundaryis=coordinates)
        saveLog("Adicionando polígono ao KML")

        # Data e hora atual
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Arquivo kml
        kmlPath = directory + f"/{dirName}_{now}.kml"
        # Salvar arquivo kml
        kml.save(kmlPath)
        saveLog(f"Arquivo KML gerado com sucesso: {kmlPath}")
        # Exibe a mensagem de operação com sucesso
        showInfo(
            "Arquivo KMZ gerado com sucesso",
            f"Arquivo gerado com {count} imagens em:\n {kmlPath}\n\n"
            + "::: by Paulo Wender :::",
        )
        saveLog(datetime.datetime.now().strftime("%d-%m-%Y - %H:%M:%S"))
        saveLog("================ Operação Finalizada ================")
    else:
        showInfo("Operação cancelada", "Nenhuma imagem selecionada")
        saveLog("================ Operação Cancelada ================")
