import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = Chrome(options=chrome_options)

url = "https://www.pararius.com/apartments/amsterdam/"
driver.get(url)
time.sleep(5)

title = driver.find_element(by=By.CLASS_NAME, value="page__content")
print(title)

