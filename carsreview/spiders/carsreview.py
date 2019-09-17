# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 07:49:16 2019

@author: Sam
"""

from scrapy import Spider
from carsreview.items import CarsreviewItem
from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np


class Carsreview(Spider):
    name = 'carsreview'
    url = 'https://www.cars.com/research/'
    response = get(url)
    page_html = BeautifulSoup(response.text,'html.parser')
    page_title = page_html.find('title').text
    
    try:
        main_left = page_html.find('script', attrs = {'id':'REDUX_STATE'})
    except:
        None    
        
    data=re.split('{|}',main_left.get_text())
    data=[i for i in data if re.search(r'makeId', i)]
    data=[','.join(i.split(':')) for i in data]   
    cars=pd.DataFrame()
    cars['id']=[i.split(',')[1] for i in data]
    cars['model']=[i.split(',')[3].split('"')[1] for i in data]
    cars['model_pass']=[i.split(',')[5].split('-')[1].split('"')[0] if len(i.split(','))>=7 else '' for i in data]
    cars['brand']=[i.split(',')[5].split('-')[0].split('"')[1] for i in data]
    cars['makeId']=[i.split(',')[7] if len(i.split(','))>=7 else '' for i in data]
    cars['years']=[i[i.find('years')+8:-1].split(',') for i in data]

    cars=cars[cars['model']!='0']

    cars_review =  pd.DataFrame({'id':np.repeat(cars['id'], cars['years'].str.len()),
                        'model':np.repeat(cars['model'], cars['years'].str.len()),
                        'model_pass':np.repeat(cars['model_pass'], cars['years'].str.len()),
                        'brand':np.repeat(cars['brand'], cars['years'].str.len()),
                        'makeId	':np.repeat(cars['makeId'], cars['years'].str.len()),
                        'years': np.concatenate(cars['years'])})
    cars_review.drop_duplicates(inplace=True)
    cars_review.to_csv('data/cars_list_by_year.csv')    
    urllst = []
    for brand in cars['brand']:
        car_brand=cars[cars['brand']==brand]
        for model in car_brand['model_pass']:
            car_model=car_brand[car_brand['model_pass']==model]
            for yearlst in car_model['years']:
                for year in yearlst:
                    for i in range(1,4):
                        urllst.append('https://www.cars.com/research/{}-{}-{}/consumer-reviews/?pg={}&nr=250'.format(brand, model, year, i))
                
                
                
                    
    start_urls =list(set(urllst))
    print('Number of pages: {}'.format(len(urllst)))

    
    def parse(self, response):
        reviews = response.xpath('//article') #tag for the user reviews

        ymm = response.xpath('//h2[@class="cui-heading-3"]/text()').extract_first().split()
        modelYear, make = ymm[:2]
        model = ' '.join(ymm[2:])

        for review in reviews:

            rating = review.xpath('./cars-star-rating/@rating').extract_first()
            url = review.xpath('./p[@class="cui-heading-6"]/a/@href').extract_first()
            title = review.xpath('./p[@class="cui-heading-6"]/a/text()').extract_first()
            reviewerInfo = review.xpath('./p[@class="review-card-review-by"]/text()').extract_first().split("\n")[1:4] #contains username, location and time
            reviewBody = review.xpath('./p[@class="review-card-text"]/text()').extract_first() #remove .replace when using SQL
            comfort = review.xpath('./div/div[1]/cars-star-rating/@rating').extract_first()
            performance = review.xpath('./div/div[2]/cars-star-rating/@rating').extract_first()
            exteriorStyling = review.xpath('./div/div[3]/cars-star-rating/@rating').extract_first()
            interior = review.xpath('./div/div[4]/cars-star-rating/@rating').extract_first()
            value = review.xpath('./div/div[5]/cars-star-rating/@rating').extract_first()
            reliability = review.xpath('./div/div[6]/cars-star-rating/@rating').extract_first()
            extras = review.xpath('./p[@class="review-card-extra"]')
            new = '' #should these 3 be set to None?
            use = ''
            recommend = ''
            for extra in extras:
                if extra.xpath('./text()').extract_first().find('Purchased') != -1:
                    new = extra.xpath('./b/text()').extract_first()
                    continue
                if extra.xpath('./text()').extract_first().find('Uses') != -1:
                    use = extra.xpath('./b/text()').extract_first()
                    continue
                if extra.xpath('./text()').extract_first().find('recommend') != -1:
                    recommend = extra.xpath('./b/text()').extract_first()
            helpful = review.xpath('./p[@class="review-card-feedback"]/b[1]/text()').extract_first()
            if not helpful:
                helpful = ''
            outOf = review.xpath('./p[@class="review-card-feedback"]/b[2]/text()').extract_first()
            if not outOf:
                outOf = ''
            
            item = CarsreviewItem()
            item['make'] = make  #add these later after correct way to loop through urls is
            item['model'] = model
            item['modelYear'] = modelYear
            item['rating'] = rating
            item['url'] = url
            item['title'] = title
            item['author'] = reviewerInfo[0].lstrip()[3:]
            item['location'] = reviewerInfo[1].lstrip()[5:].rstrip()
            item['date'] = reviewerInfo[2].lstrip()[3:]
            item['reviewBody'] = reviewBody
            item['comfort'] = comfort
            item['exteriorStyling'] = exteriorStyling
            item['value'] = value
            item['performance'] = performance
            item['interior'] = interior
            item['reliability'] = reliability
            item['new'] = new
            item['use'] = use
            item['recommend'] = recommend
            item['helpful'] = helpful
            item['outOf'] = outOf
            yield item
