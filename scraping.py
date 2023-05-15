import sys
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor

def scrape_data(token):
    start_time = time.time()
    print("INFO ---------- Starting Time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))
    # token = input("Enter the token Please.")
    website_url = 'https://www.dextools.io/app/en/ether/pair-explorer/'
    if website_url in token:
        url = token
    else:
        url = website_url + token    

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--incognito")
    options.add_argument("--nogpu")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1280")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-javascript")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    ua = UserAgent()
    userAgent = ua.random
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})

    try:
        driver.get(url)
        ul_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//ul[@class='ng-tns-c101-6']")))
        text = ul_element.text

        match = re.search(r'Total Market Cap:\s*\$(\d+(\.\d+)?[0KMB])', text)
        if match:
            market_cap = match.group(1)
            print('Total Market Cap: $', market_cap)
            # return url, 'Total Market Cap: $' + market_cap
        else:
            print("Total Market Cap: $0")
            # return url, None
            market_cap = 0
    except Exception as e:
        print(f"Error occurred for URL {url} or Seems the given token is not correct")
        return url, None
    finally:
        driver.quit()
    
    end_time = time.time()
    print("INFO ---------- Ending Time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
    duration = end_time - start_time
    print("Execution Time (in seconds):", duration)
    print("Execution Time (in minutes):", duration / 60)
    return market_cap



def extractValue(fName):
    token_list = open(fName, "r").read().splitlines()

    start_time = time.time()
    print("INFO ---------- Starting Time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for token in token_list:
            url = f'https://www.dextools.io/app/en/ether/pair-explorer/{token}'
            futures.append(executor.submit(scrape_data, url))

        market_value = {}
        for future in futures:
            url, result = future.result()
            if result:
                market_value[url] = result

    print(market_value)
    print("Total URLs processed:", len(market_value))

    end_time = time.time()
    print("INFO ---------- Ending Time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))

    duration = end_time - start_time
    print("Execution Time (in seconds):", duration)
    print("Execution Time (in minutes):", duration / 60)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Parameter is required to run this file")
    else:
        parameter = sys.argv[1]
        # Use the 'parameter' variable to process the URL as required
        scrape_data(parameter)