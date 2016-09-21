# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

con = MySQLdb.connect(host ="localhost", user="root",passwd="root",db="Test")
cursor =con.cursor()

class AllbusinessstorePipeline(object):
	def process_item(self, item, spider):
		business_name = item['business_name']
		address = item['address'] 
		city = item['city']
		state = item['state']
		zipcode = item['zipcode']
		country = item['country']
		phone = item['phone']
		# latitude = item['latitude']	
		# longitude = item['longitude']
		# address_after_parser = item['address_after_parser']
		with con:
			cur=con.cursor()
			query='INSERT into poi_data values("%s","%s","%s","%s","%s","%s","%s")'%(business_name,address,city,state,zipcode,country,phone)
			print "query>>>>>.",query
			cur.execute(query)
			con.commit()



		return item

