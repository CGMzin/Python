from bs4 import BeautifulSoup
import requests

response = requests.get("https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")
html = response.text

soup = BeautifulSoup(html, "html5lib")
    
titles = [title.getText() for title in soup.find_all(name="h3", class_="title")]
titles.reverse()

with open("./filmes.txt", mode="w", encoding="utf-8") as file:
    for title in titles:
        file.write(f"{title}\n")
