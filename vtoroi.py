from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pandas as pd
import re
import time

# Запускаем браузер и переходим на сайт coinmarketcap.com
driver = webdriver.Chrome()
driver.get('https://coinmarketcap.com/ru/')

# Ищем все таблицы на странице
tables = driver.find_elements(By.XPATH, "//table")

# Создаем пустой список для хранения данных
data = []
name_krp_sps = []
price_krp_sps = []
capit_100 = 0
capital = []
# Перебираем все таблицы на странице
for table in tables:
    # Извлекаем данные из каждой строки таблицы
    rows = table.find_elements(By.XPATH, ".//tr")
    for row in rows:
        cols = row.find_elements(By.XPATH, ".//td")
        # Если в строке есть данные, добавляем их в список
        if len(cols) > 0:
            #Находим из всего сайта нужные нам данные
            name_col = cols[2].text
            capitalization_col = cols[7].text
            #print(name_col, capitalization_col)
            
            
            ##Ставим запятые после каждых 3-ех символов
            #cap2 = f"{cap2:s}"
            #добавляем значения в другой списко в другой список
            name_krp_sps.append(name_col.replace('\n', ''))
            price_krp_sps.append(capitalization_col)
            #data_row = [name_col, cap2]
            #data.append(data_row)
            #Удаляем знак рубля
            cap2 = capitalization_col[1:]
            #Удаляем запятые и приводим к целочисленному значению для сложения
            cap2 = re.sub(',', '', cap2)
            int_cap = int(cap2)
            capit_100 += int_cap
            capital.append(int_cap)
            #print(capit_100)

proc_capital100 = []
for i in capital:
    percent = (i / capit_100 * 100)
    if percent > 1:
        proc_capital100.append(round(percent, 1))
    elif round(percent) == 0:
        proc_capital100.append(round(percent * 100, 1))

for name, price, cap in zip(name_krp_sps, price_krp_sps, proc_capital100):
    zipp = [name, price, cap, ' %']
    data.append(zipp)
       
current_time = time.strftime("%H.%M") + " " + datetime.now().strftime("%d.%m.%Y")
# Преобразуем список в DataFrame
df = pd.DataFrame(data, columns=['Name', 'Market Capitalization', 'Procent 100 cap', 'Procent'])

# Сохраняем DataFrame в CSV файл
df.to_csv('{}.csv'.format(current_time), index=False)

# Закрываем браузер
driver.quit()