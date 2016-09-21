# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import datetime
con = MySQLdb.connect(host ="localhost", user="root",passwd="root",db="Test", use_unicode=True,charset="utf8")

class StorelocatorPipeline(object):
	def process_item(self, item, spider):
		data = item['rows']

		Category = data['Category']
		City = data['City']
		Full_Street = data['Full_Street']
		StoreName = data['StoreName']
		Country = data['Country']
		Zipcode = data['Zipcode']
		Longitude = data['Longitude']
		BrandID = data['BrandID']
		RawAddress = data['RawAddress']
		State = data['State']
		BrandName = data['BrandName']
		PhoneNumber = data['PhoneNumber']
		DataSource = data['DataSource']
		Latitude = data['Latitude']
		string_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		last_update = datetime.datetime.strptime(string_time, "%Y-%m-%d %H:%M:%S")



		final_db   = ['None',BrandName, StoreName,Full_Street, City, State, Zipcode, 'US',PhoneNumber,Latitude,Longitude,RawAddress,last_update,'None', 'None']
		print final_db,len(final_db)
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

			cur.execute('''INSERT IGNORE INTO ''' + str(BrandName)  + ''' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', final_db) #### Number of coulms input
			con.commit()

		return item
