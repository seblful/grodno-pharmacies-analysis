import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.shell import inspect_response
from ..items import AptekaItem
from urllib.request import Request
from urllib.parse import urljoin
from subprocess import call
from gc import callbacks

class AptSpider(scrapy.Spider):
    name = 'apt'
    allowed_domains = ['tabletka.by']
    #start_urls = ['https://tabletka.by/pharmacies?region=1006&page=1&sort=name&sorttype=asc']  # гродненская область
    start_urls = ['https://tabletka.by/pharmacies?region=38&page=1&sort=name&sorttype=asc']  # гродно
    page_pharmacies = 1 # номер страницы с аптеками
    page_medicines = 1 # номер страницы с лекарствами
    
    def __init__(self, page_pharmacies=1, page_medicines=1, *args, **kwargs):
        super(AptSpider, self).__init__(*args, **kwargs)
        self.page_pharmacies = page_pharmacies
    
    def parse(self, response):
        
        for row in (response.css("tbody tr")):
            # перебор по аптекам (на странице 20 штук)
            items = AptekaItem()
            name_of_pharmacy = row.css(".pharm-name .text-wrap a::text").get()
            location_of_pharmacy = row.css(".tooltip-info-header .text-wrap span::text").get()
            number_of_pharmacy = row.css(".phone.tooltip-info .tooltip-info-header .text-wrap a::text").get()
            
            items['name_of_pharmacy'] = name_of_pharmacy
            items['location_of_pharmacy'] = location_of_pharmacy
            items['number_of_pharmacy'] = number_of_pharmacy
            
            for i in range(1, 240):
                inner_link = urljoin('https://tabletka.by/', (row.css(".pharm-name .text-wrap a::attr(href)").get() + '?page=' + str(i)))
                yield response.follow(inner_link, callback=self.parse_medicines, meta={'items' : items})

        # пагинация по аптекам
        if self.page_pharmacies < 10:  #and not response.css(".table-pagination.last-page")
            self.page_pharmacies += 1
            #yield response.follow('https://tabletka.by/pharmacies?region=1006&page=' + str(self.page_pharmacies) + '&sort=name&sorttype=asc', callback=self.parse)
            yield response.follow('https://tabletka.by/pharmacies?region=38&page=' + str(self.page_pharmacies) + '&sort=name&sorttype=asc', callback=self.parse)

            
    def parse_medicines(self, response):
        
        for low in response.css("tbody tr"):
            # перебор по названиям одной аптеки
            items = response.meta['items']
            name_of_medicine = low.css(".name.tooltip-info .tooltip-info-header a::text").get()
            
            # разделение на лекарства и остальное (разная структура так как у лекарств ссылка)
            a_or_t = low.css(".name.tooltip-info .capture::text").get().strip()
            if a_or_t:
                active_ingredient_or_type = a_or_t
            else:
                active_ingredient_or_type = low.css(".name.tooltip-info .capture a::text").get().strip()
            
            dosage_form = low.css(".form-title::text").get()
            prescribed = low.css(".form.tooltip-info .capture::text").get()
            name_of_manufacturer = low.css(".produce.tooltip-info .tooltip-info-header span a::text").get().strip()
            country_of_manufaturer = low.css(".produce.tooltip-info .capture::text").get().strip()
            price_of_medicine = low.css(".price-value::text").get().strip()
            
            items['name_of_medicine'] = name_of_medicine
            items['active_ingredient_or_type'] = active_ingredient_or_type
            items['dosage_form'] = dosage_form
            items['prescribed'] = prescribed
            items['name_of_manufacturer'] = name_of_manufacturer
            items['country_of_manufaturer'] = country_of_manufaturer
            items['price_of_medicine'] = price_of_medicine
            
            items['page'] = str(self.page_medicines)
            
            yield items