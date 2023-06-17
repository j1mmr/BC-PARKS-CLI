from selenium import webdriver
import time

driver = webdriver.Firefox()

driver.get(r"https://camping.bcparks.ca/create-booking/results?startDate=2023-06-23&endDate=2023-06-25&nights=2&isReserving=true&filterData=%7B%7D&searchTime=2023-06-14T16:50:25.419&mapId=-2147483552&searchTabGroupId=0&bookingCategoryId=0&equipmentId=-32768&subEquipmentId=-32768&partySize=1&equipmentCapacity=1")

print("Page Title:", driver.title)

list_button = driver.find_element_by_xpath('//*[@id="list-view-button"]')
list_button.click()

time.sleep(10)
# Close the browser
driver.quit()