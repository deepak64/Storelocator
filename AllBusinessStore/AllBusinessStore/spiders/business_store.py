# encoding: utf-8
import scrapy
import os
from pyvirtualdisplay import Display
import time 
from scrapy.http import Request
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
from bs4 import BeautifulSoup
from AllBusinessStore.items import AllbusinessstoreItem
sleep_time = 3
import pyap
import MySQLdb
import json
import csv
import logging
import random
from scrapy.utils.log import configure_logging
con = MySQLdb.connect(host ="localhost", user="root",passwd="root",db="Test",use_unicode=True,charset="utf8")
from slugify import slugify
import usaddress
import datetime

# display = Display(visible=0, size=	(800, 600))
# self.display.start()
# chromeself.driver = os.path.dirname(__file__).replace("/spiders","")+"/chromeself.driver"
# os.environ["webself.driver.chrome.self.driver"] = chromeself.driver
# self.driver = webself.driver.Chrome(chromeself.driver)
# # self.driver = webself.driver.Firefox()
# self.driver.maximize_window()	

# self.driver.set_window_size(1120, 550)


class BusinessStoreClass(scrapy.Spider):
	name = "all_store"
	# allowed_domains = ['ebay.com']
	configure_logging(install_root_handler=False)
	logging.basicConfig(
	filename='log.txt',
	format='%(levelname)s: %(message)s',
	level=logging.INFO
	)
	start_urls =[#"http://www.walgreens.com/storelocator/find.jsp",
	# "http://www.wholefoodsmarket.com/stores/list",
	# "http://local.biglots.com/search",
	# "http://www.bestwestern.com/#",
	# "https://www.walmart.com/store/finder",
	# "http://www.homedepot.com/StoreFinder/",
	# "https://www.mcdonalds.com/us/en-us/restaurant-locator.html",
	# "https://www.lowes.com/store/",
	# "https://www.7-eleven.com/locator",
	# "https://find.wendys.com/",
	# "https://www.tacobell.com/locations",
	"https://www.dollartree.com/custserv/custserv.jsp?pageName=StoreLocations"
	]

	def __init__(self):
		# self.display = Display(visible=1, size=(800, 600))
		# self.display.start()
		chromedriver = "/home/deepak/Desktop/chromedriver"
		os.environ["webdriver.chromedriver"] = chromedriver
		self.driver = webdriver.Chrome(chromedriver)
		# self.self.driver = webself.driver.Firefox()
		self.driver.maximize_window()
		#self.self.driver = webself.driver.PhantomJS()

	
	# def start_requests(self):
	# 	Input_Country_Brands = os.path.dirname(__file__).replace("/spiders","")+"/Zipcode_input.json"
	# 	with open(Input_Country_Brands) as fs:
	# 		Country_Brands = json.loads(fs.read())
	# 		print Country_Brands
	# 		try:
	# 			Country=raw_input('Enter Country : ')
	# 		except KeyError as e:
	# 			print "COuntry is not found in our database please input another country"
	# 		try:
	# 			for brand_name, store_url in Country_Brands[Country].iteritems():
	# 				yield Request(url =Country_Brands[Country][raw_input(brand_name)], callback = self.parse,meta ={'brand_name':brand_name})
	# 				break

	# 		except KeyError:
	# 			print "Enter Another Brand_name"
	# 	# Country=raw_input('Enter Country : ')
		# if Country in Country_Brands.keys():
		# 	BrandName = raw_input ("Country Exists, Please Enter Brand Name: ")
		# 	print ".>>>>>>>>>>>>>>>",Country_Brands[Country]["BrandName"]
			# if BrandName in Country_Brands[Country]["BrandName"]:
	# 			BrandUrl = raw_input('Brand Exists Enter BrandUrl : ')
	# 			yield Request(url = BrandUrl, callback = self.parse, meta ={'BrandName':BrandName})
	# 		else:
	# 			print "Please Enter Another Brand Name...." 

	# 	else:
	# 		print "Please enter Another country...."  

	def pagination_block(self,body,url):
		print "=============================================================="

		if 'class="next"' in body.lower() or 'title="next"' in body.lower()  or "next button" in body.lower() or "next</a" in body.lower():
			while True:

				print "helllo>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
				try:
					next = self.driver.find_element_by_xpath('//*[contains(translate(@class,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"next")]/a')
					time.sleep(random.randint(3, 6))
					next.click()
					time.sleep(random.randint(3, 8))
					self.extractaddress(self.driver.page_source,self.driver.current_url)

				except NoSuchElementException as e:
					try:
						print "trrrrrrrrrrrrrrrrrrrrrrrryyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy111111111111111111"
						next = self.driver.find_element_by_xpath('//a[contains(translate(@class,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"next")]')
						time.sleep(random.randint(3, 6))
						next.click()
						time.sleep(random.randint(3, 9))
						self.extractaddress(self.driver.page_source,self.driver.current_url)

					except NoSuchElementException as e:
						try:
							print "title class Text"
							next = self.driver.find_element_by_xpath('//a[contains(translate(@title,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"next")]')
							time.sleep(random.randint(3, 5))
							next.click()
							time.sleep(random.randint(5, 12))
							self.extractaddress(self.driver.page_source,self.driver.current_url)

						except NoSuchElementException as e:
							try:
								print "A tag Text()"
								next = self.driver.find_element_by_xpath("//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'next')]")
								time.sleep(random.randint(5, 9))
								next.click()
								time.sleep(random.randint(5, 9))
								self.extractaddress(self.driver.page_source,self.driver.current_url)
							except NoSuchElementException as e:
								try:
									next = self.driver.find_element_by_xpath("//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'load')]")
									time.sleep(random.randint(5, 9))
									next.click()
									time.sleep(random.randint(5, 9))
									self.extractaddress(self.driver.page_source,self.driver.current_url)

								except:
									break

		elif 'view more' in body.lower():
			while True:

				print "View More"
				try:
					next = self.driver.find_element_by_xpath('//button[contains(translate(text(),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"view more")]')
					time.sleep(random.randint(3, 6))
					next.click()
					time.sleep(random.randint(3, 8))
					self.extractaddress(self.driver.page_source,self.driver.current_url)

				except NoSuchElementException as e:
					break
		else:
			print "Next Pagination condition No satisfied"
			self.extractaddress(self.driver.page_source,self.driver.current_url)
			print "terminated Pagination Condition Need to put COndition For Pagination Block"

		# elif 'show more' in body.lower() or 'showmore' in response.body.lower() or "view more" in  response.body.lower() or "see more" in response.body.lower():
		# 	print "SHOOWWWWWWWWWWWWWWWWWMOREEEEEEEEEEEEEEEEEEEEEEEEEE button"
		# 	if "americangreetings" in self.driver.current_url:
		# 		print "hellllllllllllllllllllllllllloooooooooooooooooo"
		# 		print "self.driver>>>>>>>>>>>>>.", self.driver.page_source
				 
		# 		yield Request(url = self.driver.current_url, meta ={'result_after_pagination':self.driver.page_source },callback = self.parse_details)
		# 	else:
		# 		while True:
		# 			try:
		# 				element = wait.until(
		# 				EC.presence_of_element_located((By.XPATH, '//button[contains(text(),"View More")]'))
		# 				)
		# 				self.driver.implicitly_wait(5)
		# 				ActionChains(self.driver).move_to_element(element).click().perform()
		# 			except:
		# 				break

		# elif "thomaspink.com" in url:
		# 	url_list = sel.xpath('//a[@class="article_store_link"]/@href').extract()
		# 	for url in url_list:
		# 		url ='http://www.thomaspink.com/storefinder/content/fcp-content?' + url
		# 		yield Request(url = url, meta ={'result_after_pagination':self.driver.page_source},callback = self.parse_details)

		# else:
		# 	while True:
		# 		# do the scrolling
		# 		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		# 		try:
		# 			wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Loading')]")))
		# 		except TimeoutException:
		# 			break  # not more posts were loaded - exit the loop

		# else:
		# 	print "there is no pagination>>>>>>>>>>>>>block >>>>>>>>>>>>>>>>>"
		# 	yield Request(url = self.driver.current_url, meta ={'result_after_pagination':self.driver.page_source},callback = self.parse_details)

	def extractaddress(self,body,url):
		print "heloooooooooooooooooooooooooooooooo"
		sel = Selector(text=body)
		'''regex for extracting brandname from response.url'''

		BrandName_from_url = re.findall(r'(\w+).com', url)[0]
		BrandName_from_url = BrandName_from_url.replace('-','')
		print BrandName_from_url
		''''Reading csv for extracting address block '''
		reader =csv.reader(open('/home/deepak/configFile.csv', 'rb'))
		reader.next()
		for row in reader:
			BrandName_from_config = row[0]
			Full_INFO_Xpath = row[3]
			if BrandName_from_url == BrandName_from_config:
				BrandName = BrandName_from_config
				time.sleep(random.randint(7, 11))
				Full_INFO_Xpaths = self.driver.find_elements_by_xpath(Full_INFO_Xpath)
				for Full_INFO_Xpath in Full_INFO_Xpaths:
					print Full_INFO_Xpath.text
					StoreName = Full_INFO_Xpath.text.split('\n')[0]
					if len(StoreName)<=3:
						if StoreName.isdigit():
							StoreName = Full_INFO_Xpath.text.split('\n')[1]
						else:
							StoreName = BrandName
					else:
						StoreName = StoreName

					string_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					last_update = datetime.datetime.strptime(string_time, "%Y-%m-%d %H:%M:%S")
	
					Raw_Address = Full_INFO_Xpath.text.replace('\n',' ').encode('utf-8').strip().upper()
					addresses = pyap.parse(Raw_Address, country='US')
					# if not addresses:
					# 	full_address = dict(usaddress.parse(Raw_Address))
					# 	address_dict = {}
					# 	PlaceName = []
					# 	StreetAddress = []
					# 	for k, j in full_address.iteritems(): 

					# 		if j!= 'Recipient':
					# 			if j=='StateName':
					# 				address_dict['state'] = k
					# 			elif j== 'ZipCode':
					# 				address_dict['zipcode'] = k 
								
					# 			elif j=='PlaceName':
					# 				PlaceName.append(k)
					# 		#  
					# 			elif k!='':
					# 				StreetAddress.append(k)
					# 		address_dict['city'] = ' '.join(PlaceName).replace(',','')     
					# 		address_dict['StreetAddress'] = ' '.join(StreetAddress)
					# 			# print address_dict
					# 		Full_street = address_dict['StreetAddress']
					# 		if Full_street_from_web!='None':
					# 			Full_street = Full_street_from_web
					# 		else:
					# 			Full_street = 'None'
					# 		City = address_dict['city']
					# 		try:
					# 			ZipCode = address_dict['zipcode']
					# 		except:
					# 			# try:
					# 			# 	ZipCode = re.findall(r"\d+", Raw_Address)[-1]
					# 			# except:
					# 			ZipCode = 'None'
					# 		try:
					# 			State = address_dict['state']
					# 		except:
					# 			State = 'None'
					# 		phone = ", ".join(re.findall(r'[(]*\d{3}[)]*[\s\-\.]*[(]*\d{3}[)]*[\s\-\.]*[(]*\d{4}[)]*|\d{10}',Raw_Address))
					# 		Full_street = Full_street.replace(phone, '')
					# 	''''''''''''''''INSERT into Table by Brand Name'''''''''''''''
					# 	final_db1 =  [BrandName, StoreName , Raw_Address, Full_street, City, State, ZipCode, phone]
					# 	print final_db1
					# 	import MySQLdb
					# 	con = MySQLdb.connect(host ="localhost", user="root",passwd="root",db="Test", use_unicode=True,charset="utf8")
					# 	with con:
					# 		cur=con.cursor()
					# 		create_table = ('CREATE TABLE if NOT EXISTS ' + str(BrandName) +'  LIKE TestDB;')
					# 		# print create_table
					# 		cur.execute(create_table)
					# 		con.commit()

					# 		cur.execute("INSERT IGNORE INTO " + str(BrandName)  + " values (%s,%s,%s,%s,%s,%s,%s,%s)", final_db1) #### Number of coulms input
					# 		con.commit()
					# else:
					for address in addresses:
						Full_street = (address.as_dict())['full_street']
						City = (address.as_dict())['city']
						State = (address.as_dict())['region1']
						ZipCode = (address.as_dict())['postal_code']
						phone = re.findall(r'[(]*\d{3}[)]*[\s\-\.]*[(]*\d{3}[)]*[\s\-\.]*[(]*\d{4}[)]*|\d{10}',Raw_Address)
						phone = phone[0] if phone else None
						Full_street = re.sub(r'[\d\.]+\s*mi','',Full_street.lower()).strip()
						Full_street = re.sub(r'00 p.m.  ','',Full_street.lower())
						Full_street = Full_street.strip()
						final_db   = ['None',BrandName, StoreName, Full_street, City, State, ZipCode,'US', phone, 'None', 'None', Raw_Address, last_update , 'None', 'None']
						print final_db,len(final_db)
						'''Creating Table By Brand Name'''
						import MySQLdb
						con = MySQLdb.connect(host ="localhost", user="root",passwd="root",db="zip_database", use_unicode=True,charset="utf8")
						with con:
							cur=con.cursor()
							create_table = ('CREATE TABLE if NOT EXISTS ' + str(BrandName) +'  LIKE TestDB;')
							# print create_table
							cur.execute(create_table)
							con.commit()

							''''''''''''''''INSERT into Table by Brand Name'''''''''''''''

							cur.execute('''INSERT IGNORE INTO ''' + str(BrandName)  + ''' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', final_db) #### Number of coulms input
							
							con.commit()



	def parse(self, response):
		# zipcode_file_path = '/home/deepak/newzips_50Miles.csv'
		# with open(zipcode_file_path, 'rb') as csvfile:
		# 	spamreader = csv.reader(csvfile, quotechar='|')
		# 	spamreader.next()
		# 	for row in spamreader:
		

		for zipcode in ['10001','80003']:
		
			self.driver.get(response.url)
			try:
				print "Inside First Zipcode"
				time.sleep(random.randint(9, 13))
				element = self.driver.find_element_by_xpath("//input[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'zip') or contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'post') or contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'location')]")
				time.sleep(random.randint(15, 19))
				element.clear()
				element.send_keys(zipcode)
				time.sleep(random.randint(10, 15))
				element.send_keys(Keys.RETURN)
				time.sleep(random.randint(14, 19))

				results ={'url':self.driver.current_url,
						'page_source':self.driver.page_source}


				self.pagination_block(self.driver.page_source,self.driver.current_url)

				# yield Request(url = self.driver.current_url, callback = self.parse_link, meta ={'results':results})

			except NoSuchElementException as e:
				try:
					print "Inside Second Zipcode"
					time.sleep(random.randint(9, 13))
					element = self.driver.find_element_by_xpath("//input[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'address') or contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'address') or contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'zip') or contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'location')]")
					time.sleep(random.randint(15, 19))
					element.clear()
					time.sleep(random.randint(10, 14))
					element.send_keys(zipcode)
					element.send_keys(Keys.RETURN)
					time.sleep(random.randint(15, 17))
					results ={'url':self.driver.current_url,
						'page_source':self.driver.page_source}
					# yield Request(url = self.driver.current_url, callback = self.parse_link, meta ={'results':results})
					print "k---------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
					self.pagination_block(self.driver.page_source,self.driver.current_url)
				except NoSuchElementException as e:
					raise

