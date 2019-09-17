# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy 


class CarsreviewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    make            = scrapy.Field()
    model           = scrapy.Field()
    modelYear       = scrapy.Field()
    rating          = scrapy.Field()
    url             = scrapy.Field()
    title           = scrapy.Field()
    author          = scrapy.Field()
    location        = scrapy.Field()
    date            = scrapy.Field()
    reviewBody      = scrapy.Field()
    comfort         = scrapy.Field()
    exteriorStyling = scrapy.Field()
    value           = scrapy.Field()
    performance     = scrapy.Field()
    interior        = scrapy.Field()
    reliability     = scrapy.Field()
    new             = scrapy.Field()
    use             = scrapy.Field()
    recommend       = scrapy.Field()
    helpful         = scrapy.Field()
    outOf           = scrapy.Field() 
