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
import argparse
try:
    import autoit
except ModuleNotFoundError:
    pass

parser = argparse.ArgumentParser(description='Cybertrom WhatsApp Automation Guide')
parser.add_argument('--chrome_driver_path', action='store', type=str, default='./chromedriver', help='chromedriver executable path (MAC and Windows path would be different)')
parser.add_argument('--remove_cache', action='store_true', help='Remove Cache | Scan QR again or Not')
parser.add_argument('--test', action='store_true', help='Send message to test contacts')
parser.add_argument('--login',action='store_true', help='Log in to whatsapp')
args = parser.parse_args()

if args.remove_cache:
    os.system('rm -rf User_Data/*')

driver = None
_user_data = './User_Data'
valid = []

def getContactsList(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        contacts = list(reader)
    return contacts

def startBrowser(headless = True):
    global driver,args
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir='+_user_data)
    if headless: chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(executable_path=args.chrome_driver_path, options=chrome_options)
    return

def stopBrowser():
    global driver
    driver.quit()
    return

def whatsappLogin():
    startBrowser(False)
    driver.get("https://web.whatsapp.com/")
    return

def sendContact(contact):
    global driver
    clip_button = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clip_button.click()
    time.sleep(1)
    contact_button = driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[4]/button')
    contact_button.click()
    search_input = driver.find_element_by_xpath('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[1]/div/label/div/div[2]')
    search_input.click()
    search_input.send_keys(contact)
    time.sleep(1)
    x_arg = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div[1]/div/div/div[2]'
    contact_title = driver.find_element_by_xpath(x_arg)
    contact_title.click()
    time.sleep(1)
    send_button = driver.find_element_by_xpath('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/span/div/div/div')
    send_button.click()
    time.sleep(1)
    send_button2 = driver.find_element_by_xpath('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div')
    send_button2.click()
    time.sleep(1)

def sendMessage(recipient,message,contact):
    global driver
    driver.get("https://web.whatsapp.com/send?phone=91{}&text&source&data&app_absent".format(recipient['num']))
    inp_xpath = "//*[@id=\"main\"]/footer/div[1]/div[2]/div/div[2]"
    msg = message
    for key in recipient:
        msg = msg.replace("@"+key+"@", recipient[key])
    pyperclip.copy(msg)
    try:
        input_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, inp_xpath)))
        time.sleep(1)
        input_box.click()
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.INSERT).key_up(Keys.INSERT).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        if contact: sendContact(contact)
        return True
    except:
        try:
            inp_xpath1 = "//*[@id=\"app\"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div"
            popup = driver.find_element_by_xpath(inp_xpath1)
            recipient['failed'] = "Contact not on WhatsApp"
        except:
            recipient['failed'] = "Unknown error. Please try sending again"
        time.sleep(3)
        return False
    return

def sender(filename,variables,message):
    global valid,args
    if isinstance(message,str):
        text = message
        contact = None
    else:
        text = message['text']
        contact = message['contact']
    recipients = getContactsList(filename)
    startBrowser()
    with open('Invalid/'+filename.replace('.csv','.invalid.csv'),'w+') as invalid:
        invWriter = csv.writer(invalid)
        for i in range(len(recipients)):
            print('Processing {} of {} contacts'.format(i+1,len(recipients)))
            recipient = {}
            for key in variables:
                recipient[key] = recipients[i][variables[key]]
            if recipient['num'] in valid:
                recipient['failed']= 'Messaage already sent in this campaign'
                invWriter.writerow(recipient.values())
                continue
            if not sendMessage(recipient,text,contact):
                invWriter.writerow(recipient.values())
            else:
                if not args.test: valid.append(recipient['num'])
    stopBrowser()
    return
    
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
    
if __name__ == "__main__":
    if args.login:
        whatsappLogin()
        input("Press Enter to exit")
        stopBrowser()



