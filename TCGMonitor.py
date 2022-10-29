# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 17:36:09 2022

@author: mithr
"""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import smtplib
# discordwebhook

#Change these constants
driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))
#Make sure this .txt is formated like ####$#### where left is productid and right is price as a float
cardlistpath = 'C:/Users/mithr/Desktop/TCGScraper/cardlist.txt'
sender = 'sample@gmail.com'
pwd = 'pwd'
receivers = ['mithran.mohanraj@gmail.com']
subject = 'Cards Detected Under Price:'
body = ''

# Prepare actual message
message = """From: %s\nTo: %s\nSubject: %s\n\n%s
""" % (sender, ", ".join(receivers), subject, body)

product_url_template = 'https://www.tcgplayer.com/product/'
myproducts = []
productid = ''

cardlisttxt = open(cardlistpath, 'r')
cardlist = cardlisttxt.readlines()
cardlisttxt.close()

#I could put this whole thing in a loop but I'm not authorized to do that yet
#Open the input file by the path of that file
for card in cardlist:
    split = card.split('$')
    driver.get(product_url_template + split[0])
    print(split[1])
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    productprice = soup.find('span', {'class': 'spotlight__price'}).text.replace('$','')
    if float(productprice) < float(split[1]):
        print( split[0] + 'is under')
        message += product_url_template + split[0] + '\n Is under ' + split[1]
#Send an email
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(sender, pwd)
    server.sendmail(sender, receivers, message)
    server.close()
    print("Successfully sent email")
except:
    print ("Error: unable to send email")
    
driver.close()
driver.quit()
