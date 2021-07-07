from selenium import webdriver
from getpass import getpass
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os

#Delete file if it already exists
try:
    os.remove('/Users/dbelle/Downloads/paper-bill.pdf')
except OSError:
    pass
    
#Auth using env variables
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
password_email = os.environ.get('PASSWORD_EMAIL')

driver = webdriver.Chrome("/Users/dbelle/Documents/dbelle_scripts/get_FIOS_bill/chromedriver")
driver.get("https://secure.verizon.com/vzauth/UI/Login")

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

view_bill = driver.find_element_by_partial_link_text("View Bill Detail")
view_bill.click()

download = driver.find_element_by_partial_link_text("Download PDF")
download.click()

time.sleep(5) # Sleep for 3 seconds

# Create a secure SSL context
subject = "An email with attachment from Python"
body = "This is an email with attachment sent from Python"
sender_email = "tt5775030@gmail.com"
receiver_email = "dauryl.belle@gmail.com"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails

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
