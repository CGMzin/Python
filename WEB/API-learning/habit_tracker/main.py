import requests
from datetime import datetime

USERNAME = "cgm"
TOKEN = "ponawodhaufgawpun"

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME, #https://pixe.la/@cgm
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

""" response = requests.post(url=pixela_endpoint, json=user_params)
print(response.text) """

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_params = {
    "id": "estudos",
    "name": "Tabela de Estudos",
    "unit": "hours",
    "type": "float",
    "color": "ajisai",
}

headers = {
    "X-USER-TOKEN": TOKEN
}

""" response = requests.post(url=graph_endpoint, json=graph_params, headers=headers)
print(response) """

post_endpoint = f"{graph_endpoint}/estudos"

today = datetime.now()
post_body = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "2.5"
}

response = requests.post(url=post_endpoint, json=post_body, headers=headers)
print(response.text)