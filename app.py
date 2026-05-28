from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import redirect
from flask import session

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from funcoes import monitor_pc
from funcoes import calcular_energia
from funcoes import gerar_ideias

app = Flask(__name__)

import json 

# ====================================
# CHAVE SESSÃO
# ====================================

app.secret_key = "neo_energy"

# ====================================
# EMAIL DO BOT
# ====================================

EMAIL = "sobrenomecleitan@gmail.com"

def verificar_e_criar_json():
    # Verifica se o arquivo NÃO existe
    if not os.path.exists(ARQUIVO_USERS):
        # Cria o arquivo com uma lista vazia dentro
        with open(ARQUIVO_USERS, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo, indent=4)
        print(f"O arquivo {ARQUIVO_USERS} foi criado com sucesso!")

# Executa a função assim que o script roda
verificar_e_criar_json()

# SENHA DE APP GOOGLE
SENHA = "COLOQUE_SEU_CODIGO_DE_EMAIL"

# ====================================
# FUNÇÃO ENVIAR EMAIL
# ====================================

def enviar_email(destino, assunto, mensagem):

    try:

        msg = MIMEMultipart()

        msg["From"] = EMAIL

        msg["To"] = destino

        msg["Subject"] = assunto

        msg.attach(
            MIMEText(
                mensagem,
                "plain"
            )
        )

        servidor = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        servidor.starttls()

        servidor.login(
            EMAIL,
            SENHA
        )

        servidor.send_message(msg)

        servidor.quit()

        print("EMAIL ENVIADO")

    except Exception as e:

        print("ERRO EMAIL:")
        print(e)

# ====================================
# LOGIN
# ====================================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        nome = request.form.get("name")

        email = request.form.get("email")

        energia = request.form.get("energia")

        # 1. CRIA O DICIONÁRIO COM OS DADOS DO NOVO USUÁRIO
        novo_usuario = {
            "nome": nome,
            "email": email,
            "energia": energia
        }

        # 2. ABRE O ARQUIVO, LÊ A LISTA ATUAL E ADICIONA O NOVO USUÁRIO
        try:
            with open(ARQUIVO_USERS, "r", encoding="utf-8") as arquivo:
                lista_usuarios = json.load(arquivo)
        except Exception:
            lista_usuarios = [] # Garante uma lista vazia se houver erro ao ler

        lista_usuarios.append(novo_usuario)

        # 3. SALVA A LISTA ATUALIZADA DE VOLTA NO ARQUIVO
        with open(ARQUIVO_USERS, "w", encoding="utf-8") as arquivo:
            json.dump(lista_usuarios, arquivo, indent=4, ensure_ascii=False)

        # SALVA SESSÃO (Mantém o usuário logado no navegador)
        session["nome"] = nome
        session["email"] = email
        session["energia"] = energia

        # ENVIA EMAIL
        enviar_email(
            email,
            "⚡ Bem-vindo ao Neo Energy",
            f"""
Olá {nome}, boas vindas!

Obrigado por entrar no Neo Energy ⚡

Seu nível de energia:
{energia}

Aproveite o sistema!
"""
        )

        return redirect("/dashboard")

    return render_template("login.html")

# ====================================
# DASHBOARD
# ====================================

@app.route("/dashboard")
def dashboard():

    if "nome" not in session:

        return redirect("/")

    return render_template(

        "index.html",

        nome=session["nome"],

        energia=session["energia"]
    )

# ====================================
# MONITOR
# ====================================

@app.route("/monitor")
def monitor():

    dados = monitor_pc()

    return jsonify(dados)

# ====================================
# CALCULAR
# ====================================

@app.route("/calcular", methods=["POST"])
def calcular():

    dados = request.json

    resultado = calcular_energia(dados)

    ideias = gerar_ideias(resultado)

    resultado["ideias"] = ideias

    return jsonify(resultado)

# ====================================
# INICIAR SITE
# ====================================

if __name__ == "__main__":

    enviar_email(

        "sobrenomecleitan@gmail.com",

        "⚡ Neo Energy Online",

        "Servidor iniciado com sucesso."
    )

    app.run(debug=True)