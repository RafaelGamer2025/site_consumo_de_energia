import imaplib
import email
import time



def get_body(msg):
    """Extrai o texto do email"""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                return part.get_payload(decode=True).decode(errors="ignore")
    else:
        return msg.get_payload(decode=True).decode(errors="ignore")
    return ""

def gmail_bot():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, SENHA)
    mail.select("inbox")

    # pega quantidade inicial
    status, mensagens = mail.search(None, "ALL")
    ultimo_total = len(mensagens[0].split())

    print("Bot iniciado. Emails atuais:", ultimo_total)
    print("Aguardando novo email...\n")

    while True:
        time.sleep(10)  # verifica a cada 10 segundos

        status, mensagens = mail.search(None, "ALL")
        atual = len(mensagens[0].split())

        if atual > ultimo_total:
            print("📩 NOVO EMAIL DETECTADO!")
            novos = mensagens[0].split()[ultimo_total:]

            for i in novos:
                status, dados = mail.fetch(i, "(RFC822)")
                msg = email.message_from_bytes(dados[0][1])

                print("De:", msg["From"])
                print("Assunto:", msg["Subject"])
                print("Texto:")
                print(get_body(msg))
                print("-" * 50)

            ultimo_total = atual

gmail_bot()
