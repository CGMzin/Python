from bs4 import BeautifulSoup
import requests

url = "https://produto.mercadolivre.com.br/MLB-1883364100-teclado-gamer-semi-mecanico-barato-iluminado-rgb-em-ptbr-_JM#position=32&search_layout=grid&type=item&tracking_id=106ab534-4ddb-4970-9603-b2a5ed0fb535"

header = {
    "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0",
    "sec-ch-ua": '"Opera GX";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

response_amazon = requests.get(url, headers=header)
soup = BeautifulSoup(response_amazon.content, "html.parser")
print(soup.prettify())
