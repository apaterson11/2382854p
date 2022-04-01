import logging
import threading
import os
import subprocess
import sys
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
# from .test-bandwidth import DumbellTopo
# from testbandwidth import stopServer
# import testbandwidth

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument('--unsafely-treat-insecure-origin-as-secure=http://10.0.0.2:4001')


    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = { 'browser':'ALL' }

    driver = webdriver.Chrome(options=options, desired_capabilities=d)
    # load the desired webpage
    # print("1")
    # driver.get('https://www.google.co.uk')
    driver.get('http://localhost:4000/1')

    messages = []

    while(len(messages) < 3):
        for entry in driver.get_log('browser'):
            if 'result' in str(entry):
                value = str(entry['message']).split("result: ",1)[1]
                # value = value[:-1]
                # value = str(entry['message'])
                value = value.replace('"', '')
                messages.append(value)

    f = open("results.csv", "a")
    writer = csv.writer(f)
    writer.writerow(messages)
    f.close()

    driver.quit()