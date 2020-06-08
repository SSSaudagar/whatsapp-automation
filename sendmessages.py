from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv

# contacts = [
#     [
#         '1234567890', 'Srushti'
#     ],
#     [
#         '1234567891', 'Shashank' 
#     ],
#     [
#         '1234567892', 'Prasad'
#     ],
#     [
#         '1234567893', 'Sudhir'
#     ]
# ]

invalid = []
string = "This is a python generated message. this is test message. @name@ your number is @num@."
driver = webdriver.Chrome('./chromedriver')
driver.get("https://web.whatsapp.com/")
input('Enter anything after scanning QR code')

wait = WebDriverWait(driver, 10)
inp_xpath = "//*[@id=\"main\"]/footer/div[1]/div[2]/div/div[2]"

for contact in contacts:
    driver.get("https://web.whatsapp.com/send?phone=91"+contact[0])
    try:
        input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
        input_box.send_keys(string.replace("@name@",contact[1]).replace("@num@",contact[0])+Keys.ENTER)
        time.sleep(3)
        continue
    except:
        try:
            wait1 = WebDriverWait(driver, 10)
            inp_xpath1 = "//*[@id=\"app\"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div"
            wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath1)))
            print(contact[1]+" Not available on whatsapp")
            invalid.append(contact)
            continue
        except:
            print("Something went wrong")

print("invalid contacts")
print(invalid)
driver.quit()




