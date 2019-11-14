import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def Skyscanner_scrape():
    print("Please paste skyscanner link: ")
    url = input()
    scraped_flights = {}
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
    times = driver.find_elements_by_css_selector("span[class='BpkText_bpk-text__2NHsO BpkText_bpk-text--base__2vfTl BpkText_bpk-text--bold__4yauk']")
    total_time = driver.find_elements_by_css_selector("span[class='BpkText_bpk-text__2NHsO BpkText_bpk-text--sm__345aT Duration_duration__1QA_S]")
    links = driver.find_elements_by_class_name("FlightsTicket_link__kl4DL")
    prices_list = driver.find_elements_by_css_selector("span[class='BpkText_bpk-text__2NHsO BpkText_bpk-text--lg__3vAKN BpkText_bpk-text--bold__4yauk']")
    prices = prices_list[3:]
    i = 0
    while i < len(prices):
        flight_info = {"origin_dep_time": times[i*4].text, "destination_arr_time": times[i*4+1].text, "destination_dep_time": times[i*4+2].text, "origin_arr_time": times[i*4+3].text, "price": prices[i].text, "link": links[i].get_attribute("href")}
        scraped_flights[i+1] = flight_info
        i += 1
    driver.close()
    return scraped_flights


flights = Skyscanner_scrape()

for num, value in flights.items():
    print(num, value)

data = pd.DataFrame.from_dict(flights, orient='index')
data.to_csv("./data.csv")