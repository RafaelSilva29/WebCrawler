# -*- coding: utf-8 -*-
import scrapy

from autoevolution_scraper.items import AutoevolutionScraperItem

class AutoevolutionSpider(scrapy.Spider):
    name = 'AutoEvolution'
    allowed_domains = ['autoevolution.com']
    start_urls = ['http://autoevolution.com/cars/']

    def parse(self, response):
        BRAND_LIST_SELECTOR = '.carman'
        for brand in response.css(BRAND_LIST_SELECTOR):
            NAME_SELECTOR = 'h5 a ::text'
            URL_BRAND_SELECTOR = 'h5 a ::attr(href)'
            IMAGE_SELECTOR = 'a img ::attr(src)'
            nameBrand = brand.css(NAME_SELECTOR).extract_first()
            urlBrand = brand.css(URL_BRAND_SELECTOR).extract_first()
            imageBrand = brand.css(IMAGE_SELECTOR).extract_first()
            brand = {
                'nameBrand': nameBrand.replace(' ', '_'),
                'urlBrand': urlBrand,
                'imageBrand': imageBrand,
            }
            if urlBrand:
                request = scrapy.Request(urlBrand, callback=self.parseBrand, meta={'brand': brand})
                yield request
    
    def parseBrand(self, response):
        brand = response.meta['brand']
        HISTORY_SELECTOR = '#newscol1 > .histbox > .prodhist::text'
        history = response.css(HISTORY_SELECTOR).extract()
        aux_history = ''
        for line in history:
            line = line.strip() 
            aux_history += line
        info_brand = list()
        INFO_BRAND_SELECTOR = '#newscol1 > .brandinfo > p'
        for info in response.css(INFO_BRAND_SELECTOR):
            AUX_SELECTOR = 'b ::text'
            aux_info = info.css(AUX_SELECTOR).extract_first()
            info_brand.append(aux_info)
        if len(info_brand) > 0:
            brand['infoBrand'] = {
                'history': aux_history,
                'productionModels': info_brand[0],
                'discontinuedModels': info_brand[1]
            }
        else:
            brand['infoBrand'] = {
                'history': aux_history, 
            }
        CAR_LIST_SELECTOR = '.carmod'
        for car in response.css(CAR_LIST_SELECTOR):
            NAME_CAR = '.fl > a h4::text'
            URL_CAR = '.fl > a::attr(href)'
            IMG_CAR = '.fl > a img::attr(src)'
            CLASS_CAR = '.fl > .body ::text'
            FUEL_CAR = '.fl > .eng > span'
            CAR_INFO_ONE = '.fl > p > b::text'
            CAR_INFO_TWO = '.fl > span::text'
            url_car = car.css(URL_CAR).extract_first()
            name_car = car.css(NAME_CAR).extract_first()
            img_car = car.css(IMG_CAR).extract_first()
            class_car = car.css(CLASS_CAR).extract_first()
            fuels = []
            for fuel in car.css(FUEL_CAR):
                FUEL_AUX = '::text'
                fuel_aux = fuel.css(FUEL_AUX).extract_first()
                fuels.append(fuel_aux)
            nrGenerations = car.css(CAR_INFO_ONE).extract_first()
            modelYears = car.css(CAR_INFO_TWO).extract_first()
            model = {
                'name': name_car.replace(' ', '_'),
                'url': url_car,
                'img': img_car,
                'class': class_car,
                'fuels': fuels,
                'nrGenerations': nrGenerations,
                'modelYears': modelYears
            }
            if url_car:
                request = scrapy.Request(url_car, callback=self.parseModelVersion, meta={'model': model, 'brand': brand})
                yield request
            
    def parseModelVersion(self, response):
        model = response.meta['model']
        brand = response.meta['brand']
        VERSION_SELECTOR = '.carmodel'
        for version in response.css(VERSION_SELECTOR):
            GALLERY_SELECTOR = '.col1width > a ::attr(href)'
            YEARS_SELECTOR = '.col2width > .years > a ::text'
            VERSION_SELECTOR_URL = '.col2width > .col12width > .col2width > .engitm > a ::attr(href)'
            VERSION_SELECTOR_NAME = '.col2width > .col12width > .col2width > .engitm > a ::attr(title)'
            gallery = version.css(GALLERY_SELECTOR).extract_first()
            years = version.css(YEARS_SELECTOR).extract_first()
            version_url = version.css(VERSION_SELECTOR_URL).extract_first()
            version_name = version.css(VERSION_SELECTOR_NAME).extract_first()
            version_name = version_name.replace('More info about ', '')
            version = {
                'gallery': gallery,
                'years': years,
                'version_url': version_url,
                'version_name': version_name.replace(' ', '_')
            }
            if version_url:
                request = scrapy.Request(version_url, callback=self.parseSpecsVersion, meta={'model': model, 'brand': brand, 'version': version})
                yield request

    def parseSpecsVersion(self, response):
        model = response.meta['model']
        brand = response.meta['brand']
        version = response.meta['version']
        SEGMENT_SELECTOR = '.col23width > .modelbox > p ::text'
        BODY_SELECTOR = '.col23width > .modelbox > p ::text'
        INTRO_SELECTOR = '.col23width > .newstext > .mgbot_20 > .intro ::text'
        DESCRIPTION_SELECTOR = '.col23width > .newstext > .mgbot_20 > p ::text'
        TECHDATA_SELECTOR = '.col23width > .padcol2 > .engine-block > .enginedata > .techdata'
        segment = response.css(SEGMENT_SELECTOR).extract()
        intro = response.css(INTRO_SELECTOR).extract_first()
        description = response.css(DESCRIPTION_SELECTOR).extract_first()
        if len(segment) <= 3:
            info = {
                'segment': segment[2].strip()
            }
        else:
            info = {
                'segment': segment[4].strip(),
                'bodyStyle': segment[2].strip()
            }
        if intro:
            info['intro'] = intro.strip()
        if description:
            info['description'] = description.strip()
        ID_SELECTOR = '.col23width > .padcol2 > .engine-block ::attr(id)'
        id_aux = response.css(ID_SELECTOR).extract_first()
        i = 1
        for techdata in response.css(TECHDATA_SELECTOR):
            TITLE_SELECTOR = '.title > div ::text'
            ENGINE_SELECTOR = '.title > div > span ::text'
            SPECS_SELECTOR = '.table1w > .techdata'
            title = techdata.css(TITLE_SELECTOR).extract_first()
            engine = techdata.css(ENGINE_SELECTOR).extract_first()
            title = title.replace(' ', '')
            title = title.replace('(', '')
            title = title.replace('–', '')
            title = title.strip()
            title = title.lower()
            specs = {}
            j = 1
            for spec_aux in techdata.css('.table1w > dt'):
                INFO_SELECTOR = 'em ::text'
                DESC_SELECTOR = '//*[@id="'+id_aux+'"]/div/div['+str(i)+']/dl/dd['+str(j)+']/text()'
                info_aux = spec_aux.css(INFO_SELECTOR).extract_first()
                info_desc = response.xpath(DESC_SELECTOR).extract()
                info_aux = info_aux.replace(' ', '-')
                info_aux = info_aux.lower()
                if info_desc == []:
                    break
                if len(info_desc) == 1:
                    info_desc_aux = info_desc[0].strip()
                else:
                    info_desc_aux = info_desc
                specs[info_aux] = info_desc_aux
                j += 1
            info[title] = specs
            i += 1
        version['info'] = info
        model['version'] = version
        auto_evolution_scraper_item = AutoevolutionScraperItem(
            brand=brand,
            model=model
        )
        yield auto_evolution_scraper_item
