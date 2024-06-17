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
    # Set variables
    username_pc = ''
    username_fios = ''
    password_fios = ''
    secret_question_answer_fios = ''
    receiver_email = ''
    sender_email = ''
    password_email = ''    
    
    # Detect the current platform
    current_platform = platform.system()

    # Set up Chrome options
    options = Options()

    if current_platform == 'Linux':
        # Set up headless mode for Linux (Ubuntu server)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    # Set download directory depending on the platform
    download_directory = f"/home/{username_pc}/Downloads" if current_platform == 'Linux' else f"/Users/{username_pc}/Downloads"

    prefs = {"download.default_directory": download_directory}
    options.add_experimental_option("prefs", prefs)

    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=options)
    
    # Delete file if it already exists
    pdf_path = f"/home/{username_pc}/Downloads/paper-bill.pdf" if current_platform == 'Linux' else f"/Users/{username_pc}/Downloads/paper-bill.pdf"
    try:
        os.remove(pdf_path)
    except OSError:
        pass

    driver.get("https://secure.verizon.com/vzauth/UI/Login")
    
    # Wait for the page to load
    driver.implicitly_wait(5)
	
    # Login
    username_textbox = driver.find_element(By.ID, "IDToken1")
    driver.execute_script("arguments[0].scrollIntoView(true);", username_textbox)
    username_textbox.send_keys(username_fios)

    login_button = driver.find_element(By.ID, "continueBtn")
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
    login_button.click()

    password_textbox = driver.find_element(By.ID, "IDToken2")
    driver.execute_script("arguments[0].scrollIntoView(true);", password_textbox)
    password_textbox.send_keys(password_fios)

    login_button = driver.find_element(By.ID, "continueBtn")
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
    login_button.click()

    # Handle "Remember this device?" if it appears
    try: 
        radio_button = driver.find_element(By.ID, "emailReset")
        driver.execute_script("arguments[0].scrollIntoView(true);", radio_button)
        radio_button.click()
        continue_button = driver.find_element(By.ID, "continueBtn")
        driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
        continue_button.click()
        
    except NoSuchElementException:
        print("Remember device option not found, continuing...")

    # Handle secret question if it appears
    try:    
        secret_question_field = driver.find_element(By.ID, "IDToken2")
        driver.execute_script("arguments[0].scrollIntoView(true);", secret_question_field)
        continue_button = driver.find_element(By.ID, 'continueBtn')
        secret_question_field.send_keys(secret_question_answer_fios)
        continue_button.click()
    except NoSuchElementException:
        print("Secret question not found, continuing...")

    driver.implicitly_wait(20)

    view_bill = driver.find_element(By.PARTIAL_LINK_TEXT, "View Bill Detail")
    driver.execute_script("arguments[0].scrollIntoView(true);", view_bill)
    view_bill.click()

    # Wait for the download link to become clickable
    wait = WebDriverWait(driver, 10)
    download_link_text = "Download PDF"  # adjust as needed
    download = wait.until(EC.element_to_be_clickable(
        (By.PARTIAL_LINK_TEXT, download_link_text)))

    # Scroll the download link into view and click it
    driver.execute_script("arguments[0].scrollIntoView(true);", download)
    time.sleep(1)  # Wait for 1 second
    download.click()

    time.sleep(5)  # Sleep for 3 seconds

    driver.close()

    # Create a secure SSL context
    subject = "GetFiOSBill Script Output"
    body = "This is the GetFiOSBill script output. The FiOS bill should be attached to this email in PDF form."

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Filename
    filename = f"/home/{username_pc}/Downloads/paper-bill.pdf" if current_platform == 'Linux' else f"/Users/{username_pc}/Downloads/paper-bill.pdf"

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            "attachment; filename= paper-bill.pdf",
        )

        message.attach(part)
        text = message.as_string()

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
