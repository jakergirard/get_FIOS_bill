from selenium import webdriver
from getpass import getpass
##Logging in to Verizon FIOS
username = input("Enter user: ")
password = getpass("Enter password: ")


driver = webdriver.Chrome("/Users/dbelle/Documents/dbelle_scripts/get_FIOS_bill/chromedriver")
driver.get("https://secure.verizon.com/vzauth/UI/Login")

driver.implicitly_wait(5)

username_textbox = driver.find_element_by_id("IDToken1")
username_textbox.send_keys(username)

password_textbox = driver.find_element_by_id("IDToken2")
password_textbox.send_keys(password)

login_button = driver.find_element_by_id("login-submit")
login_button.submit()

view_bill = driver.find_element_by_partial_link_text("View Bill Detail")
view_bill.click()

download = driver.find_element_by_partial_link_text("Download PDF")
download.click()
