import os
import time
import platform
import sys
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from getpass import getpass
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def main():

# Detect the current platform
    current_platform = platform.system()

    # Set up Chrome options
    options = webdriver.ChromeOptions()

    if current_platform == 'Linux':
        # Set up headless mode for Linux (Ubuntu server)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    # Set download directory depending on the platform
    download_directory = "/home/dbelle/Downloads" if current_platform == 'Linux' else "/Users/dbelle/Downloads"

    prefs = {"download.default_directory" : download_directory}
    options.add_experimental_option("prefs",prefs)

    chromedriver_path = '/usr/local/bin/chromedriver' if current_platform == 'Linux' else '/Users/dbelle/Documents/dbelle_scripts/get_FIOS_bill/chromedriver'

    # Initialize the webdriver with the new syntax
    #driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=options)

    # Delete file if it already exists
    pdf_path = "/home/dbelle/Downloads/paper-bill.pdf" if current_platform == 'Linux' else "/Users/dbelle/Downloads/paper-bill.pdf"
    try:
        os.remove(pdf_path)
    except OSError:
        pass

    # Auth using env variables
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    password_email = os.environ.get('PASSWORD_EMAIL')
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    secret_question_answer = os.environ.get('SECRET_QUESTION')
    sender_email = "tt5775030@gmail.com"


    driver.get("https://secure.verizon.com/vzauth/UI/Login")

driver.implicitly_wait(5)
###Login
username_textbox = driver.find_element(By.ID, "IDToken1")
username_textbox.send_keys(username)

login_button = driver.find_element(By.ID, "continueBtn")
login_button.click()

password_textbox = driver.find_element(By.ID, "IDToken2")
password_textbox.send_keys(password)

login_button = driver.find_element(By.ID, "continueBtn")
login_button.click()

### Challenge Question
# def check_exists_by_xpath(xpath):
#     try:
#         driver.find_element(By.XPATH, xpath)
#     except NoSuchElementException:
#         return False
#     return True
#
#
# if check_exists_by_xpath("//input[@id='IDToken1']"):
#     secret_question = driver.find_element(By.ID, "IDToken1")
#     secret_question.send_keys(secret_question_answer)
#     continue_button = driver.find_element(By.ID, "otherButton")
#     continue_button.submit()

    driver.implicitly_wait(20)

    view_bill = driver.find_element(By.PARTIAL_LINK_TEXT, "View Bill Detail")
    view_bill.click()

    # Wait for the download link to become clickable
    wait = WebDriverWait(driver, 10)
    download_link_text = "Download PDF"  # adjust as needed
    download = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, download_link_text)))

    # Scroll the download link into view and click it
    driver.execute_script("arguments[0].scrollIntoView();", download)
    time.sleep(1)  # Wait for 1 second
    download.click()

    time.sleep(5)  # Sleep for 3 seconds

    driver.close()

    # Create a secure SSL context
    subject = "An email with attachment from Python"
    body = "This is an email with attachment sent from Python"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    #filename = "/Users/dbelle/Downloads/paper-bill.pdf"  # In same directory as script
    filename = "/home/dbelle/Downloads/paper-bill.pdf" if current_platform == 'Linux' else "/Users/dbelle/Downloads/paper-bill.pdf"

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, text)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
