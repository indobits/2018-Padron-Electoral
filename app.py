
# .env

from dotenv import load_dotenv
load_dotenv(verbose=True)

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

import os
mysql_user = os.getenv('MYSQL_USER')
mysql_pass = os.getenv('MYSQL_PASS')
mysql_host = os.getenv('MYSQL_HOST')
mysql_port = os.getenv('MYSQL_PORT')
mysql_db = os.getenv('MYSQL_DB')

# Work

from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests as req
from sqlalchemy import create_engine
from itertools import cycle

engine = create_engine('mysql+mysqldb://{0}:{1}@{2}:{3}'.format(mysql_user,mysql_pass,mysql_host,mysql_port))

# Create Database

dbs = engine.execute('SHOW DATABASES;')
dbs = [x[0] for x in dbs]

if mysql_db not in dbs:
	engine.execute('CREATE DATABASE {0}'.format(mysql_db))
	print('Created database {0}'.format(mysql_db))

engine = create_engine('mysql+mysqldb://{0}:{1}@{2}:{3}/{4}'.format(mysql_user,mysql_pass,mysql_host,mysql_port,mysql_db))
connection = engine.connect()

# Create Table

from sqlalchemy import Column,MetaData,Table,VARCHAR
metadata = MetaData()

stg_persons = Table('stg_persons',metadata,
	Column('name',VARCHAR(1000)),
	Column('lastname',VARCHAR(1000)),
	Column('dni',VARCHAR(1000)))
metadata.create_all(engine)
#print(engine.table_names())

stg_persons = Table('stg_persons',metadata,autoload=True,autoload_with=engine)
# pylint: disable=E1120
#stmt = stg_persons.delete().where(1==1); connection.execute(stmt)

# Scraping

def get_proxies():
	res = req.get('https://free-proxy-list.net')
	soup = bs(res.text,'html.parser')
	trs = soup.find(id='proxylisttable').findAll('tr')
	proxies = []
	for tr in trs:
		tds = tr.findAll('td')#; tds and print(tds)
		tds and proxies.append([td.text for i,td in enumerate(tds) if(i in(0,1,3,6))])

	proxies = list(filter(lambda proxy: proxy[2] in('Brazil','Colombia','Peru') and proxy[3] == 'yes', proxies))
	proxies = ["{0}:{1}".format(proxy[0],proxy[1]) for proxy in proxies]
	return proxies

#proxy_pool = cycle(proxies)#; pprint(proxy_pool)

import random,sys

i = 40000000
while i < 50000000:
	print('DNI: {0}'.format(i))
	#proxies = cycle(get_proxies()); proxy = next(proxies); print(proxy)
	proxies = get_proxies(); index = random.randint(0,len(proxies)-1); proxy = proxies[index]; print('Proxy: {0}'.format(proxy))
	try:
		res = req.post('https://padron.americatv.com.pe',data={'dni':str(i).zfill(8)},proxies={'https':proxy})
		print('Status: {0}'.format(res.ok))
		soup = bs(res.text,'html.parser')
		if(soup.find(id='nameData')):
			name = soup.find(id='nameData').get('value')
			lastname = soup.find(id='lastnameData').get('value')
			dni = soup.find(id='dniData').get('value')
			# pylint: disable=E1120
			stmt = stg_persons.insert().values(name=name,lastname=lastname,dni=dni)
			connection.execute(stmt)
		i += 1
	except:
		print(sys.exc_info())
