import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def Skyscanner_scrape(url_link):
    scraped_flights = {}
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False) 
    driver =webdriver.Firefox(profile)
    driver.get(url_link)
    print(driver.title)
    assert "Skyscanner" in driver.title # Makes sure that the correct website has been loaded
    time.sleep(10)
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
    return scraped_flights


flights = Skyscanner_scrape("https://www.skyscanner.ca/transport/flights/sfo/tyoa/191118/191125/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home#/")

for num, value in flights.items():
    print(num, value)

data = pd.DataFrame.from_dict(flights, orient='index')
data.to_csv(".data.csv")