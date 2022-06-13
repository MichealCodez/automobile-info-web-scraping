from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


opt = webdriver.ChromeOptions()
opt.add_argument("--enable-javascript")
opt.add_argument('--profile-directory=Default')
opt.add_argument("--incognito")
opt.add_argument("--disable-plugins-discovery")
opt.add_argument("--start-maximized")
opt.add_argument('--ignore-certificate-errors')
opt.add_argument('--allow-running-insecure-content')
opt.add_argument("--disable-extensions")
opt.add_argument("--proxy-server='direct://'")
opt.add_argument("--proxy-bypass-list=*")
opt.add_argument('--disable-dev-shm-usage')
opt.add_argument('--no-sandbox')
opt.add_argument('--disable-blink-features=AutomationControlled')
opt.add_argument('--disable-blink-features=AutomationControlled')
opt.add_experimental_option('useAutomationExtension', False)
opt.add_experimental_option("excludeSwitches", ["enable-automation"])
opt.add_argument("disable-infobars")
opt.add_argument('--single-process')


def presshold():
    try:
        press_hold = driver.find_element(By.CSS_SELECTOR, '#px-captcha')
        while press_hold:
            action = ActionChains(driver)
            action.click_and_hold(press_hold)
            action.perform()
            time.sleep(15)
            action.release(press_hold)
            action.perform()
            time.sleep(0.2)
            action.release(press_hold)
            time.sleep(5)
            press_hold = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, '#px-captcha')))
    except:
        pass


old_data = pd.read_csv("old_data.csv")
search_list = old_data['part_number'].tolist()
manufact = old_data['manufacturer'].tolist()
data = {
    'part_number': old_data['part_number'].tolist()[0:12],
    'manufacturer': old_data['manufacturer'].tolist()[0:12],
    'Scraped Part': [' ', '15-24-7161', '22-05-7065', '22-12-2024', '22-17-3082', '22-27-2041', '7010326660',
                     '22-28-0031', '22-28-4020', '39-28-1083', '39-29-9042', '30700-1147'],
    'Also known as': [' ', '15247161', ' ', '22122024', ' ', ' ', ' ', '22280031', '22284020', '39281083', '39299042',
                      '307001147'],
    'Median Price': [' ', 'USD 2.470', 'USD 0.193', 'USD 0.240', 'USD 0.860', 'USD 0.193', 'USD 1.614', 'USD 0.299',
                     'USD 0.046', 'USD 0.463', 'USD 0.330', 'USD 1.300'],
    'Match': ['FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE']
}

for i in search_list[12::]:
    driver = webdriver.Chrome(options=opt)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

    driver.get('https://octopart.com/')
    print()
    time.sleep(2)
    search = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="search"]')))
    search.send_keys(i)
    search.send_keys(Keys.ENTER)
    time.sleep(2)
    presshold()
    try:
        button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[1]')
        if button:
            """
            scraped_part = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/'
                                                         'div[1]/div/a')
            scraped_part.click()
            """
            presshold()
            scraped_part = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/'
                                                          'div[1]/div/a/div[2]/span/span'))).text
            amount = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/'
                                                   'div[1]/div[1]/div/div/span[2]').text
            currency = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/'
                                                     'div[2]/div[1]/div[1]/div/div/span[1]').text
            price = f'{currency} {amount}'
            """
            aka = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[2]/div/div/div[1]/div[1]/div/div[1]/span[2]/mark')
            if not aka:
                aka = ' '
            else:
                aka = aka.text
            """
            presshold()
            data['part_number'].append(i)
            data['manufacturer'].append(manufact[search_list.index(i)])
            data['Scraped Part'].append(scraped_part)
            data['Also known as'].append(i)
            data['Median Price'].append(price)
            data['Match'].append('FALSE')
            df = pd.DataFrame(data)

            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter('new_data.xlsx', engine='xlsxwriter')

            # Convert the dataframe to an XlsxWriter Excel object.
            df.to_excel(writer, sheet_name='Sheet1', index=False)

            # Close the Pandas Excel writer and output the Excel file.
            writer.save()
            # driver.close()
            driver.get('chrome://settings/clearBrowserData')
        else:
            data['part_number'].append(i)
            data['manufacturer'].append(manufact[search_list.index(i)])
            data['Scraped Part'].append(' ')
            data['Also known as'].append(' ')
            data['Median Price'].append(' ')
            data['Match'].append(' ')
            df = pd.DataFrame(data)

            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter('new_data.xlsx', engine='xlsxwriter')

            # Convert the dataframe to an XlsxWriter Excel object.
            df.to_excel(writer, sheet_name='Sheet1', index=False)

            # Close the Pandas Excel writer and output the Excel file.
            writer.save()
            # driver.close()
            driver.get('chrome://settings/clearBrowserData')
    except:
        pass
