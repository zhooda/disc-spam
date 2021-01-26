import os
import platform
import sys
import time

from utils import eprint, WebDriverError, PlatformError

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# verifying and getting command line args
if len(sys.argv) < 4:
    eprint(f"USAGE:\n\t{sys.argv[0]} <ITERATIONS> <INTERVAL> <MESSAGE>")

try:
    ITERATIONS = int(sys.argv[1])
    MESSAGE    = sys.argv[3]
    
    tmp = sys.argv[2]

    if tmp[-1] == "s":
        INTERVAL = int(str(tmp[:-1]))
    elif tmp[-1] == "m":
        INTERVAL = int(str(tmp[:-1])) * 60
    elif tmp[-1] == "h":
        INTERVAL = int(str(tmp[:-1])) * 60 * 60
    elif tmp[-1] == "d":
        INTERVAL = int(str(tmp[:-1])) * 60 * 60 * 24
    else:
        eprint("Error: invalid interval, use s, m, h, or d (ie. 60s, 20m, 6h, 2d)")
    
except ValueError:
    eprint("Error: invalid commang line arguments")

# load configuration from .env file
load_dotenv()

PLATFORM   = platform.system().lower()
BROWSER    = os.getenv("BROWSER")
DISC_EMAIL = os.getenv("DISC_EMAIL")
DISC_PASS  = os.getenv("DISC_PASS")
DISC_SERVER = os.getenv("DISC_SERVER")
DISC_CHANNEL = os.getenv("DISC_CHANNEL")
TFA_ENABLED = (os.getenv("TFA_ENABLED") == 'true')

if PLATFORM == "darwin":
    if BROWSER == "firefox":
        DRIVER_PATH = "./drivers/firefox/geckodriver_mac"
    elif BROWSER == "chrome":
        DRIVER_PATH = "./drivers/chrome/chromedriver_mac"
    else:
        raise WebDriverError(BROWSER)
elif PLATFORM == "linux":
    if BROWSER == "firefox":
        DRIVER_PATH = "./drivers/firefox/geckodriver_linux"
    elif BROWSER == "chrome":
        DRIVER_PATH = "./drivers/chrome/chromedriver_linux"
    else:
        eprint("Error: invalid webdriver/browser")
        raise WebDriverError(BROWSER)
elif PLATFORM == "windows":
    if BROWSER == "firefox":
        DRIVER_PATH = "./drivers/firefox/geckodriver.exe"
    elif BROWSER == "chrome":
        DRIVER_PATH = "./drivers/chrome/chromedriver.exe"
    else:
        eprint("Error: invalid webdriver/browser")
        raise WebDriverError(BROWSER)
else:
    raise PlatformError(PLATFORM)

if BROWSER == "firefox":
    driver = webdriver.Firefox(executable_path=DRIVER_PATH)
else:
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

# load the website
driver.get("https://discord.com/login")
driver.implicitly_wait(10)

# setup input fields
email_field = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[1]/div/div[2]/input")
password_field = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[2]/div/input")

# login sequence
email_field.send_keys(DISC_EMAIL)
email_field.send_keys(Keys.TAB)
password_field.send_keys(DISC_PASS)
password_field.send_keys(Keys.RETURN)

# managing 2FA
if TFA_ENABLED:
    tfa_field = driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/form/div/div[3]/div/div/input")
    print("Press ENTER here when you're done typing the 2FA code in the python shell")
    tfa_code = input("2FA CODE >> ")
    tfa_field.send_keys(tfa_code)
    tfa_field.send_keys(Keys.ENTER)

print("waiting")
time.sleep(3)

# clicking on the server
servers = driver.find_elements_by_css_selector("div[class^=wrapper-]")

counter = 0
max_searches = 10
while len(servers) < 0:
    counter += 1
    time.sleep(3)
    servers = driver.find_elements_by_css_selector("div[class^=wrapper-]")
    print(servers)
    if counter >= max_searches:
        break

time.sleep(5)
for elem in list(filter(None, servers)):
    # print(type(elem.get_attribute('aria-label')))
    if DISC_SERVER.lower() in str(elem.get_attribute('aria-label')).lower():
        elem.click()
        print("server clicked")
        break

channels = driver.find_elements_by_css_selector("div[class^=name-]")
for elem in list(filter(None, channels)):
    if DISC_CHANNEL.lower() in str(elem.text):
        elem.click()
        print("channel clicked")
        break

message_field = driver.find_element_by_css_selector("div[class^=textArea-]")
message_field.click()
print("message field clicked")

for i in range(ITERATIONS):
    actions = ActionChains(driver)
    actions.send_keys(MESSAGE)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    print(f"sleeping for {sys.argv[2]}")
    time.sleep(INTERVAL)