import logging
import threading
import os
import subprocess
import csv
import sys
import time
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

    driver2 = webdriver.Chrome(options=options, desired_capabilities=d)
    # load the desired webpage
    print("2")
    driver2.execute_script('window.open()')
    driver2.switch_to.window(driver2.window_handles[1])
    driver2.get('http://10.0.0.2:4001/1')
    driver2.quit()

    # messages = []

    # # print("entering while loop")
    # while(len(messages) < 1):
    #     for entry in driver2.get_log('browser'):
    #         print(entry)
    #         if "transport closed" in str(entry):
    #             f = open("results.csv", "a")
    #             value = str(entry['message']).split("transport closed: ",1)[1]
    #             value = value[:-1]
    #             writer = csv.writer(f)
    #             writer.writerow([value])
    #             f.close()
    #             driver2.quit()
    #             # print("server stopped called")
    #             # testbandwidth.stopServer(testbandwidth.net)
    #             # serv = testbandwidth.net.get('serv')
    #             # serv.stop()
