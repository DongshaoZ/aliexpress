# -*- coding: utf-8 -*-
import scrapy
from aliexpress.items import AliexpressItem
from scrapy.exceptions import CloseSpider


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['aliexpress.com']
    start_urls = ['https://www.aliexpress.com/all-wholesale-products.html']

    scheme = 'https:'

    def parse(self, response):
        category_url_list = response.xpath('//ul[@class="sub-item-cont util-clearfix"]/li/a/@href').extract()
        if category_url_list is None:
            raise CloseSpider(reason='cancelled')

        for each in category_url_list:
            url = self.scheme + each
            yield scrapy.Request(url, callback=self.parse_product_list)

    def parse_product_list(self, response):
        if response.status != 200:
            raise CloseSpider(reason='cancelled')

        item = AliexpressItem()

        item['category'] = self.__get_category(response)
        item['sub_category'] = self.__get_sub_category(response)

        list_item = response.xpath('//ul[@class="util-clearfix son-list"]/li/div')
        for each in list_item:
            try:
                item['name'] = self.__get_name(each)
                item['url'] = self.__get_url(each)
                item['img'] = self.__get_img(each)
                item['price'] = self.__get_price(each)
                item['rate_percent'] = self.__get_rate_percent(each)
                item['rate_num'] = self.__get_rate_num(each)
                item['order_num'] = self.__get_order_num(each)
            except Exception as e:
                # todo log something
                continue

            yield item

        url = self.__get_page_next(response)
        if url is not None:
            yield scrapy.Request(url, self.parse_product_list)

    def __get_category(self, response):
        result = response.xpath('//div[@id="aliGlobalCrumb"]/h1/a/text()').extract_first()
        if result is None:
            raise AttributeError('category is None')
        return result

    def __get_sub_category(self, response):
        result = response.xpath('//div[@id="aliGlobalCrumb"]/h1/span[2]/text()').extract_first()
        if result is None:
            raise AttributeError('sub_category is None')
        return result

    def __get_name(self, response):
        current_node = response.xpath('./div[@class="info"]/h3/a')
        result = current_node.xpath('string(.)').extract_first()
        if result is None:
            raise AttributeError('name is None')
        return result

    def __get_url(self, response):
        result = response.xpath('./div[@class="info"]/h3/a/@href').extract_first()
        if result is None:
            raise AttributeError('url is None')
        else:
            return self.scheme + result

    def __get_img(self, response):
        current_node = response.xpath('./div[@class="img img-border"]/div/a/img')

        src_attr = current_node.xpath('./@src').extract_first()
        image_src_attr = current_node.xpath('./@image-src').extract_first()

        if src_attr is None and image_src_attr is None:
            raise AttributeError('img is None')

        result = src_attr if(src_attr is not None) else image_src_attr
        return self.scheme + result

    def __get_price(self, response):
        result = response.xpath('./div[@class="info"]/span/span[1]/text()').extract_first()
        if result is None:
            raise AttributeError('price is None')
        return result

    def __get_rate_percent(self, response):
        result = response.xpath('./div[@class="info"]//span[@class="rate-percent"]/@style').extract_first()
        if result is None:
            return 0
        else:
            return result

    def __get_rate_num(self, response):
        result = response.xpath('./div[@class="info"]/div[@class="rate-history"]/a/text()').extract_first()
        if result is None:
            return 0
        else:
            return result

    def __get_order_num(self, response):
        result = response.xpath('./div[@class="info"]/div[@class="rate-history"]//em/text()').extract_first()
        if result is None:
            return 0
        else:
            return result

    def __get_page_next(self, response):
        result = response.xpath('//a[@class="page-next ui-pagination-next"]/@href').extract_first()
        if result is not None:
            return self.scheme + result
        else:
            return None


