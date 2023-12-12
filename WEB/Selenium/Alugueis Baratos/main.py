from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests, time

LINK_GOOGLEFORMS = 'https://docs.google.com/forms/d/e/1FAIpQLSfWJcPIdDl0W28bS_gDkISSc7D5aAwGYxr7x367otz9uk4plg/viewform?usp=sf_link'
LINK_DEFAULT = 'https://www.vivareal.com.br/aluguel/sp/osasco/1-quarto/#onde=Brasil,S%C3%A3o%20Paulo,Osasco,,,,,,BR%3ESao%20Paulo%3ENULL%3EOsasco,,,&preco-ate=3000&quartos=1'

url = input("Digite o url da sua consulta na vivareal: ")
if url == 'default':
    url = LINK_DEFAULT

html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')
links = [f"www.vivareal.com.br{link.get('href')}" for link in soup.find_all(name='a', class_='js-main-info')]
prices = [div.contents[1].text[:div.contents[1].text.find('/')].strip(" ") for div in soup.find_all(name='div', class_='property-card__price')]
adresses = [adress.text for adress in soup.find_all(name='span', class_='property-card__address')]

driver = webdriver.Chrome()
driver.get(LINK_GOOGLEFORMS)
wait = WebDriverWait(driver, 100)

for i in range(len(links)):
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(adresses[i])
    driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(prices[i])
    driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(links[i])
    driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div').click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')))
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()