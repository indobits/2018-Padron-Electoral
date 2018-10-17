
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
proxy_act = int(os.getenv('PROXY_ACT'))

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

from sqlalchemy import Column,func,MetaData,Table,DateTime,VARCHAR
metadata = MetaData()

stg_persons = Table('stg_persons',metadata,
	Column('dni',VARCHAR(1000)),
	Column('name',VARCHAR(1000)),
	Column('lastName',VARCHAR(1000)),
	Column('createdAt',DateTime(timezone=True),server_default=func.now())
)
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

	#proxies = list(filter(lambda proxy: proxy[2] in('Brazil','Colombia','Peru') and proxy[3] == 'yes', proxies))
	proxies = list(filter(lambda proxy: proxy[3] == 'yes', proxies))
	proxies = ["{0}:{1}".format(proxy[0],proxy[1]) for proxy in proxies]
	return proxies

import random,sys,time

# pylint: disable=E1111
stmt = stg_persons.select().with_only_columns([func.max(stg_persons.c.dni)])
dniMax = connection.execute(stmt).scalar()
if(dniMax): dniMax = int(dniMax) + 1

i = dniMax or 0
while i < 99999999:
	print('-' * 50)
	print('Fecha y Hora: {0}'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
	try:
		dni = str(i).zfill(8); print('DNI: {0}'.format(dni))
		if(proxy_act):
			proxies = get_proxies()
			index = random.randint(0,len(proxies)-1)
			proxy = proxies[index]
			print('Proxy: {0}'.format(proxy))
			res = req.post('https://padron.americatv.com.pe',data={'dni':dni},proxies={'https':proxy},timeout=(1,1),verify=None)
		else:
			res = req.post('https://padron.americatv.com.pe',data={'dni':dni},timeout=(1,1),verify=None)
		print('Passed: {0}'.format(res.ok))
		soup = bs(res.text,'html.parser')
		if(soup.find(id='nameData')):
			dni = soup.find(id='dniData').get('value')
			name = soup.find(id='nameData').get('value')
			lastName = soup.find(id='lastnameData').get('value')
			# pylint: disable=E1120
			stmt = stg_persons.insert().values(dni=dni,name=name,lastName=lastName)
			connection.execute(stmt)
			print('DNI grabado exitosamente')
		i += 1
	except:
		print(sys.exc_info())
