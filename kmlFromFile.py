from Alerts import showConfirm, showInfo
from FileManager import (
    calculate_coordinates,
    saveFile,
    selectFile,
)
import simplekml


def getLocationFromLine(line: str, inverted=False):
    # Remove a quebra de linha
    line = line.strip()
    # Separa as colunas da linha
    columns = line.split(";")
    # Monta estrutura similar ao da imagem
    if inverted:
        columns.reverse()
    # Obtem as latitudes e longitudes
    latitude = calculate_coordinates(columns[0].split(","))
    longitude = calculate_coordinates(columns[1].split(","))
    # Retorna as coordenadas
    return (latitude, longitude)


if __name__ == "__main__":
    # Informa o ti­tulo da janela
    showInfo(
        "Gerando KML",
        "Selecione o arquivo CSV que contém as informações de localização",
    )
    # Abre a tela de seleção das imagens para extrair a localização
    csvPath = selectFile(type="*.csv")

    # Lista de localizações
    locations = []

    if csvPath:
        # Lista de cordenadas para o polygono *A ordem é invertida (longitude, latitude)
        polygonCoordinates = []
        # Cria um novo objeto kml
        kml = simplekml.Kml()
        # Confirma se as informações estão invertidas
        inverted = showConfirm(
            "Inverter as coordenadas? S, W para W, S",
            "As coordenadas são invertidas?",
        )
        # Abre o arquivo CSV
        with open(csvPath, "r") as file:
            # Pega as linhas do arquivo
            lines = file.readlines()
            # Indexador
            count = 0
            # Pontos
            points = 0
            # Percorre as linhas do arquivo
            for line in lines:
                # Incrementa o contador
                count += 1
                # Verifica se a linha tem pelo menos 22 caracteres
                if len(line) >= 22:
                    # localizacao
                    location = getLocationFromLine(line, inverted)
                    # Adiciona à lista de coordenadas para o polygono
                    polygonCoordinates.append(location)
                    # Adiciona um novo marcador ao kml com o nome da imagem e as coordenadas obtidas dela
                    point = kml.newpoint(name=count, coords=[location])
                    # Incrementa o contador de pontos
                    points += 1

        # Adiciona um polígono com o nome de "Área" ligando todos os marcadores
        polygon = kml.newpolygon(name="Área", outerboundaryis=polygonCoordinates)

        # Obtem o local para salvar
        outPath = saveFile(alt="Arquivos KML", type="*.kml")

        # Se o local foi selecionado
        if outPath:
            # Verifica se não é um arquivo
            if not outPath.endswith(".kml"):
                # Arquivo kml
                outPath += f".kml"

            # Salvar arquivo kml
            kml.save(outPath)
            # Exibe a mensagem de operação com sucesso
            showInfo(
                "Arquivo KMZ gerado com sucesso",
                f"Arquivo gerado com {points} marcadores em:\n {outPath}\n\n"
                + "::: by Paulo Wender :::",
            )
        else:
            showInfo("Operação cancelada", "Nenhum local foi selecionado")
