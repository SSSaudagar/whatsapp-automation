from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv
import urllib.parse

with open('contacts.csv') as f:
    reader = csv.reader(f)
    contacts = list(reader)

invalid = []
string = "Dear @fname@ @lname@,\nDreams have no limits!\nDon\'t limit your child\'s ambitions to medicine or engineering. Help them discover their true passion!\nPlan your child\'s successful career with us.\nVisit us on https://www.mysmartmove.in?campaign=whatsapp-1&phone=@num@ or reach us on Whatsapp."
driver = webdriver.Chrome('./chromedriver')
driver.get("https://web.whatsapp.com/")
input('Enter anything after scanning QR code')

wait = WebDriverWait(driver, 10)
inp_xpath = "//*[@id=\"main\"]/footer/div[1]/div[2]/div/div[2]"
i=1
for contact in contacts:
    print('sending '+str(i)+' of '+str(len(contacts)))
    i+=1
    driver.get("https://web.whatsapp.com/send?phone=91"+contact[3]+"&text="+urllib.parse.quote(string.replace("@fname@",contact[2]).replace("@lname@",contact[0]).replace("@num@",contact[3])))
    try:
        input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
        input_box.send_keys(Keys.ENTER)
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
            invalid.append(contact)

print("invalid contacts")
print(invalid)
driver.quit()




