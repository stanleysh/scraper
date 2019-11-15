import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def Skyscanner_scrape():
    print("Please paste skyscanner link: ")
    url = input()
    print("How many flights would you like to scrape?: ")
    num_flights = input()
    scraped_flights = []
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False) 
    driver =webdriver.Firefox(profile)
    driver.get(url)
    print(driver.title)
    assert "Skyscanner" in driver.title # Makes sure that the correct website has been loaded
    time.sleep(20)
    sort = driver.find_element_by_class_name("BpkSelect_bpk-select__32bku")
    sort.click()
    cheap = driver.find_element_by_xpath("//option[@value='CHEAPEST']")
    cheap.click()
    time.sleep(1)
    load_more = driver.find_element_by_css_selector("button[class='BpkButton_bpk-button__32HxR BpkButton_bpk-button--secondary__2UhGP']")
    load_more.click()
    links = driver.find_elements_by_class_name("FlightsTicket_link__kl4DL")
    while len(links) < int(num_flights):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        links = driver.find_elements_by_class_name("FlightsTicket_link__kl4DL")
        prices_list = driver.find_elements_by_css_selector("span[class='BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN BpkText_bpk-text--bold__4yauk']")
        times = driver.find_elements_by_css_selector("span[class='BpkText_bpk-text__2NHsO BpkText_bpk-text--base__2vfTl BpkText_bpk-text--bold__4yauk']")
        time.sleep(3)  
    prices = prices_list[3:]
    i = 0
    print(f'Number of times: {len(times)}')
    print(f'Number of links: {len(links)}')
    print(f'Number of prices: {len(prices)}')
    while i < int(num_flights):
        flight_info = {"origin_dep_time": times[i*4].text, "destination_arr_time": times[i*4+1].text, "destination_dep_time": times[i*4+2].text, "origin_arr_time": times[i*4+3].text, "price": prices[i].text, "link": links[i].get_attribute("href")}
        scraped_flights.append(flight_info)
        i += 1
    driver.close()
    return scraped_flights


flights = Skyscanner_scrape()

flights_data = pd.DataFrame(flights, columns = ['origin_dep_time', 'destination_arr_time', 'destination_dep_time', 'origin_arr_time', 'price', 'link'])
flights_data.index += 1

for i in range(1,flights_data['price'].count()+1):
    flights_data['price'][i] = flights_data['price'][i].replace('C$', '')
    flights_data['price'][i] = flights_data['price'][i].replace(',', '')
flights_data['price'] = flights_data['price'].astype(int)

price_stats = pd.DataFrame(flights_data['price'].describe()).transpose()
price_stats.head()

flights_data.to_csv("./flights_data.csv")
price_stats.to_csv("./price_stats.csv")