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
from Storelocator.items import StorelocatorItem
class VersionWirelss(scrapy.Spider):
	name = 'verizon'
	start_urls =['https://www.verizonwireless.com/stores/']

	# start_urls = ['https://www.verizonwireless.com/stores/alabama/alabaster/alabaster-1135614/']

	def parse(self, response):
		category ='verizonwireless'
		links = response.xpath('//div[@id="cityStateLinks"]/div/ul/li/a/@href').extract()
		
		for link in links:
			yield Request(url = link, callback = self.parse_link,meta ={'category':category})
		

	def parse_link(self, response):
		link = response.xpath('//ul[@id="cityList"]/li/a/@href').extract()
		base ="https://www.verizonwireless.com"

		for li in link:
			li =base +li
			yield Request(url = li, callback = self.parse_next, meta ={'category':response.meta['category']})

	def parse_next(self, response):

		final_urls = response.xpath('//address[@class="big-add-text"]/span/a/@href').extract()
		for final_url in final_urls:
			base ="https://www.verizonwireless.com"
			final_url = base + final_url
			yield Request(url = final_url, callback = self.parse_details, meta ={'category':response.meta['category']})

	def parse_details(self, response):

		try:
			item = StorelocatorItem()
			print response.url
			# category = response.meta['category']
			StoreName = response.xpath('//div[@class="store-info-details"]/h1/text()').extract_first(default = None)
			Full_Street = response.xpath('//address[@class="big-add-text"]/span[1]/text()').extract_first(default = None)
			# print StoreName
			# print Full_Street
			PhoneNumber = response.xpath('//address[@class="big-add-text"]/span[3]/text()').extract_first(default = None)

			second_block = response.xpath('//address[@class="big-add-text"]/span[2]/text()').extract()[0].strip().split(',')
			
			City = second_block[0].strip()
			# # print City
			State = second_block[1].strip()
			Zipcode = second_block[2].strip()
			BrandID = 97
			Latitude = None
			Longitude = None

			Category  = 'verizonwireless'
			BrandName ='verizonwireless'
			DataSource = BrandName
			Country ='US'

			RawAddress = Full_Street + " "+ City + State + " " + Zipcode
			final_db   = [BrandName, StoreName, RawAddress, Full_Street, City, State, Zipcode, PhoneNumber, BrandID, Longitude, Latitude, Category, DataSource, Country]
			print final_db
			key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
			item_dict = {}
			for key in key_list:
				item_dict[key] = locals()[key]
			item['rows'] = item_dict

			yield item

		except:
			text_file = open("versionwireless.txt", "w")
			text_file.write("Failed urls : %s" % response.url)
			text_file.close()

		# parents = response.xpath('//address[@class="big-add-text"][1]')
		# for parent in parents:
		# 	# StoreName  = 
		# 	Full_Street = parent.xpath('span[1]/text()').extract_first()

		# 	# print StoreName
		# 	print Full_Street
			
			# City = "".join(parent.xpath('div//span[@class="locality"]/text()').extract())
			# State =  "".join(parent.xpath('div//span[@class="region"]/text()').extract())
			# Zipcode =  "".join(parent.xpath('div//span[@class="postal-code"]/text()').extract())
			# PhoneNumber =  "".join(parent.xpath('div/span[@itemprop="telephone"]/text()').extract())
			
			# BrandID = 97
			# BrandName = 'biglots'


			# # print "StoreName",StoreName
			# # print "Full_Street>",Full_Street
			# # print "City ",City
			# # print "State>>",State
			# # print "Zipcode",Zipcode
			# # print "phone",phone
			# RawAddress = Full_Street + City + Zipcode + State
			# Country ='us'
			# Latitude = None
			# Longitude = None

			# DataSource = BrandName

			# key_list = ["BrandName", "StoreName", "RawAddress", "Full_Street", "City", "State", "Zipcode", "PhoneNumber", "BrandID", "Longitude", "Latitude", "Category", "DataSource", "Country"]
			# item_dict = {}
			# for key in key_list:
			# 	# print key
			# 	item_dict[key] = locals()[key]
				
			# item['rows'] = item_dict
			# yield item

