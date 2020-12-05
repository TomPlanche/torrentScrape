
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.headless = True
options.add_argument("--window-size=1920,3000")

driverPath = "path_to/chromedriver"

driver = webdriver.Chrome(driverPath, options = options)


site = "https://www.torrentmac.net"
driver.get(site)

soupe = BeautifulSoup(driver.page_source, 'html.parser')

# articles links
liens_articles = [h2.find('a')['href'] for h2 in soupe.find_all('h2', class_ = 'post-title')]

for article in liens_articles:
    driver.get(article)
    soupe_article = BeautifulSoup(driver.page_source, 'html.parser')
    # title
    titre_article = driver.find_element_by_xpath('//*[@id="main"]/article/header/h1').text
    date_article = driver.find_element_by_xpath('//*[@id="main"]/article/header/p/time').text
    categorie_article = [elem.text for elem in soupe_article.find('p', class_ = 'meta post-info').find_all('a')]
    image_article = soupe_article.find('div', class_ = 'feature-img').find('img')['src']
    # size of the article
    taille_article = soupe_article.find('table', class_ = 'torrentInfoTable').find_all('td')[1].text
    description_article = soupe_article.find('section', class_ = 'post_content clearfix').find('p').text

    print(f"{titre_article}\n"
          f"Post on {date_article} in categories : {categorie_article}\n"
          f"{description_article}\n"
          f"File size : {taille_article}\n"
          f"Link : {article}")
    print()
