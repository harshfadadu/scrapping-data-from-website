import requests
from scrapy.http import TextResponse
import datetime as dt
from datetime import datetime
import pandas as pd
import json
import pprint

def moneycontrol(year, main_dict, company, company_code):
	main_dict[company]['moneycontrol'] = {}
	res_title_list = []
	res_date_list = []
	res_subtitle_list = []
	page = 0

	while (True):
		page = page + 1
		print(page)
		# get data from site using scrapy
		site = str('https://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=')+company_code+('&scat=&pageno=')+str(page)+str('&next=0&durationType=Y&Year=')+str(year)+str('&duration=1&news_type=')
		res = requests.get(site)
		response = TextResponse(res.url, body=res.text, encoding='utf-8')
		
		# date & time
		temp_date_list = response.css(".PT3.a_10dgry::text").getall()
		# condition for checking, if this is page contains data
		if len(temp_date_list) == 0:
			print('break')
			break
		# storing date & time
		res_date_list.extend([datetime.strptime((i.split('|')[1][1:12]+' '+i.split('|')[0][0:-1]), '%d %b %Y %I.%M %p') for i in temp_date_list])
		
		# title
		temp_title_list = response.xpath('//strong/text()').extract()
		if len(temp_date_list) == 20:
			res_title_list.extend(temp_title_list[11:31])
		else:
			res_title_list.extend(temp_title_list[11:31-(20-len(temp_date_list))])
			
		# subtitle
		temp_subtitle_list = response.css(".PT3::text").getall()
		res_subtitle_list.extend(temp_subtitle_list[1::2])

	# checks
	if len(res_title_list) == len(res_date_list) == len(res_subtitle_list):
		print("All ok.")
	else:
		print("Check Failed!!")

	main_dict[company]['moneycontrol']['Title'] = res_title_list
	main_dict[company]['moneycontrol']['Date & Time'] = res_date_list
	main_dict[company]['moneycontrol']['Subtitle'] = res_subtitle_list
	return main_dict

def businesstoday(year, main_dict, company, company_code):
	main_dict[company]['BusinessToday'] = {}
	res_date_list = []
	res_title_list = []
	res_subtitle_list = []
	page = 0

	while (True):
	    page = page + 1
	    #print(page)
	    flag = 0
	    # get data from site using scrapy
	    site = str('https://www.businesstoday.in/search.jsp?searchword=')+company_code+('&page=')+str(page)
	    res = requests.get(site)
	    response = TextResponse(res.url, body=res.text, encoding='utf-8')
	    
	    # date & time
	    temp_date_list1 = response.xpath('//fieldset/span/text()').extract()
	    temp_date_list = []
	    for i in temp_date_list1:
	        try:
	            temp_date_list.append(datetime.strptime(' '.join(i.replace(' ','').split(',')[-2:]), "%B%d %Y"))
	        except:
	            continue
	    # condition for checking, if data for "year" is over
	    if all(int(i.year)==(year-1) for i in temp_date_list):
	    	print(page)
	        print('break')
	        break
	    # storing date & time
	    if all(int(i.year)==year for i in temp_date_list):
	        res_date_list.extend(temp_date_list)
	    elif any(int(i.year)==year for i in temp_date_list):
	        flag = 1
	        start = [i for i, e in enumerate([int(i.year) for i in temp_date_list]) if e == year][0]
	        end = [i for i, e in enumerate([int(i.year) for i in temp_date_list]) if e == year][-1] + 1
	        res_date_list.extend(temp_date_list[start:end])
	    else:
	    	# skipping as this page does not contain data for "year"
	        #print('Skip...')
	        continue
	    print(page)

	    # title
	    temp_title_list = response.xpath('//div/h2/a/text()').extract()
	    if flag == 0:
	        res_title_list.extend(temp_title_list)
	    else:
	        res_title_list.extend(temp_title_list[start:end])

	# checks
	if len(res_title_list) == len(res_date_list):
	    print("All ok.")
	else:
	    print("Check Failed!!")

	main_dict[company]['BusinessToday']['Title'] = res_title_list
	main_dict[company]['BusinessToday']['Date & Time'] = res_date_list
	main_dict[company]['BusinessToday']['Subtitle'] = res_subtitle_list
	return main_dict

def IIFL(year, main_dict, company, company_code):
	total_pages = 207
	main_dict[company]['IIFL'] = {}
	res_title_list = []
	res_date_list = []
	res_subtitle_list = []

	for page in range(148, total_pages+1):
		print(page)
		flag = 0
		site = str('https://www.indiainfoline.com/search/news/')+company_code+('/')+str(page)
		res = requests.get(site)
		response = TextResponse(res.url, body=res.text, encoding='utf-8')
		
		# date&time
		temp_date_list = response.css(".source.fs12e::text").extract()
		try:
			temp_date_list = [datetime.strptime(str(i.replace(' ','').replace('\n','').replace('\r','').split('|')[2])+" "+str(i.replace(' ','').replace('\n','').replace('\r','').split('|')[1][6:-3]), "%B%d,%Y %H:%M") for i in temp_date_list]
		except:
			temp_date_list = [datetime.strptime(str(i.replace(' ','').replace('\n','').replace('\r','').split('|')[2]), "%B%d,%Y") if(len(i.replace(' ','').replace('\n','').replace('\r','').split('|'))==3) else dt.datetime(1, 1, 1, 1, 1) for i in temp_date_list]
		if all(int(i.year)==year for i in temp_date_list):
			res_date_list.extend(temp_date_list)
		elif any(int(i.year)==year for i in temp_date_list):
			flag = 1
			start = [i for i, e in enumerate([int(i.year) for i in temp_date_list]) if e == year][0]
			end = [i for i, e in enumerate([int(i.year) for i in temp_date_list]) if e == year][-1] + 1
			res_date_list.extend(temp_date_list[start:end])
		else:
			continue
		print("process!")
		# title
		temp_title_list = response.xpath('//a/text()').extract()
		if flag == 0:
			res_title_list.extend(temp_title_list[143:162])
		else:
			res_title_list.extend(temp_title_list[(143+start):(162-(19-end))])

	# checks
	if len(res_title_list) == len(res_date_list):
		print("All ok.")
	else:
		print("Check Failed!!")

	main_dict[company]['IIFL']['Title'] = res_title_list
	main_dict[company]['IIFL']['Date & Time'] = res_date_list
	main_dict[company]['IIFL']['Subtitle'] = res_subtitle_list
	return main_dict

def outputJSON(obj):
	"""Default JSON serializer"""
	if isinstance(obj, datetime):
		if obj.utcoffset() is not None:
			obj = obj - obj.utcoffset()

		return obj.strftime('%Y-%m-%d %H:%M')
	return str(obj)

if __name__ == "__main__":
	
	main_dict = {}
	year = 2018
	company_list = [('Reliance', 'RI'), ('Infosys', 'IT'), ('State Bank of India', 'SBI'), ('ICICI Bank', 'ICI02'),
					('Bharti Airtel', 'BTV'), ('Tata Motors', 'TEL'), ('ITC', 'ITC'), ('Maruti Suzuki', 'MU01'),
					('ONGC', 'ONG'), ('Hindustan Unilever', 'HL'), ('TCS', 'TCS'), ('Larsen & Toubro', 'LT'),
					('Sun Pharmaceutical Industries', 'SPI'), ('Dr Reddy', 'DRL')]
	comp_code = {
					'Reliance': 'reliance',
					'Infosys': 'infosys',
					'State Bank of India': 'sbi',
					'ICICI Bank': 'icici_bank',
					'Bharti Airtel': 'airtel',
					'Tata Motors': 'tata_motors',
					'ITC': 'itc',
					'Maruti Suzuki': 'maruti',
					'ONGC': 'ongc',
					'Hindustan Unilever': 'hul',
					'TCS': 'tcs',
					'Larsen & Toubro': 'larsen',
					'Sun Pharmaceutical Industries': 'sun_pharma',
					'Dr Reddy': 'Dr_Reddy'
				}
	for company, company_code in company_list:
		print(company)
		main_dict[company] = {}
		main_dict = moneycontrol(year, main_dict, company, company_code)
		# main_dict = IIFL(year, main_dict, company, comp_code[company]) # takes much more time to run
		main_dict = businesstoday(year, main_dict, company, comp_code[company])
	
	with open('news.json', 'w') as fp:
		json.dump(main_dict, fp, default=outputJSON)