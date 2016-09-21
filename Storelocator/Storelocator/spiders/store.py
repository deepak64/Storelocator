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

from scrapy_splash import SplashRequest

class SToreIdentity(scrapy.Spider):
	name = 'storel'
	# start_urls = [
	# # 'http://local.biglots.com/search/ny/?q=10001'
	# # 'https://hosted.where2getit.com/northface/2015/ajax?lang=en-EN&xml_request=%3Crequest%3E%3Cappkey%3E0835E90E-EDBF-11E4-B7E4-6CB1A38844B8%3C%2Fappkey%3E%3Cformdata+id%3D%22locatorsearch%22%3E%3Cdataview%3Estore_default%3C%2Fdataview%3E%3Corder%3Erank%2C_distance%3C%2Forder%3E%3Csearchradius%3E25%3C%2Fsearchradius%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3E80003%3C%2Faddressline%3E%3Clongitude%3E-105.06743169999999%3C%2Flongitude%3E%3Clatitude%3E39.8182494%3C%2Flatitude%3E%3Ccountry%3EUS%3C%2Fcountry%3E%3C%2Fgeoloc%3E%3C%2Fgeolocs%3E%3Cwhere%3E%3Cvisiblelocations%3E%3Ceq%3E1%3C%2Feq%3E%3C%2Fvisiblelocations%3E%3Cor%3E%3Cyouth%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fyouth%3E%3Capparel%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fapparel%3E%3Cfootwear%3E%3Ceq%3E%3C%2Feq%3E%3C%2Ffootwear%3E%3Cequipment%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fequipment%3E%3Cnorthface%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fnorthface%3E%3Cretailstore%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fretailstore%3E%3Coutletstore%3E%3Ceq%3E%3C%2Feq%3E%3C%2Foutletstore%3E%3Csummit%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fsummit%3E%3Cmt%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fmt%3E%3Caccess_pack%3E%3Ceq%3E%3C%2Feq%3E%3C%2Faccess_pack%3E%3C%2For%3E%3C%2Fwhere%3E%3C%2Fformdata%3E%3C%2Frequest%3E'
	# # "https://www.thenorthface.com/utility/store-locator.html"
	# ]

	start_urls =[#'http://www.thefreshmarket.com/all-stores/',
	'http://whataburger.com/locations'
	]
	start_urls =['http://whataburger.com/locations/store/378#location_378']
	

	# start_urls =['http://www.ikea.com/us/en/store/tempe/']

	# start_urls =['http://www.verizon.com/home/storelocator/']

	start_urls =["http://www.thefreshmarket.com/directions?store=43"]
	def parse(self, response):
		if "verizon" in response.url:

			Sname =  response.xpath('//select[@id="ddlState"]/option/text()').extract()[1:]
			State  = response.xpath('//select[@id="ddlState"]/option/@value').extract()[1:]
			# print State
			for sname, state in zip(Sname, State):
				print sname,state
				sname = sname.replace(' ','+')
				urlss = "http://www.verizon.com/home/storelocatorresults/?ctoken=&State="+str(state)+"&SName="+str(sname)
				
				yield Request(url = urlss, callback = self.parse_next)

		elif "thefreshmarket" in response.url:
			links = response.xpath('//td[@class="cta last"]/a/@href').extract()
			for link in links:
				print link
				link = 'http://www.thefreshmarket.com' + link 
				yield Request(url = link, callback = self.parse_next)

		elif "whataburger" in response.url:
			links = response.xpath('//ul[@class="stores clearfix"]/li/p/a[2]/@href').extract()
			print links,len(links)
			for link in links:
				print link
				link = 'http://whataburger.com' + link 
				yield Request(url = link, callback = self.parse_next)		
		else:
			yield Request(url = response.url, callback = self.parse_next)



	def parse_next(self, response):
		item = StorelocatorItem()

		Category = None
		if 'biglots' in response.url:

			parents = response.xpath('//div[@class="result clearfix"]')
			for parent in parents:
				StoreName  = "".join(parent.xpath('h2/a[@class="resultname"]/@title').extract())
				Full_Street = "".join(parent.xpath('div//span[@itemprop="streetAddress"]/text()').extract())
				
				City = "".join(parent.xpath('div//span[@class="locality"]/text()').extract())
				State =  "".join(parent.xpath('div//span[@class="region"]/text()').extract())
				Zipcode =  "".join(parent.xpath('div//span[@class="postal-code"]/text()').extract())
				PhoneNumber =  "".join(parent.xpath('div/span[@itemprop="telephone"]/text()').extract())
				
				BrandID = 916
				BrandName = 'biglots'


				# print "StoreName",StoreName
				# print "Full_Street>",Full_Street
				# print "City ",City
				# print "State>>",State
				# print "Zipcode",Zipcode
				# print "phone",phone
				RawAddress = Full_Street + City + Zipcode + State
				Country ='us'
				Latitude = None
				Longitude = None

				DataSource = BrandName

				key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
				item_dict = {}
				for key in key_list:
					# print key
					item_dict[key] = locals()[key]
					
				item['rows'] = item_dict
				yield item
				# print item


		elif "northface" in response.url:
			res = requests.get(response.url)
			soup = BeautifulSoup(res.text.encode('utf-8'))
			pois = soup.find_all('poi')
			for poi in pois:
				StoreName  = poi.find('name').text
				Full_Street = poi.find('address1').text
				City = poi.find('city').text
				Country = poi.find('country').text
				Latitude = poi.find('latitude').text
				Longitude = poi.find('longitude').text
				PhoneNumber = poi.find('phone').text
				Zipcode = poi.find('postalcode').text
				State = poi.find('state').text

				BrandID = 4226
				print StoreName
				print Full_Street
				BrandName ='northface'

		elif "thefreshmarket" in response.url:
			try:

				address_block = response.xpath('//dd[@id="store_address"]/strong/text()').extract()
			
				Full_Street = address_block[0].strip()
				print Full_Street
				second_block  = address_block[1].split(',')
				City = second_block[0].strip()
				second_block  = address_block[1].split(',')
				State = second_block[1].strip().split()[0]
				Zipcode = second_block[1].strip().split()[1]
				BrandID = 4048
				Latitude = None
				Longitude = None
				StoreName = 'Fresh_Market'
				BrandName = 'Fresh_Market'
				Category  = None
				DataSource = BrandName
				Country ='US'
				PhoneNumber = response.xpath('//dd[@id="store_phone"]/strong/text()').extract()
				PhoneNumber =PhoneNumber[1].strip() if PhoneNumber else None
				RawAddress = Full_Street + " "+ City + State + " " + Zipcode 

				final_db   = [BrandName, StoreName, RawAddress, Full_Street, City, State, Zipcode, PhoneNumber, BrandID, Longitude, Latitude, Category, DataSource, Country]
				print final_db
				key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
				item_dict = {}
				for key in key_list:
					# print key
					item_dict[key] = locals()[key]
				item['rows'] = item_dict

				yield item


			except:
				text_file = open("fresh_market.txt", "w")
				text_file.write("Failed Url: %s" % response.url)
				text_file.close()


		elif "verizon.com" in response.url:
			address = response.xpath('//*[@id="ghfbodycontent"]/div/div[1]/table[1]/tbody/tr')
			for add in  address:
				StoreName1 = add.xpath('td[1]/text()[1]').extract()
				try:
					StoreName = add.xpath('td[1]/text()[1]').extract_first()
					PhoneNumber = add.xpath('td[3]/text()[1]').extract_first()
					print PhoneNumber
					Full_Street = add.xpath('td[1]/text()[2]').extract_first(default='None').strip()
					print StoreName
					print Full_Street
					# print  add.xpath('td[1]/text()[3]').extract()[0].strip()
					second_block = add.xpath('td[1]/text()[3]').extract()[0].strip().split(',')
					City = second_block[0].strip()
					# print City
					State = second_block[1].split()[0]
					Zipcode = second_block[1].split()[1]
					BrandID = 97
					Latitude = None
					Longitude = None

					Category  = None
					BrandName ='verizon'
					DataSource = BrandName
					Country ='US'
					RawAddress = Full_Street + " "+ City + State + " " + Zipcode
					final_db   = [BrandName, StoreName, RawAddress, Full_Street, City, State, Zipcode, PhoneNumber, BrandID, Longitude, Latitude, Category, DataSource, Country]
					print final_db
					key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
					item_dict = {}
					for key in key_list:
						# print key
						item_dict[key] = locals()[key]
					item['rows'] = item_dict

					yield item
				except:
					text_file = open("whataburger.txt", "w")
					text_file.write("Purchase Amount: %s" % StoreName1)
					text_file.close()

		elif "whataburger" in response.url:

			StoreName = response.xpath('//ul[@class="stores"]/li/h4/text()').extract_first(default = None).strip()
			
		
			BrandName ='whataburger'
			Full_Street = response.xpath('//ul[@class="stores"]/li/p/text()').extract_first(default = None).strip()
			print Full_Street

			second_block = response.xpath('//ul[@class="stores"]/li/p/text()').extract()[1].strip().split(',')
			print second_block
			City = second_block[0].strip()
			State = second_block[1].split()[0]
			Zipcode = second_block[1].split()[1]
			BrandID = 2124
			PhoneNumber = None
			# Latitude = None
			# Longitude = None

			# Category  = None
			# DataSource = BrandName
			# Country ='US'
			# PhoneNumber = None
			# RawAddress = Full_Street + " "+ City + State + " " + Zipcode
			# final_db   = [BrandName, StoreName, RawAddress, Full_Street, City, State, Zipcode, PhoneNumber, BrandID, Longitude, Latitude, Category, DataSource, Country]
			# print final_db
			# key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
			# item_dict = {}
			# for key in key_list:
			# 	# print key
			# 	item_dict[key] = locals()[key]
			# item['rows'] = item_dict

			# yield item
				# except:
				# 	text_file = open("whataburger.txt", "w")
				# 	text_file.write("Purchase Amount: %s" % StoreName1)
				# 	text_file.close()

 





				# except:
				# 	pass




				# break

		elif "ikea.com" in response.url:

			chromedriver = "/home/deepak/Desktop/chromedriver"
			os.environ["webdriver.chrome.driver"] = chromedriver
			driver = webdriver.Chrome(chromedriver)
			driver.get(response.url)
			elem = driver.find_elements_by_xpath('//select[@id="localStore"]/option')
			for ele in elem:
				urls= ele.get_attribute('value')
				base_url ='http://www.ikea.com'
				url  = base_url + urls
				yield Request(url = url, callback = self.parse_link)
				# break



	def parse_link(self, response):

		Raw_Address = "".join(response.xpath('//div[@class="leftColumn toleft"]/div[2]/text()').extract()).replace('\n',' ').encode('utf-8').strip().upper()
		
		addresses = pyap.parse(Raw_Address, country='US')
		if len(addresses) ==0:
			text_file = open("Output.txt", "w")
			text_file.write("Purchase Amount: %s" % address_block)
			text_file.close()
		else:
			for address in addresses:
				
				Full_Street = (address.as_dict())['full_street']
				City = (address.as_dict())['city']
				State = (address.as_dict())['region1']
				Zipcode = (address.as_dict())['postal_code']
				phone = re.findall(r'[(]*\d{3}[)]*[\s\-\.]*[(]*\d{3}[)]*[\s\-\.]*[(]*\d{4}[)]*|\d{10}',Raw_Address)
				PhoneNumber = phone[0] if phone else None

				BrandID = 52
				BrandName = 'ikea'

				RawAddress = Full_Street + City + Zipcode + State
				Country ='us'
				Latitude = None
				Longitude = None
				Category = None
				DataSource = BrandName
				StoreName = "".join(response.xpath('//div[@class="currentStore"]/text()').extract()).strip()

				final_db   = [BrandName, StoreName, RawAddress, Full_Street, City, State, Zipcode, PhoneNumber, BrandID, Longitude, Latitude, Category, DataSource, Country]
				print len(final_db)


				'''Creating Table By Brand Name'''
				import MySQLdb
				con = MySQLdb.connect(host ="localhost", user="root",passwd="root",db="Test", use_unicode=True,charset="utf8")
				
				# Final_DB = []
				# for final in final_db:
				# 	Final_DB.append(final.encode('utf-8'))


				with con:
					cur=con.cursor()
					create_table = ('CREATE TABLE if NOT EXISTS ' + str(BrandName) +'  LIKE TestDB;')
					print create_table
					cur.execute(create_table)
					con.commit()

					''''''''''''''''INSERT into Table by Brand Name'''''''''''''''

					cur.execute('''INSERT IGNORE INTO ''' + str(BrandName)  + ''' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', final_db) #### Number of coulms input
		
					con.commit()