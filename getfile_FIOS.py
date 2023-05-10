import os
import platform
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from getpass import getpass
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Detect the current platform
current_platform = platform.system()

# Set up Chrome options
options = webdriver.ChromeOptions()

if current_platform == 'Linux':
    # Set up headless mode for Linux (Ubuntu server)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

chromedriver_path = '/usr/local/bin/chromedriver' if current_platform == 'Linux' else '/Users/dbelle/Documents/dbelle_scripts/get_FIOS_bill/chromedriver'

# Initialize the webdriver with the new syntax
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

# Delete file if it already exists
pdf_path = "/home/dbelle/Downloads/paper-bill.pdf" if current_platform == 'Darwin' else "/path/to/your/ubuntu/pdf/location/paper-bill.pdf"

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

username_textbox = driver.find_element_by_id("IDToken1")
username_textbox.send_keys(username)

password_textbox = driver.find_element_by_id("IDToken2")
password_textbox.send_keys(password)

login_button = driver.find_element_by_id("login-submit")
login_button.submit()

# Challenge Question


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


if check_exists_by_xpath("//input[@id='IDToken1']"):
    secret_question = driver.find_element_by_id("IDToken1")
    secret_question.send_keys(secret_question_answer)
    continue_button = driver.find_element_by_id("otherButton")
    continue_button.submit()


driver.implicitly_wait(20)

view_bill = driver.find_element_by_partial_link_text("View Bill Detail")
view_bill.click()

download = driver.find_element_by_partial_link_text("Download PDF")
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

filename = "/Users/dbelle/Downloads/paper-bill.pdf"  # In same directory as script

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
