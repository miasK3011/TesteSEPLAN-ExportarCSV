import requests, sys, csv

QNTD_REGISTROS = 5000
URL = f"https://dadosabertos.aneel.gov.br/api/3/action/datastore_search?resource_id=b1bd71e7-d0ad-4214-9053-cbd58e9564a7&limit={QNTD_REGISTROS}"


def get_data(url):
    try:
        response = requests.get(url)
        return response.json().get("result").get("records")
    except Exception as e:
        print(f"Erro ao fazer requisição: {e}")
        sys.exit(1)


def main():
    potencia_total = {}
    response = get_data(URL)

    # Trata a resposta e calcula a potência total por estado e classe de consumo.
    if response:
        for record in response:
            classe = record["DscClasseConsumo"]
            if classe in ["Rural", "Residencial"]:
                estado = record["SigUF"]
                potencia = record["MdaPotenciaInstaladaKW"].replace(",", ".")
                potencia = float(potencia)
                if estado not in potencia_total:
                    potencia_total[estado] = {"Rural": 0, "Residencial": 0}
                potencia_total[estado][classe] += potencia

        # Salva o resultado processado em um arquivo CSV.
        with open("potencia_total_por_estado.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Estado", "Classe de Consumo", "Potencia Total"])
            for estado, classes in potencia_total.items():
                for classe, potencia in classes.items():
                    writer.writerow([estado, classe, potencia])


if __name__ == "__main__":
    main()
