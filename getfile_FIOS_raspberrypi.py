from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from getpass import getpass
import smtplib,email,email.encoders,email.mime.text,email.mime.base
#import smtplib, ssl
#from email import encoders
#from email.mime.base import MIMEBase
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMETexti
from pyvirtualdisplay import Display
import time
import os

#Delete file if it already exists
#try:
#    os.remove('/home/dbelle')
#except OSError:
#    pass

#Auth using env variables
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
password_email = os.environ.get('PASSWORD_EMAIL')


chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',chrome_options=chrome_options)
driver.get('https://secure.verizon.com/vzauth/UI/Login')

driver.implicitly_wait(5)

username_textbox = driver.find_element_by_id("IDToken1")
username_textbox.send_keys(username)

password_textbox = driver.find_element_by_id("IDToken2")
password_textbox.send_keys(password)

login_button = driver.find_element_by_id("login-submit")
login_button.submit()

#Challenge Question
secret_question = driver.find_element_by_id("IDToken1")
secret_question.send_keys("Trinidad")

continue_button = driver.find_element_by_id("otherButton")
continue_button.submit()

view_bill = driver.find_element_by_link_text("View Bill Details")
view_bill.click()

download = driver.find_element_by_partial_link_text("Download PDF")
download.click()

time.sleep(5) # Sleep for 3 seconds

driver.close()
