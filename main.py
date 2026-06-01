import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SITE_URL")

print("Acessando o site...")

resposta = requests.get(url)

if resposta.status_code == 200:
    print("Site acessado com sucesso!") 
else:
    print(f"Erro ao acessar o site. Status code: {resposta.status_code}")
    exit()

soup = BeautifulSoup(resposta.text, "html.parser")

links = soup.find_all("a") 

print("\nVagas de estágio encontradas no site (INDT):\n")

for link in links:
    texto =  link.get_text(strip=True)

    if "estágio" in texto.lower():
        print(f"Título: {texto}")
        print(f"Link: {link.get('href')}")
        print("-" * 50)
