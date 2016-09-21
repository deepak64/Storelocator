# encoding: utf-8
import scrapy
from scrapy.http import Request
import csv
import re
import scrapy
from scrapy.http import Request
import csv
import time
# import MySQLdb as mdb
# con=mdb.connect("localhost","r","","xad_database")
from scrapy.http import FormRequest
import pprint
import MySQLdb
from random import randint
# from time import sleep
con = MySQLdb.connect(host ="localhost", user="root",passwd="root",db="Test")
cursor =con.cursor()
output_csv = csv.writer(open('geodriud_data.csv', 'wb'))
output_csv.writerow(['BrandName','StoreName' , 'RawAddress', 'Full_Street', 'City','State','Zipcode', 'PhoneNumber'])

class geogoidCraw(scrapy.Spider):

	name ='geo'
	# allowed_domains = ["http://easternusa.salvationarmy.org/"]
	start_urls = [
	# "http://www.geodruid.com/intl/en/brands/4995:promod/DE:germany",
	# "http://www.geodruid.com/intl/en/brands/9066:stefanel/DE:germany",
	# "http://www.geodruid.com/intl/en/brands/6419:only/DE:germany",
	# "http://www.geodruid.com/intl/en/brands/6943:engbers/DE:germany"
	# "http://www.geodruid.com/intl/en/brands/6599:edc-by-esprit/DE:germany"
	]
	#"http://www.geodruid.com/intl/en/brands/6931:betty-barclay/DE:germany"]#"http://www.geodruid.com/intl/en/brands/1135:bosch-car-service/DE:germany"]
	# start_urls =[#'http://www.geodruid.com/intl/en/place/1749659-mezger-gmbh-co-kg-autoreparatur-bamberg-deutschland']
	# start_urls =["http://www.geodruid.com/intl/en/brands/268:volkswagen/DE:germany"]


	# def start_requests(self):
	# 	reader = csv.reader(open('/home/deepak/Downloads/GERMANY- CATEGORY SCRAP- FASHION STORES -  Fashion Stores.csv',"rb"))
	# 	reader.next()
	# 	for row in reader:
	# 		urls = row[4]
	# 		if "geodruid" in urls:
	# 			yield Request(url = urls , callback = self.parse)

	# http_handle_list =[302]


	start_urls =['https://www.fressnapf.de/marktfinder/']

	def parse(self, response):

		if 'geodriud' in response.url:
			links = response.xpath('//div[@class="result-list-ctrl"]/ul/li/a/@href').extract()

			if not links:
				yield Request(url = response.url, callback = self.parse_next)
			for link in links:
				link = 'http://www.geodruid.com' + link
				yield Request(url = link, callback = self.parse_next)
		elif 'fressnapf.de' in response.url:
			links = response.xpath('//div[@class="store-list"]/ul/li/a/@href').extract()
			for link in links:
				link = 'https://www.fressnapf.de' + link
				yield Request(url = link, callback = self.parse_next)





	def parse_next(self, response):
		print response.url
		if 'geodriud' in response.url:
			linkss  = response.xpath('//div[@class="poi-lstsq-info-name"]/a/@href').extract()
			# print linkss, len(set(linkss))
			BrandName ="".join(response.xpath('//li[@class="step_just_done"]/a/text()').extract())
			time.sleep(randint(3,7))

			lst = []
			for link in linkss:
				link ='http://www.geodruid.com' + link
				# lst.append(link)

				yield Request(url = link, callback = self.parse_last,meta ={'brand_name':BrandName})
		elif 'fressnapf.de' in response.url:
			links = response.xpath('//a[@class="store-item"]/@href').extract()
			for link in links:
				link = 'https://www.fressnapf.de' + link +'/markt'
				print link
				yield Request(url = link, callback = self.parse_last)




	def parse_last(self, response):

		if 'geodruid' in response.url:
			try:

				BrandName = response.meta['brand_name']
				# BrandName ='hello'
				BussinessName = "".join(response.xpath('//meta[@property="og:title"]/@content').extract()).strip()
				Full_Street = "".join(response.xpath('//meta[@property="og:street-address"]/@content').extract()).strip()
				State = "".join(response.xpath('//meta[@property="og:region"]/@content').extract()).strip()
				Zipcode = "".join(response.xpath('//meta[@property="og:postal-code"]/@content').extract()).strip()
				PhoneNumber = "".join(response.xpath('//meta[@property="og:phone_number"]/@content').extract()).strip()
				Latitude = "".join(response.xpath('//meta[@property="og:latitude"]/@content').extract()).strip()
				Longitude = "".join(response.xpath('//meta[@property="og:longitude"]/@content').extract()).strip()
				City = "".join(response.xpath('//meta[@property="og:locality"]/@content').extract()).strip()
				Country = "".join(response.xpath('//meta[@property="og:country-name"]/@content').extract()).strip()

				
				Raw_Address = Full_Street + City + Zipcode + State
				url = response.url
				# print "urls>>>>>>>>>>>", url 
				# print "BusinesName ",BussinessName

				final_db   = [BrandName, BussinessName,Full_Street, City, State, Zipcode,Country,PhoneNumber,Latitude,Longitude, Raw_Address, url]
				print final_db, len(final_db)

				'''Creating Table By Brand Name'''
				import MySQLdb
				con = MySQLdb.connect(host ="localhost", user="root",passwd="root",db="germany_data", use_unicode=True,charset="utf8")
				
				# Final_DB = []
				# for final in final_db:
				# 	Final_DB.append(final.encode('utf-8'))


				with con:
					cur=con.cursor()
					create_table = ('CREATE TABLE if NOT EXISTS ' + str('geodruid') +'  LIKE GermanyStructure;')
					# print create_table
					cur.execute(create_table)
					con.commit()

					''''''''''''''''INSERT into Table by Brand Name'''''''''''''''

					cur.execute('''INSERT IGNORE INTO ''' + str('geodruid')  + ''' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', final_db) #### Number of coulms input

					con.commit()

			except:
				text_file = open("geodruid.txt", "w")
				text_file.write("Failed Url: %s" % response.url)
				text_file.close()

		elif "fressnapf.de" in response.url:
			# try:
				print "responssnse>>>>", response.url
				BrandName = 'fressnapf'
				# # BrandName ='hello'
				BussinessName = response.xpath('//div[@class="span3 address-description"]/address/text()').extract()
				BussinessName = BussinessName[0].strip() if BussinessName else None
				Full_Street = response.xpath('//div[@class="span3 address-description"]/address/text()').extract()
				Full_Street = Full_Street[1].strip() if Full_Street else None
				Second_block = response.xpath('//div[@class="span3 address-description"]/address/text()').extract()
				Second_block = Second_block[2].strip() if Second_block else None
				Second_block=Second_block.split()
				PhoneNumber = response.xpath('//span[@class="phone calling-link"]/text()').extract_first(default='None').strip()
				try:
					City = Second_block[1].strip()
				except:
					City = None
				try:
					Zipcode = Second_block[0].strip()
				except:
					Zipcode = None

				Latitude = response.xpath('//div[@class="module map row-fluid"]/div/@data-lat').extract_first(default='None')
				Longitude = response.xpath('//div[@class="module map row-fluid"]/div/@data-lng').extract_first(default='None')

				print BussinessName
				print Full_Street
				print City
				print Zipcode
				print Latitude
				print Longitude
				print Zipcode + " " +  City

				State_Lookup = {'BE': 'Berlin', 'RP': 'Rhineland-Palatinate (Rheinland-Pfalz)', 'BB': 'Brandenburg', 'MV': 'Mecklenburg-Western Pomerania', 
				'SH': 'Schleswig-Holstein', 'ST': 'Saxony-Anhalt (Sachsen-Anhalt)', 'SN': 'Saxony (Freistaat Sachsen)', 'HH': 'Hamburg (Freie und Hansestadt Hamburg)', 
				'BW': 'baden-württemberg', 'NI': 'Lower Saxony (Niedersachsen)', 'TH': 'Thuringia (freistaat thuringen)', 
				'SL': 'Saarland', 'HB': 'Bremen (Freie Hansestadt Bremen)', 'NW': 'North Rhine-Westphalia (Nordrhein-Westfalen)', 'BY': 'Bavaria (Freistaat Bayern) ', 
				'HE': 'Hesse (Hessen)','SN':'Sachsen'}
				import sys
				"""LATITUDE LONGITUDE"""
				from geopy.geocoders import Nominatim
				from geopy.geocoders import GeocoderDotUS
				reload(sys)
				sys.setdefaultencoding("utf-8")
				geolocator = Nominatim()
				latlon =  '%s, %s'%(Latitude,Longitude)
				location = geolocator.reverse(latlon,timeout = 60)
				state_geo = location.raw['address']['state']
				# if "deutschland" in location[-1].lower():
					# state_geo = location[-2].strip()
				for key, v in  State_Lookup.iteritems():
				  	value = State_Lookup[key].encode('utf-8')
				  	if  state_geo.lower() in value.lower():
				  		State = key
					  	break
					else:
						State = 'N/A'


				print State


# import re

				Country = 'Germany'

				
				Raw_Address = Full_Street + City + Zipcode + State
				url = response.url
				# print "urls>>>>>>>>>>>", url 
				# # print "BusinesName ",BussinessName

				final_db   = [BrandName, BussinessName,Full_Street, City, State, Zipcode,Country,PhoneNumber,Latitude,Longitude, Raw_Address, url]
				print final_db, len(final_db)

				'''Creating Table By Brand Name'''
				import MySQLdb
				con = MySQLdb.connect(host ="localhost", user="root",passwd="root",db="germany_data", use_unicode=True,charset="utf8")
				
				# Final_DB = []
				# for final in final_db:
				# 	Final_DB.append(final.encode('utf-8'))


				with con:
					cur=con.cursor()
					create_table = ('CREATE TABLE if NOT EXISTS ' + str(BrandName) +'  LIKE GermanyStructure;')
					# print create_table
					cur.execute(create_table)
					con.commit()

					''''''''''''''''INSERT into Table by Brand Name'''''''''''''''

					cur.execute('''INSERT IGNORE INTO ''' + str(BrandName)  + ''' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', final_db) #### Number of coulms input

					con.commit()

			# except:
				# text_file = open("geodruid.txt", "w")
				# text_file.write("Failed Url: %s" % response.url)
				# text_file.close()


	# 	# print BrandName






		

	# 	print "response>>>>>>>>>>>>>>>>>>>>>>>", response.url
	# 	BrandName = response.meta['brand_name']
		


	# 	address_details = response.xpath('//div[@class="poi-address-content"]')

	# 	for add in address_details:
	# 		StoreName = add.xpath('div/h3/text()').extract()
	# 		if StoreName:
	# 			StoreName = StoreName[0]
	# 		else:
	# 			StoreName = None

	# 		Full_Street = add.xpath('div[2]/text()').extract()
	# 		if Full_Street:
	# 			Full_Street = Full_Street[0]
	# 		else:
	# 			Full_Street = None
	# 		Zipcode = add.xpath('div[3]/span[1]/text()').extract()
	# 		if Zipcode:
	# 			Zipcode = Zipcode[0]
	# 		else:
	# 			Zipcode = None
	# 		City = add.xpath('div[3]/span[2]/text()').extract()
	# 		if City:
	# 			City = City[0].strip()
	# 		else:
	# 			City = None

	# 		Country = add.xpath('div[4]/text()').extract()
	# 		if Country:
	# 			Country = Country[0].strip()
	# 		else:
	# 			Country = None

	# 		if StoreName!=None and Full_Street!=None and Zipcode!=None and City!=None and Country!=None:
	# 			RawAddress = StoreName + Full_Street + Zipcode + City + Country

	# 	PhoneNumber = response.xpath('//meta[@property="og:phone_number"]/@content').extract()
	# 	if PhoneNumber:
	# 		PhoneNumber = PhoneNumber[0]
	# 	else:
	# 		PhoneNumber = None

	# 	print 'BrandName', BrandName
	# 	print 'StoreName' , StoreName
	# 	print 'Full_Street' , Full_Street
	# 	print 'Zipcode' , Zipcode
	# 	print 'City' , City
	# 	print 'Country', Country

	# 	print "RawAddress", RawAddress
	# 	State = 'None'


	# 	cur=con.cursor()
		
	# 	query = "INSERT IGNORE into geodruid values('%s','%s','%s','%s','%s','%s','%s','%s')"%(BrandName,StoreName,RawAddress,Full_Street,City,State,Zipcode,PhoneNumber)
	# 	cur.execute(query)
	# 	con.commit()
	#  	Data =  [ BrandName.encode('utf-8').strip(),StoreName.encode('utf-8').strip() , RawAddress.encode('utf-8').strip(), Full_Street.encode('utf-8').strip(), City.encode('utf-8').strip(),State.encode('utf-8').strip(),Zipcode.encode('utf-8').strip(), PhoneNumber.encode('utf-8').strip()]
	# 	output_csv.writerow(Data)
	# 	print Data
	# 	# Data =  [ BrandName.encode('utf-8').strip(),StoreName.encode('utf-8').strip() , RawAddress.encode('utf-8').strip(), FullStreet.encode('utf-8').strip(), City.encode('utf-8').strip(),Zipcode.encode('utf-8').strip(), PhoneNumber.encode('utf-8').strip()]
	# 	# output_csv.writerow(Data)








