from bs4 import BeautifulSoup
import requests
import json
import MySQLdb
import datetime
import time
import random
con = MySQLdb.connect(host ="localhost", user="root",passwd="root",db="Test", use_unicode=True,charset="utf8")
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


# for st in states:
# 	url ="https://www.walmart.com/store/ajax/finder?location="+str(st)+"&is_search=true"
# 	res = requests.get(url)
# 	time.sleep(random.randint(2, 4))
# 	soup = res.text.encode('utf-8')
# 	data =json.loads(soup)
# 	for i in range(len(data['stores'])):
# 		time.sleep(random.randint(2, 5))
# 		BrandName = data['stores'][i]['storeType']['displayName']
# 		Full_Street = data['stores'][i]['address']['address1']
# 		City = data['stores'][i]['address']['city']
# 		State = data['stores'][i]['address']['state']
# 		try:
# 			Zipcode = data['stores'][i]['address']['postalCode']
# 		except:
# 			Zipcode = "None"
# 		try:
# 			PhoneNumber = data['stores'][i]['phone']
# 		except:
# 			PhoneNumber = "None"
# 		try:
# 			Latitude = data['stores'][i]['geoPoint']['latitude']
# 		except:
# 			Latitude = "None"
# 		try:
# 			Longitude = data['stores'][i]['geoPoint']['longitude']
# 		except:
# 			Longitude = "None"

# 		StoreName = City + " " + BrandName

# 		BrandName = BrandName.replace("'","").replace(" ","")

# 		ids = data['stores'][i]['id']	
# 		print BrandName
# 		print Full_Street
# 		print City
# 		print State
# 		print Zipcode
# 		print StoreName
# 		print ids
# 		print PhoneNumber
# 		print Latitude
# 		print Longitude

# 		string_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# 		last_update = datetime.datetime.strptime(string_time, "%Y-%m-%d %H:%M:%S")
# 		RawAddress = Full_Street + City + Zipcode + State


# 		final_db   = ['None',BrandName, StoreName,Full_Street, City, State, Zipcode, 'US',PhoneNumber,Latitude,Longitude,RawAddress,last_update,'None', 'None']
# 		print final_db,len(final_db)

# 		with con:
# 			cur=con.cursor()
# 			create_table = ('CREATE TABLE if NOT EXISTS ' + str(BrandName) +'  LIKE TestDB;')
# 			# print create_table
# 			cur.execute(create_table)
# 			con.commit()

# 			''''''''''''''''INSERT into Table by Brand Name'''''''''''''''

# 			cur.execute('''INSERT IGNORE INTO ''' + str(BrandName)  + ''' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', final_db) #### Number of coulms input
# 			con.commit()





