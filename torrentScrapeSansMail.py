
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.headless = True
options.add_argument("--window-size=1920,3000")

driverPath = "/Users/tom_planche/Desktop/Prog/Python/chromedriver"

driver = webdriver.Chrome(driverPath, options = options)


site = "https://www.torrentmac.net"
driver.get(site)

soupe = BeautifulSoup(driver.page_source, 'html.parser')

liens_articles = [h2.find('a')['href'] for h2 in soupe.find_all('h2', class_ = 'post-title')]

for article in liens_articles:
    driver.get(article)
    soupe_article = BeautifulSoup(driver.page_source, 'html.parser')

    titre_article = driver.find_element_by_xpath('//*[@id="main"]/article/header/h1').text
    date_article = driver.find_element_by_xpath('//*[@id="main"]/article/header/p/time').text
    categorie_article = [elem.text for elem in soupe_article.find('p', class_ = 'meta post-info').find_all('a')]
    image_article = soupe_article.find('div', class_ = 'feature-img').find('img')['src']
    taille_article = soupe_article.find('table', class_ = 'torrentInfoTable').find_all('td')[1].text
    description_article = soupe_article.find('section', class_ = 'post_content clearfix').find('p').text

    print(f"{titre_article}\n"
          f"Posté le {date_article} et a pour catégories {categorie_article}\n"
          f"{description_article}\n"
          f"Taille : {taille_article}\n"
          f"lien : {article}")
    print()

