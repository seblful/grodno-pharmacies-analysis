# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AptekaItem(scrapy.Item):
    name_of_pharmacy = scrapy.Field()
    location_of_pharmacy = scrapy.Field()
    number_of_pharmacy = scrapy.Field()
    
    name_of_medicine = scrapy.Field()
    active_ingredient_or_type = scrapy.Field()
    dosage_form = scrapy.Field()
    prescribed = scrapy.Field()
    name_of_manufacturer = scrapy.Field()
    country_of_manufaturer = scrapy.Field()
    price_of_medicine = scrapy.Field()
    
    page = scrapy.Field()
