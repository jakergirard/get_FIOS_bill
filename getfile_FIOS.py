from selenium import webdriver
from getpass import getpass
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

##Logging in to Verizon FIOS
# username = input("Enter user: ")
# password = getpass("Enter password: ")
#
#
# driver = webdriver.Chrome("/Users/dbelle/Documents/dbelle_scripts/get_FIOS_bill/chromedriver")
# driver.get("https://secure.verizon.com/vzauth/UI/Login")
#
# driver.implicitly_wait(5)
#
# username_textbox = driver.find_element_by_id("IDToken1")
# username_textbox.send_keys(username)
#
# password_textbox = driver.find_element_by_id("IDToken2")
# password_textbox.send_keys(password)
#
# login_button = driver.find_element_by_id("login-submit")
# login_button.submit()
#
# view_bill = driver.find_element_by_partial_link_text("View Bill Detail")
# view_bill.click()
#
# download = driver.find_element_by_partial_link_text("Download PDF")
# download.click()





# password = getpass("Type your password and press enter: ")

# Create a secure SSL context
port = 1025  # For SSL
smtp_server = "localhost"
subject = "An email with attachment from Python"
body = "This is an email with attachment sent from Python"
sender_email = "my@gmail.com"
receiver_email = "your@gmail.com"
# password = input("Type your password and press enter:")

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

filename = "testfile.txt"  # In same directory as script

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
with smtplib.SMTP(smtp_server, port) as server:
    # server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
