from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/")
html = response.text

soup = BeautifulSoup(html, "html5lib")
    
links = [link.contents[0].get("href") for link in soup.find_all(name="span", class_="titleline")]
text = [link.getText() for link in soup.find_all(name="span", class_="titleline")]
votes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

index = votes.index(max(votes))

print(links[index])
print(text[index])
print(votes[index])