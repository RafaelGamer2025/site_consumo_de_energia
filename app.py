from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import redirect
from flask import session
from flask_sqlalchemy import SQLAlchemy


from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import smtplib

import os

import dotenv
from dotenv import load_dotenv

load_dotenv()


EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from funcoes import monitor_pc
from funcoes import calcular_energia
from funcoes import gerar_ideias

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///neoenergy.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

import json 

class Usuario(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        nullable=False
    )

    energia = db.Column(
        db.String(50),
        nullable=False
    )

    senha = db.Column(
        db.String(255),
        nullable=False
    )
class Consumo(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario_id = db.Column(
    db.Integer,
    nullable=False
)

    nome_aparelho = db.Column(
        db.String(100)
    )

    watts = db.Column(
        db.Float
    )

    horas = db.Column(
        db.Float
    )

    dias = db.Column(
        db.Float
    )

    quantidade = db.Column(
        db.Integer
    )

    tarifa = db.Column(
        db.Float
    )

    kwh = db.Column(
        db.Float
    )

    preco = db.Column(
        db.Float
    )
# ====================================
# CHAVE SESSÃO
# ====================================

app.secret_key = SECRET_KEY

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

        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = Usuario.query.filter_by(
            email=email
        ).first()

        if usuario and check_password_hash(usuario.senha, senha):

            session["usuario_id"] = usuario.id
            session["nome"] = usuario.nome
            session["email"] = usuario.email
            session["energia"] = usuario.energia
        # ENVIA EMAIL
            enviar_email(
                email, "⚡ Bem-vindo ao Neo Energy", f"""
    Olá {session['nome']}, boas vindas!

    Obrigado por entrar no Neo Energy ⚡

    Seu nível de energia:
    {session['energia']}

    Aproveite o sistema!
    """
            )

            return redirect("/dashboard")

        return render_template("login.html", error="Email ou senha inválidos")
    return render_template("login.html")
@app.route("/admin/logout")
def admin_logout():

    session.pop("admin", None)

    return redirect("/admin")
@app.route("/usuarios")
def usuarios():

    if not session.get("admin"):
        return redirect("/")

    lista = Usuario.query.all()

    return render_template(
        "usuarios.html",
        usuarios=lista
    )
# ====================================
# DASHBOARD
# ====================================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        nome = request.form.get("name")
        email = request.form.get("email")
        senha = request.form.get("senha")
        energia = request.form.get("energia")

        existe = Usuario.query.filter_by(
            email=email
        ).first()

        if existe:

            return render_template(
                "register.html",
                error="Email já cadastrado"
            )

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            energia=energia,
            senha=generate_password_hash(senha)
        )

        db.session.add(novo_usuario)
        db.session.commit()

        return redirect("/")

    return render_template("register.html")
@app.route("/dashboard")
def dashboard():

    if "nome" not in session:
        return redirect("/")

    usuarios = []

    consumos = Consumo.query.filter_by(usuario_id=session["usuario_id"]).order_by(Consumo.id.desc()).all()

    return render_template("index.html", nome=session["nome"], energia=session["energia"], usuarios=usuarios, consumos=consumos, is_admin=session.get("admin", False))
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
#=====================================
#admin
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        senha = request.form.get("senha")

        if senha == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect("/admin/dashboard")

        return render_template(
            "admin_login.html",
            error="Senha inválida"
        )

    return render_template("admin_login.html")
@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin"):
        return redirect("/admin")

    usuarios = Usuario.query.order_by(
        Usuario.id.desc()
    ).all()

    consumos = Consumo.query.order_by(
        Consumo.id.desc()
    ).all()

    return render_template(
        "admin.html",
        usuarios=usuarios,
        consumos=consumos,
        total_users=len(usuarios),
        total_consumos=len(consumos)
    )
# ====================================
# MONITOR
# ====================================

@app.route("/monitor")
def monitor():

    dados = monitor_pc()

    return jsonify(dados)
@app.route("/sobre_mim")
def sobre_mim():
    return render_template("sobre_mim.html")
# ====================================
# CALCULAR
# ====================================

@app.route("/calcular", methods=["POST"])
def calcular():

    dados = request.json

    if "usuario_id" not in session:
        return jsonify({
            "erro": "Faça login."
        })

    resultado = calcular_energia(dados)

    novo_consumo = Consumo(

        usuario_id=session["usuario_id"],

        nome_aparelho=dados["nome"],

        watts=float(dados["watts"]),

        horas=float(dados["horas"]),

        dias=float(dados["dias"]),

        quantidade=int(dados["quantidade"]),

        tarifa=float(dados["tarifa"]),

        kwh=resultado["kwh"],

        preco=resultado["preco"]
    )

    db.session.add(novo_consumo)

    db.session.commit()

    ideias = gerar_ideias(resultado)

    resultado["ideias"] = ideias

    return jsonify(resultado)
@app.route("/usuario/<int:id>")
def usuario(id):

    if (not session.get("admin")and session["usuario_id"] != id):
        return redirect("/dashboard")

    usuario = Usuario.query.get_or_404(id)

    consumos = Consumo.query.filter_by(usuario_id=id).all()

    return render_template("usuario.html", usuario=usuario, consumos=consumos)
# ====================================
# INICIAR SITE
# ====================================


with app.app_context():
    db.create_all()
    print("BANCO CRIADO")
    print(db.engine.url)
if __name__ == "__main__":

    enviar_email(

        "sobrenomecleitan@gmail.com",

        "⚡ Neo Energy Online",

        "Servidor iniciado com sucesso."
    )
    port = int(os.environ.get("PORT", 5000))
    
    # IMPORTANTE: Remova o ssl_context="adhoc" no deploy do Render.
    # O Render já fornece HTTPS/SSL gratuitamente de forma automática.
    app.run(host="0.0.0.0", port=port)