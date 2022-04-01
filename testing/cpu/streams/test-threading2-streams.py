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


    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = { 'browser':'ALL' }

    driver2 = webdriver.Chrome(options=options, desired_capabilities=d)
    # load the desired webpage
    print("2")
    driver2.execute_script('window.open()')
    driver2.switch_to.window(driver2.window_handles[1])
    driver2.get('http://10.0.0.2:4001')

    messages = []

    # print("entering while loop")
    while(len(messages) < 1):
        for entry in driver2.get_log('browser'):
            if "result" in str(entry):
                messages.append(entry)
                try:
                    f = open("results.csv", "a")
                    value = str(entry['message']).split("result: ",1)[1]
                    value = value[:-1]
                    writer = csv.writer(f)
                    writer.writerow([value])
                    f.close()
                    driver2.quit()
                except:
                    print("line cannot be read")
                
                # print("server stopped called")
                # testbandwidth.stopServer(testbandwidth.net)
                # serv = testbandwidth.net.get('serv')
                # serv.stop()
