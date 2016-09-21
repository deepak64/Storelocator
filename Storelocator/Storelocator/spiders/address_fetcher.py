# encoding: utf-8
import scrapy
import os
from pyvirtualdisplay import Display
import time 
from selenium import webdriver
from scrapy.http import Request
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import ElementNotVisibleException
from scrapy.selector import Selector
from bs4 import BeautifulSoup
sleep_time = 3
import pyap
import MySQLdb
import json
import csv
import logging
from scrapy.utils.log import configure_logging
con = MySQLdb.connect(host ="localhost", user="root",passwd="root",db="Test",use_unicode=True,charset="utf8")
from slugify import slugify
import usaddress
import xml.etree.ElementTree as ET
import requests
from scrapy.http import Request
from Storelocator.items import StorelocatorItem
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import ElementNotVisibleException
from scrapy.selector import Selector

# from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from Storelocator.items import StorelocatorItem

# chromedriver = "/home/deepak/Desktop/chromedriver"
# os.environ["webdriver.chromedriver"] = chromedriver
# driver = webdriver.Chrome(chromedriver)
# # self.self.driver = webself.driver.Firefox()
# driver.maximize_window()

import csv
class ADDfetcher(scrapy.Spider):
	name = 'add'
	# start_urls = [
	# # 'http://local.biglots.com/search/ny/?q=10001'
	# # 'https://hosted.where2getit.com/northface/2015/ajax?lang=en-EN&xml_request=%3Crequest%3E%3Cappkey%3E0835E90E-EDBF-11E4-B7E4-6CB1A38844B8%3C%2Fappkey%3E%3Cformdata+id%3D%22locatorsearch%22%3E%3Cdataview%3Estore_default%3C%2Fdataview%3E%3Corder%3Erank%2C_distance%3C%2Forder%3E%3Csearchradius%3E25%3C%2Fsearchradius%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3E80003%3C%2Faddressline%3E%3Clongitude%3E-105.06743169999999%3C%2Flongitude%3E%3Clatitude%3E39.8182494%3C%2Flatitude%3E%3Ccountry%3EUS%3C%2Fcountry%3E%3C%2Fgeoloc%3E%3C%2Fgeolocs%3E%3Cwhere%3E%3Cvisiblelocations%3E%3Ceq%3E1%3C%2Feq%3E%3C%2Fvisiblelocations%3E%3Cor%3E%3Cyouth%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fyouth%3E%3Capparel%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fapparel%3E%3Cfootwear%3E%3Ceq%3E%3C%2Feq%3E%3C%2Ffootwear%3E%3Cequipment%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fequipment%3E%3Cnorthface%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fnorthface%3E%3Cretailstore%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fretailstore%3E%3Coutletstore%3E%3Ceq%3E%3C%2Feq%3E%3C%2Foutletstore%3E%3Csummit%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fsummit%3E%3Cmt%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fmt%3E%3Caccess_pack%3E%3Ceq%3E%3C%2Feq%3E%3C%2Faccess_pack%3E%3C%2For%3E%3C%2Fwhere%3E%3C%2Fformdata%3E%3C%2Frequest%3E'
	# # "https://www.thenorthface.com/utility/store-locator.html"
	# ]

	# start_urls =['http://www.verizon.com/home/storelocatorresults/?ctoken=&State=DE&SName=Delaware']
	start_urls = [#"http://local.biglots.com/search/ny/?q=10001",
	"http://www.wholefoodsmarket.com/stores/list",
	# "http://www.michaelkors.com/stores/search/united-states/25/10001"
	]
	# url_list = [u'http://www.ikea.com/us/en/store/tempe', u'http://www.ikea.com/us/en/store/burbank', u'http://www.ikea.com/us/en/store/carson', u'http://www.ikea.com/us/en/store/costa_mesa', u'http://www.ikea.com/us/en/store/covina', u'http://www.ikea.com/us/en/store/east_palo_alto', u'http://www.ikea.com/us/en/store/emeryville', u'http://www.ikea.com/us/en/store/san_diego', u'http://www.ikea.com/us/en/store/west_sacramento', u'http://www.ikea.com/us/en/store/centennial', u'http://www.ikea.com/us/en/store/new_haven', u'http://www.ikea.com/us/en/store/miami', u'http://www.ikea.com/us/en/store/orlando', u'http://www.ikea.com/us/en/store/sunrise', u'http://www.ikea.com/us/en/store/tampa', u'http://www.ikea.com/us/en/store/atlanta', u'http://www.ikea.com/us/en/store/bolingbrook', u'http://www.ikea.com/us/en/store/schaumburg', u'http://www.ikea.com/us/en/store/merriam', u'http://www.ikea.com/us/en/store/stoughton', u'http://www.ikea.com/us/en/store/baltimore', u'http://www.ikea.com/us/en/store/college_park', u'http://www.ikea.com/us/en/store/canton', u'http://www.ikea.com/us/en/store/twin_cities', u'http://www.ikea.com/us/en/store/st_louis', u'http://www.ikea.com/us/en/store/charlotte', u'http://www.ikea.com/us/en/store/elizabeth', u'http://www.ikea.com/us/en/store/paramus', u'http://www.ikea.com/us/en/store/las_vegas', u'http://www.ikea.com/us/en/store/brooklyn', u'http://www.ikea.com/us/en/store/long_island', u'http://www.ikea.com/us/en/store/columbus', u'http://www.ikea.com/us/en/store/west_chester', u'http://www.ikea.com/us/en/store/portland', u'http://www.ikea.com/us/en/store/conshohocken', u'http://www.ikea.com/us/en/store/pittsburgh', u'http://www.ikea.com/us/en/store/philadelphia', u'http://www.ikea.com/us/en/store/memphis', u'http://www.ikea.com/us/en/store/frisco', u'http://www.ikea.com/us/en/store/houston', u'http://www.ikea.com/us/en/store/round_rock', u'http://www.ikea.com/us/en/store/draper', u'http://www.ikea.com/us/en/store/woodbridge', u'http://www.ikea.com/us/en/store/seattle']
	# for url in url_list:
	# 	start_urls.append(url)
	

	
	def parse(self, response):
		'''div/ancestor::*[@id="block-views-80946ef4b139b2cead1c5f9f9cb3d671"]'''
		print response.xpath('//*[@id="block-views-80946ef4b139b2cead1c5f9f9cb3d671"]/div/div/div[3]/div[1]/div[2]/div[4]/div[1]/./preceding-sibling::').extract()
		# driver.get(response.url)
		# item = StorelocatorItem()
		# reader = csv.reader(open('/home/deepak/Relative_Xpath.csv',"rb"))
		# # reader.next()
		# for row in reader:
		# 	# print "rowSSSSSSSSSSSSSSSSSSSSSSSSS", row
		# 	BrandName_from_config = row[0]
		# 	Parent_xpath = row[2]
		# 	StoreName_xpath = row[3]
 	# 		Full_street_xpath = row[4]
		# 	City_xpath = row[5]
		# 	State_xpath = row[6]
		# 	Zipcode_xpath = row[7]
		# 	phone_xpath = row[8]


	
		# 	if BrandName_from_config in response.url:
				
		# 		BrandName = BrandName_from_config
		# 		# print response.xpath('//span[@lass="locality"]/text()').extract()

		# 		parents = response.xpath(Parent_xpath)

		# 		for parent in parents:
		# 			print parent.xpath('text()').extract()
					# print ">>>>>>>>>>>>>>>",parent.xpath('div/text()').extract()
					# StoreName  = "".join(parent.xpath(StoreName_xpath).extract()).strip()
					# Full_Street = "".join(parent.xpath(Full_street_xpath).extract()).strip()
					
					# City = "".join(parent.xpath(City_xpath).extract()).strip()
					# State =  "".join(parent.xpath(State_xpath).extract()).strip()
					# Zipcode =  "".join(parent.xpath(Zipcode_xpath).extract()).strip()
					# PhoneNumber =  "".join(parent.xpath(phone_xpath).extract()).strip()
					
					# print StoreName
					# print Full_Street
					# print City
					# print State
					# print Zipcode
					# print PhoneNumber

					# RawAddress = Full_Street + City + Zipcode + State
					# Country ='US'
					# Latitude = None
					# Longitude = None
					# BrandID = None
					# Category = None

					# DataSource = BrandName

					# key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
					# item_dict = {}
					# for key in key_list:
					# 	# print key
					# 	item_dict[key] = locals()[key]
						
					# item['rows'] = item_dict
					# yield item

					# BrandID = 916
					# BrandName = 'biglots'


		

		