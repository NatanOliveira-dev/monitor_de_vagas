import os
import json
import smtplib
import requests
import unicodedata

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.mime.text import MIMEText
from urllib.parse import urljoin


load_dotenv()

SITE_URL = os.getenv("SITE_URL")
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")

ARQUIVO_VAGAS = "vagas_encontradas.json"


def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")


def carregar_vagas_salvas():
    try:
        with open(ARQUIVO_VAGAS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []


def salvar_vagas(vagas):
    with open(ARQUIVO_VAGAS, "w", encoding="utf-8") as arquivo:
        json.dump(vagas, arquivo, indent=4, ensure_ascii=False)


def enviar_email(titulo, link):
    print("Enviando e-mail...")

    mensagem = MIMEText(
        f"Nova vaga encontrada:\n\nTítulo: {titulo}\nLink: {link}",
        "plain",
        "utf-8"
    )

    mensagem["Subject"] = "Nova vaga de estágio encontrada!"
    mensagem["From"] = EMAIL_REMETENTE
    mensagem["To"] = EMAIL_DESTINO

    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
        servidor.send_message(mensagem)

    print("E-mail enviado com sucesso!")


def buscar_vagas():
    print("Acessando o site...")

    resposta = requests.get(SITE_URL)

    if resposta.status_code != 200:
        print("Erro ao acessar o site.")
        return []

    print("Site acessado com sucesso!")

    soup = BeautifulSoup(resposta.content, "html.parser")
    links = soup.find_all("a")

    vagas = []

    for link in links:
        titulo = link.get_text(strip=True)
        url_vaga = link.get("href")

        if not titulo or not url_vaga:
            continue

        if "estagio" in normalizar_texto(titulo):
            vaga = {
                "titulo": titulo,
                "link": urljoin(SITE_URL, url_vaga)
            }

            vagas.append(vaga)

    return vagas


def main():
    vagas_salvas = carregar_vagas_salvas()
    vagas_encontradas = buscar_vagas()

    links_salvos = []

    for vaga in vagas_salvas:
        links_salvos.append(vaga["link"])

    for vaga in vagas_encontradas:
        if vaga["link"] not in links_salvos:
            print("\nNova vaga encontrada!")
            print("Título:", vaga["titulo"])
            print("Link:", vaga["link"])

            enviar_email(vaga["titulo"], vaga["link"])
            vagas_salvas.append(vaga)

    salvar_vagas(vagas_salvas)
    print("\nVerificação finalizada.")


main()
