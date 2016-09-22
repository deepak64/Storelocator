# encoding: utf-8
import scrapy
import os
from pyvirtualdisplay import Display
import time 
# from selenium import webdriver
from scrapy.http import Request
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
import re
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import NoAlertPresentException
# from selenium.common.exceptions import ElementNotVisibleException
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
# from slugify import slugify
import usaddress
import xml.etree.ElementTree as ET
import requests
from scrapy.http import Request
from Storelocator.items import StorelocatorItem
from scrapy.linkextractors import LinkExtractor

# from scrapy_splash import SplashRequest
import random 
import time

class HundredBrand(scrapy.Spider):
	name = 'hundred'

	start_urls =[#"http://www.homedepot.com/StoreFinder/storeDirectory",
	# "http://www.bk.com/restaurants/sitemap.html",
	# "https://www.ihg.com/holidayinnexpress/destinations/us/en/united-states-hotels",
	# "https://locations.wendys.com/",
	# "http://local.safeway.com/",
	# "http://franchise.7-eleven.com/franchise/available-store-locations",
	"https://www.24hourfitness.com/ClubInformation/rest/v1/Gyms"	
	]
	def parse(self, response):
		
		if "homedepot" in response.url:
			links = response.xpath('//li[@class="stateList__item"]/a/@href').extract()
			for link in links:
				link = 'http://www.homedepot.com'+ link
				yield Request(url = link, callback = self.pagination)

		elif "bk.com/" in response.url:
			links = response.xpath('//ul[@class="store-list"]/li/a/@href').extract()
			for link in links:
				link = 'http://www.bk.com'+ link
				yield Request(url = link, callback = self.pagination)
		elif "ihg.com" in response.url:
			links = response.xpath('//li[@class="listingItem"]/a/@href').extract()
			time.sleep(random.randint(7, 11))
			for link in links:
				yield Request(url = link, callback = self.pagination)

		elif "wendys.com" in response.url:
			links = response.xpath('//h2[text()="Browse by State or Province"]/following-sibling::div/ul/li/a/@href').extract()
			for link in links:
				link = 'https://locations.wendys.com/'+ link
				yield Request(url = link, callback = self.pagination)

		elif "safeway" in response.url:
			links = response.xpath('//div[@class="row"]/a/@href').extract()
			for link in links:
				yield Request(url = link, callback = self.pagination)
		elif "7-eleven" in response.url:
			links = response.xpath('//*[@id="stores_listing"]/div/div[4]/div/div/div/ul/li/a/@href').extract()
			for link in links:
				link = 'http://franchise.7-eleven.com' + link
				yield Request(url = link, callback = self.pagination)



		else:
			yield Request(url = response.url, callback = self.pagination)

	def pagination(self, response):
		# time.sleep(random.randint(2,5))
		print "response_pagination",response.url

		if "homedepot" in response.url:

			links = response.xpath('//li[@class="grid_7 local-store"]/a/@href').extract()
			time.sleep(random.randint(7, 11))
			for link in links:
				link = 'http://www.homedepot.com'+ link
				yield Request(url = link, callback = self.parse_next)
		elif "ihg.com" in response.url:
			links = response.xpath('//li[@class="listingItem"]/a/@href').extract()
			time.sleep(random.randint(7, 11))
			for link in links:
				yield Request(url = link, callback = self.parse_next)

		elif "wendys.com" in response.url:
			links = response.xpath('//h2[text()="Browse by City"]/following-sibling::div/ul/li/a/@href').extract()
			for link in links:	
				link = 'https://locations.wendys.com'+ link
				yield Request(url = link, callback = self.parse_next)
		elif 'safeway' in response.url:
			links = response.xpath('//div[@class="city_item"]/a/@href').extract()
			for link in links:
				yield Request(url = link, callback = self.parse_next)


		else:
			print "hellllllllllllllllooooooooooooooooooooooooooooooo"
			yield Request(url = response.url, callback = self.parse_next)



	def parse_next(self, response):
		time.sleep(random.randint(2,5))
		print "response>>>next", response.url
		
		if "wendys.com" in response.url:
			links = response.xpath('//a[@itemprop="address"]/@href').extract()
			# time.sleep(random.randint(7, 11))
			for link in links:
				link ='https://locations.wendys.com/' + link
				yield Request(url = link , callback = self.parse_details)
		elif 'safeway.com' in response.url:
			links = response.xpath('//div[@id="cities"]/ul/li/a/@href').extract()
			for link in links:
				yield Request(url = link, callback = self.parse_details)
		else:
			yield Request(url = response.url, callback = self.parse_details)




	def parse_details(self, response):
		print "details>>>>>>>>>>urlssssssssssssss.", response.url
		item = StorelocatorItem()

# 		Category = None
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

		elif 'homedepot' in response.url:

			try:
				
				StoreName  = "".join(response.xpath('//h1[@class="page-title"]/text()').extract())
				Full_Street = "".join(response.xpath('//span[@itemprop="streetAddress"]/text()').extract())
				
				City = "".join(response.xpath('//span[@itemprop="addressLocality"]/text()').extract())
				State =  "".join(response.xpath('//span[@itemprop="addressRegion"]/text()').extract())
				Zipcode =  "".join(response.xpath('//span[@itemprop="postalCode"]/text()').extract())
				PhoneNumber =  "".join(response.xpath('//span[@itemprop="telephone"]/text()').extract())
				
				BrandID = None
				BrandName = 'homedepot'


				# print "StoreName",StoreName
				# print "Full_Street>",Full_Street
				# print "City ",City
				# print "State>>",State
				# print "Zipcode",Zipcode
				# print "phone",phone
				RawAddress = Full_Street + City + Zipcode + State
				Country ='us'
				Latitude =  "".join(response.xpath('//meta[@itemprop="latitude"]/@content').extract())
				Longitude = "".join(response.xpath('//meta[@itemprop="longitude"]/@content').extract())

				DataSource = BrandName
				Category = None

				key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
				item_dict = {}
				for key in key_list:
					# print key
					item_dict[key] = locals()[key]
					
				item['rows'] = item_dict
				yield item
			except:
				text_file = open("homedepot.txt", "w")
				text_file.write("Failed Url: %s" % response.url)
				text_file.close()

		elif 'bk.com/' in response.url:

			# try:
				time.sleep(random.randint(3,9))
				StoreName  = "".join(response.xpath('//div[@itemprop="name"]/text()').extract()).strip()
				Full_Street = "".join(response.xpath('//span[@itemprop="streetAddress"]/text()').extract()).strip()
				
				City = "".join(response.xpath('//span[@itemprop="addressLocality"]/text()').extract()).strip()
				State =  "".join(response.xpath('//span[@itemprop="addressRegion"]/text()').extract()).strip()
				Zipcode =  "".join(response.xpath('//span[@itemprop="postalCode"]/text()').extract()).strip()
				PhoneNumber =  "".join(response.xpath('//strong[@itemprop="telephone"]/text()').extract()).strip()
				
				BrandID = None
				BrandName = 'Burger_King'


				print "StoreName",StoreName
				print "Full_Street>",Full_Street
				print "City ",City
				print "State>>",State
				print "Zipcode",Zipcode
				print "phone",PhoneNumber
				RawAddress = Full_Street + City + Zipcode + State
				Country ='us'

				script = "".join(response.xpath("//script[@type='application/ld+json']/text()").extract())
				# print ">>>>>>>>>>>>",script
				data = json.loads(script)
				print data 
				Latitude =  data['geo']['latitude']
				Longitude = data['geo']['longitude']
				# print Latitude
				# print Longitude
				DataSource = BrandName
				Category = None

				key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
				item_dict = {}
				for key in key_list:
					# print key
					item_dict[key] = locals()[key]
					
				item['rows'] = item_dict
				yield item
			# except:
				# text_file = open("burger_king.txt", "w")
				# text_file.write("Failed Url: %s" % response.url)
				# text_file.close()

		elif "wendys.com" in response.url:
			try:
				time.sleep(random.randint(7, 17))
				StoreName  = "".join(response.xpath('//meta[@itemprop="alternateName"]/@content').extract())
				Full_Street = "".join(response.xpath('//p[@itemprop="streetAddress"]/text()').extract())
				
				City = "".join(response.xpath('//span[@itemprop="addressLocality"]/text()').extract())
				State =  "".join(response.xpath('//span[@itemprop="addressRegion"]/text()').extract())
				Zipcode =  "".join(response.xpath('//span[@itemprop="postalCode"]/text()').extract())
				PhoneNumber =  "".join(response.xpath('//span[@itemprop="telephone"]/text()').extract())
				
				BrandID = None
				BrandName = 'wendys'


				# print "StoreName",StoreName
				# print "Full_Street>",Full_Street
				# print "City ",City
				# print "State>>",State
				# print "Zipcode",Zipcode
				# print "phone",phone
				RawAddress = Full_Street + City + Zipcode + State
				Country ='us'
				Latitude =  "".join(response.xpath('//span[@itemprop="geo"]/meta[@itemprop="latitude"]/@content').extract())
				Longitude = "".join(response.xpath('///span[@itemprop="geo"]/meta[@itemprop="longitude"]/@content').extract())

				DataSource = BrandName
				Category = None

				key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
				item_dict = {}
				for key in key_list:
					# print key
					item_dict[key] = locals()[key]
					
				item['rows'] = item_dict
				yield item
			except:
				text_file = open("wendys.txt", "w")
				text_file.write("Failed Url: %s" % response.url)
				text_file.close()

		elif "safeway.com" in response.url:
			# try:
				time.sleep(random.randint(7, 17))
				BrandName = 'safeway'
				StoreName  = 'safeway'
				Full_Street = response.xpath('//meta[contains(@property,"street_address")]/@content').extract_first(default = "None").strip()
				
				City = response.xpath('//meta[contains(@property,"locality")]/@content').extract_first(default = "None").strip()
				State =  response.xpath('//meta[contains(@property,"region")]/@content').extract_first(default = "None").strip()
				Zipcode =  response.xpath('//meta[contains(@property,"postal_code")]/@content').extract_first(default = "None").strip()
				PhoneNumber =  response.xpath('//meta[contains(@property,"phone_number")]/@content').extract_first(default = "None").strip()
				
				BrandID = None
				


				# print "StoreName",StoreName
				# print "Full_Street>",Full_Street
				# print "City ",City
				# print "State>>",State
				# print "Zipcode",Zipcode
				# print "phone",phone
				RawAddress = Full_Street + City + Zipcode + State
				Country ='us'
				Latitude =  response.xpath('//meta[contains(@property,"latitude")]/@content').extract_first(default = "None").strip()
				Longitude = response.xpath('//meta[contains(@property,"longitude")]/@content').extract_first(default = "None").strip()

				DataSource = BrandName
				Category = None

				key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
				item_dict = {}
				for key in key_list:
					# print key
					item_dict[key] = locals()[key]
					
				item['rows'] = item_dict
				yield item
			# except:
				# text_file = open("safeway.txt", "w")
				# text_file.write("Failed Url: %s" % response.url)
				# text_file.close()

		elif '7-eleven.com/' in response.url:
			time.sleep(random.randint(3,7))

			parent = response.xpath('//*[@id="stores_listing"]/div/div[4]/div/div/div/table/tr[position()>1]')
			for par in parent:
				StoreName ="Store #" +"".join(par.xpath('td[2]/a/text()').extract())
				print StoreName	

				Full_Street = "".join(par.xpath('td[5]/text()').extract())
				
				City = "".join(par.xpath('td[6]/text()').extract())
				State =  "".join(par.xpath('td[7]/text()').extract())
				Zipcode =  "".join(par.xpath('td[8]/text()').extract())
				PhoneNumber =  "".join(par.xpath('td[10]/a/text()').extract())
				
				BrandID = "None"
				BrandName = '7eleven'


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
				Category = None

				key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
				item_dict = {}
				for key in key_list:
					# print key
					item_dict[key] = locals()[key]
					
				item['rows'] = item_dict
				yield item


		elif "24hourfitness" in response.url:

			data = json.loads(response.body_as_unicode())
			for i in range(len(data['groupClubs'])):
				for key in range(len(data['groupClubs'][i]['clubs'])):
					StoreName = data['groupClubs'][i]['clubs'][key]['clubName']
					Full_Street = data['groupClubs'][i]['clubs'][key]['clubAddressStreet']
					City = data['groupClubs'][i]['clubs'][key]['clubAddressCity']
					State = data['groupClubs'][i]['clubs'][key]['clubAddressState']
					Zipcode = data['groupClubs'][i]['clubs'][key]['clubAddressZip']
					Latitude = data['groupClubs'][i]['clubs'][key]['clubAddressLatitude']
					Longitude = data['groupClubs'][i]['clubs'][key]['clubAddressLongitude']
					PhoneNumber = data['groupClubs'][i]['clubs'][key]['clubPhoneNumber']
					BrandID = "None"
					BrandName = '24hourfitness'

					RawAddress = Full_Street + City + Zipcode + State
					Country ='us'

					DataSource = BrandName
					Category = None

					key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
					item_dict = {}
					for key in key_list:
						# print key
						item_dict[key] = locals()[key]
						
					print item_dict
					item['rows'] = item_dict
					yield item

					







# # 				# print item


# 		elif "northface" in response.url:
# 			res = requests.get(response.url)
# 			soup = BeautifulSoup(res.text.encode('utf-8'))
# 			pois = soup.find_all('poi')
# 			for poi in pois:
# 				StoreName  = poi.find('name').text
# 				Full_Street = poi.find('address1').text
# 				City = poi.find('city').text
# 				Country = poi.find('country').text
# 				Latitude = poi.find('latitude').text
# 				Longitude = poi.find('longitude').text
# 				PhoneNumber = poi.find('phone').text
# 				Zipcode = poi.find('postalcode').text
# 				State = poi.find('state').text

# 				BrandID = 4226
# 				print StoreName
# 				print Full_Street
# 				BrandName ='northface'

# 		elif "thefreshmarket" in response.url:
# 			try:

# 				address_block = response.xpath('//dd[@id="store_address"]/strong/text()').extract()
			
# 				Full_Street = address_block[0].strip()
# 				print Full_Street
# 				second_block  = address_block[1].split(',')
# 				City = second_block[0].strip()
# 				second_block  = address_block[1].split(',')
# 				State = second_block[1].strip().split()[0]
# 				Zipcode = second_block[1].strip().split()[1]
# 				BrandID = 4048
# 				Latitude = None
# 				Longitude = None
# 				StoreName = 'Fresh_Market'
# 				BrandName = 'Fresh_Market'
# 				Category  = None
# 				DataSource = BrandName
# 				Country ='US'
# 				PhoneNumber = response.xpath('//dd[@id="store_phone"]/strong/text()').extract()
# 				PhoneNumber =PhoneNumber[1].strip() if PhoneNumber else None
# 				RawAddress = Full_Street + " "+ City + State + " " + Zipcode 

# 				final_db   = [BrandName, StoreName, RawAddress, Full_Street, City, State, Zipcode, PhoneNumber, BrandID, Longitude, Latitude, Category, DataSource, Country]
# 				print final_db
# 				key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
# 				item_dict = {}
# 				for key in key_list:
# 					# print key
# 					item_dict[key] = locals()[key]
# 				item['rows'] = item_dict

# 				yield item


# 			except:
# 				text_file = open("fresh_market.txt", "w")
# 				text_file.write("Failed Url: %s" % response.url)
# 				text_file.close()


# 		elif "verizon.com" in response.url:
# 			address = response.xpath('//*[@id="ghfbodycontent"]/div/div[1]/table[1]/tbody/tr')
# 			for add in  address:
# 				StoreName1 = add.xpath('td[1]/text()[1]').extract()
# 				try:
# 					StoreName = add.xpath('td[1]/text()[1]').extract_first()
# 					PhoneNumber = add.xpath('td[3]/text()[1]').extract_first()
# 					print PhoneNumber
# 					Full_Street = add.xpath('td[1]/text()[2]').extract_first(default='None').strip()
# 					print StoreName
# 					print Full_Street
# 					# print  add.xpath('td[1]/text()[3]').extract()[0].strip()
# 					second_block = add.xpath('td[1]/text()[3]').extract()[0].strip().split(',')
# 					City = second_block[0].strip()
# 					# print City
# 					State = second_block[1].split()[0]
# 					Zipcode = second_block[1].split()[1]
# 					BrandID = 97
# 					Latitude = None
# 					Longitude = None

# 					Category  = None
# 					BrandName ='verizon'
# 					DataSource = BrandName
# 					Country ='US'
# 					RawAddress = Full_Street + " "+ City + State + " " + Zipcode
# 					final_db   = [BrandName, StoreName, RawAddress, Full_Street, City, State, Zipcode, PhoneNumber, BrandID, Longitude, Latitude, Category, DataSource, Country]
# 					print final_db
# 					key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
# 					item_dict = {}
# 					for key in key_list:
# 						# print key
# 						item_dict[key] = locals()[key]
# 					item['rows'] = item_dict

# 					yield item
# 				except:
# 					text_file = open("whataburger.txt", "w")
# 					text_file.write("Purchase Amount: %s" % StoreName1)
# 					text_file.close()

# 		elif "whataburger" in response.url:

# 			StoreName = response.xpath('//ul[@class="stores"]/li/h4/text()').extract_first(default = None).strip()
			
		
# 			BrandName ='whataburger'
# 			Full_Street = response.xpath('//ul[@class="stores"]/li/p/text()').extract_first(default = None).strip()
# 			print Full_Street

# 			second_block = response.xpath('//ul[@class="stores"]/li/p/text()').extract()[1].strip().split(',')
# 			print second_block
# 			City = second_block[0].strip()
# 			State = second_block[1].split()[0]
# 			Zipcode = second_block[1].split()[1]
# 			BrandID = 2124
# 			PhoneNumber = None
# 			# Latitude = None
# 			# Longitude = None

# 			# Category  = None
# 			# DataSource = BrandName
# 			# Country ='US'
# 			# PhoneNumber = None
# 			# RawAddress = Full_Street + " "+ City + State + " " + Zipcode
# 			# final_db   = [BrandName, StoreName, RawAddress, Full_Street, City, State, Zipcode, PhoneNumber, BrandID, Longitude, Latitude, Category, DataSource, Country]
# 			# print final_db
# 			# key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
# 			# item_dict = {}
# 			# for key in key_list:
# 			# 	# print key
# 			# 	item_dict[key] = locals()[key]
# 			# item['rows'] = item_dict

# 			# yield item
# 				# except:
# 				# 	text_file = open("whataburger.txt", "w")
# 				# 	text_file.write("Purchase Amount: %s" % StoreName1)
# 				# 	text_file.close()

 





# 				# except:
# 				# 	pass




# 				# break

# 		elif "ikea.com" in response.url:

# 			chromedriver = "/home/deepak/Desktop/chromedriver"
# 			os.environ["webdriver.chrome.driver"] = chromedriver
# 			driver = webdriver.Chrome(chromedriver)
# 			driver.get(response.url)
# 			elem = driver.find_elements_by_xpath('//select[@id="localStore"]/option')
# 			for ele in elem:
# 				urls= ele.get_attribute('value')
# 				base_url ='http://www.ikea.com'
# 				url  = base_url + urls
# 				yield Request(url = url, callback = self.parse_link)
# 				# break



# 	def parse_link(self, response):

# 		Raw_Address = "".join(response.xpath('//div[@class="leftColumn toleft"]/div[2]/text()').extract()).replace('\n',' ').encode('utf-8').strip().upper()
		
# 		addresses = pyap.parse(Raw_Address, country='US')
# 		if len(addresses) ==0:
# 			text_file = open("Output.txt", "w")
# 			text_file.write("Purchase Amount: %s" % address_block)
# 			text_file.close()
# 		else:
# 			for address in addresses:
				
# 				Full_Street = (address.as_dict())['full_street']
# 				City = (address.as_dict())['city']
# 				State = (address.as_dict())['region1']
# 				Zipcode = (address.as_dict())['postal_code']
# 				phone = re.findall(r'[(]*\d{3}[)]*[\s\-\.]*[(]*\d{3}[)]*[\s\-\.]*[(]*\d{4}[)]*|\d{10}',Raw_Address)
# 				PhoneNumber = phone[0] if phone else None

# 				BrandID = 52
# 				BrandName = 'ikea'

# 				RawAddress = Full_Street + City + Zipcode + State
# 				Country ='us'
# 				Latitude = None
# 				Longitude = None
# 				Category = None
# 				DataSource = BrandName
# 				StoreName = "".join(response.xpath('//div[@class="currentStore"]/text()').extract()).strip()

# 				final_db   = [BrandName, StoreName, RawAddress, Full_Street, City, State, Zipcode, PhoneNumber, BrandID, Longitude, Latitude, Category, DataSource, Country]
# 				print len(final_db)


# 				'''Creating Table By Brand Name'''
# 				import MySQLdb
# 				con = MySQLdb.connect(host ="localhost", user="root",passwd="root",db="Test", use_unicode=True,charset="utf8")
				
# 				# Final_DB = []
# 				# for final in final_db:
# 				# 	Final_DB.append(final.encode('utf-8'))


# 				with con:
# 					cur=con.cursor()
# 					create_table = ('CREATE TABLE if NOT EXISTS ' + str(BrandName) +'  LIKE TestDB;')
# 					print create_table
# 					cur.execute(create_table)
# 					con.commit()

# 					''''''''''''''''INSERT into Table by Brand Name'''''''''''''''

# 					cur.execute('''INSERT IGNORE INTO ''' + str(BrandName)  + ''' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', final_db) #### Number of coulms input
		
# 					con.commit()


# '''