import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://www.justonecookbook.com/recipes/'
# response = requests.get(url)

driver = webdriver.Chrome()
driver.get(url)
driver.find_element

# Close out of button if it pops up
try:
    driver.find_element(By.CLASS_NAME, 'inwood-CloseButton').click()
except:
    pass

recipes = driver.find_elements(By.CLASS_NAME, 'post-filter')

driver.quit()

for recipe in recipes:
    print(recipe.text)

# soup = BeautifulSoup(response.text, 'html.parser')
# print('hello')
# recipes = soup.find_all('article', {'class': 'post-filter'})


# for recipe in recipes:
#     title = recipe.find('h3').text
#     img = recipe.find('img')['src']
#     link = recipe.find('h3').find('a')['href']
#     print(title, img, link)