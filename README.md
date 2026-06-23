# Monitor de Vagas

Projeto em Python para monitorar vagas de estágio em um site, identificar novas oportunidades e enviar um alerta por e-mail automaticamente.

## Sobre o projeto

Este projeto automatiza a busca por vagas de estágio.

O programa acessa uma página de vagas, interpreta o HTML, filtra links relacionados a estágio, compara os resultados com um histórico local e envia um e-mail quando encontra uma vaga nova.

## Tecnologias utilizadas

- Python
- Requests
- BeautifulSoup
- python-dotenv
- JSON
- SMTP com `smtplib`
- Git e GitHub

## Como funciona

1. Carrega as configurações do arquivo `.env`.
2. Acessa o site configurado em `SITE_URL`.
3. Lê o HTML da página com BeautifulSoup.
4. Procura links que contenham a palavra `estágio`.
5. Normaliza o texto para reconhecer `estágio` e `estagio`.
6. Compara as vagas encontradas com o histórico salvo em `vagas_encontradas.json`.
7. Se encontrar uma vaga nova, envia um e-mail.
8. Salva a nova vaga no histórico para evitar notificações repetidas.

## Estrutura do projeto

```text
Confere vagas/
├── main.py
├── executar_monitor.bat
├── vagas_encontradas.json
├── .env
├── .gitignore
└── README.md
