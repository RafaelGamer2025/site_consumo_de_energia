import psutil
import random

def monitor_pc():

    cpu = psutil.cpu_percent()

    ram = psutil.virtual_memory().percent

    watts = random.randint(80,300)

    return {

        "cpu": cpu,
        "ram": ram,
        "watts": watts
    }

def calcular_energia(dados):

    nome = dados["nome"]

    watts = float(dados["watts"])

    horas = float(dados["horas"])

    dias = float(dados["dias"])

    tarifa = float(dados["tarifa"])

    quantidade = int(dados["quantidade"])

    casa = float(dados["casa"])

    kwh = (
        watts *
        horas *
        dias *
        quantidade
    ) / 1000

    preco = kwh * tarifa

    return {

        "nome": nome,

        "kwh": round(kwh,2),

        "preco": round(preco,2),

        "casa": casa
    }

def gerar_ideias(resultado):

    ideias = []

    if resultado["kwh"] > 100:

        ideias.append(
        "⚠ Consumo alto"
        )

    if resultado["preco"] > 200:

        ideias.append(
        "💸 Conta cara"
        )

    return ideias