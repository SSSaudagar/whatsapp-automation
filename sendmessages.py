from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import csv
import datetime
import os
import urllib.parse
import pyperclip
try:
    import autoit
except ModuleNotFoundError:
    pass

message = "Dear @fname@ @lname@,\n\nTransform passion into a profession.👨🎓\n\nHelp your child make the right career choice by discovering their true talents and strengths. 💪💯\n\nOur AI-based career guidance test helps determine your career path based on your personality and aptitude. 📝😎\n\nTake our FREE career test today on - \n\n\n\nOr reach out to us on - "
media = False
attachment = False
contactCard = False
driver = None
variables = {
    'lname'     : 0,
    'name'      : 1,
    'fname'     : 2,
    'num'       : 3,
    'dist'      : 4
}


def getContactsList():
    with open('contacts.csv') as f:
        reader = csv.reader(f)
        contacts = list(reader)
    print(str(len(contacts))+" have been imported")
    print(contacts[:5])
    input("Please press enter key to continue")
    return contacts

def whatsappLogin():
    global driver, wait
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=./User_Data')
    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    driver.get("https://web.whatsapp.com/")
    input('Enter anything after scanning QR code')

def sendMessaage(contact):
    global driver,message,variables
    driver.get("https://web.whatsapp.com/send?phone=91{}&text&source&data&app_absent".format(contact['num']))
    inp_xpath = "//*[@id=\"main\"]/footer/div[1]/div[2]/div/div[2]"
    msg = message
    for key in variables:
        msg = msg.replace("@"+key+"@", contact[key])
    pyperclip.copy(msg)
    try:
        input_box = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.XPATH, inp_xpath)))
        time.sleep(1)
        input_box.click()
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.INSERT).key_up(Keys.INSERT).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
        input_box.send_keys(Keys.ENTER)
        time.sleep(3)
        return True
    except:
        try:
            inp_xpath1 = "//*[@id=\"app\"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div"
            popup = driver.find_element_by_xpath(inp_xpath1)
            contact['failed'] = "Contact not on WhatsApp"
        except:
            contact['failed'] = "Unknown error. Please try sending again"
        time.sleep(3)
        return False
    

def sender(contacts):
    global variables
    with open('invalid.csv','w+') as invalid:
        invWriter = csv.writer(invalid)
        valid = []
        for i in range(len(contacts)):
            print('Processing {} of {} contacts'.format(i+1,len(contacts)))
            contact = {}
            for key in variables:
                contact[key] = contacts[i][variables[key]]
            if contact['num'] in valid:
                contact['failed']= 'Messaage already sent in this campaign'
                invWriter.writerow(contact.values())
                continue
            if not sendMessaage(contact):
                invWriter.writerow(contact.values())
            else:
                valid.append(contact['num'])
        

def sendContact(contact):
    clipButton = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)
    contactButton = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[4]/button')
    contactButton.click()
    searchInput = driver.find_element_by_xpath('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[1]/div/label/div/div[2]')
    searchInput.click()
    searchInput.send_keys(contact)
    time.sleep(1)
    x_arg = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div[1]/div/div/div[2]'
    contactTitle = driver.find_element_by_xpath(x_arg)
    contactTitle.click()
    time.sleep(1)
    sendButton = driver.find_element_by_xpath('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/span/div/div/div')
    sendButton.click()
    time.sleep(1)
    sendButton2 = driver.find_element_by_xpath('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div')
    sendButton2.click()

def sendMedia(filename): #onlyForWindows
    clipButton = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)
    mediaButton = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button')
    mediaButton.click()
    image = os.getcwd() + "\\Media\\" + filename
    autoit.control_focus("Open", "Edit1")
    autoit.control_set_text("Open", "Edit1", image)
    autoit.control_click("Open", "Button1")
    time.sleep(3)
    sendButton = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div/span')
    sendButton.click()
    

contacts = getContactsList()
whatsappLogin()
sender(contacts)
driver.quit()




