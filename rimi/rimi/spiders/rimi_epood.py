import scrapy

from ..items import RimiItem


class RimiEpoodSpider(scrapy.Spider):
    name = "rimi_epood"
    page_number = 2
    start_urls = ["https://www.rimi.ee/epood/ee/otsing?page=1&pageSize=100&query="]

    def parse(self, response):
        items = RimiItem()

        XPATH_ALL_PRODUCTS = "//*[@class='product-grid__item']"
        XPATH_PRODUCT_NAME = ".//p[@class='card__name']/text()"
        XPATH_PRODUCT_PRICE = ".//*[@class='card__price']//text()"
        XPATH_PRODUCT_OLD_PRICE = ".//p[@class='card__old-price']"
        XPATH_BONUSCARD_PRICE = ".//*[@class='price-badge__price']//text()"
        XPATH_PRODUCT_URL = ".//*[@class='card__url js-gtm-eec-product-click']/@href"
        XPATH_THUMBNAIL_URL = ".//*[@class='card__image-wrapper']//img/@src"

        all_products = response.xpath(XPATH_ALL_PRODUCTS)

        for product in all_products:
            product_name = product.xpath(XPATH_PRODUCT_NAME).extract()
            # response.xpath("//*[@class='card__price']//text()").re(r'[\d.,]+').extract()
            product_price = product.xpath(XPATH_PRODUCT_PRICE).re(r"\d+")

            if len(product_price) > 0:
                product_price = float(".".join(product_price))

            product_old_price = product.xpath(XPATH_PRODUCT_OLD_PRICE).re(r"[\d,]+")
            if len(product_old_price) > 0:  # replace comma to point if old price exists
                product_old_price = float(product_old_price[0].replace(",", "."))

            product_bonuscard_price = product.xpath(XPATH_BONUSCARD_PRICE).re(r"\d+")
            if len(product_bonuscard_price) > 0:
                product_bonuscard_price = float(".".join(product_bonuscard_price))

            currency = "EUR"

            product_url = product.xpath(XPATH_PRODUCT_URL).extract()

            thumbnail_picture = product.xpath(XPATH_THUMBNAIL_URL).extract()

            items["name"] = product_name[0]
            items["price"] = product_price
            items["old_price"] = product_old_price
            items["currency"] = currency
            items["bonuscard_price"] = product_bonuscard_price
            items["url"] = f"https://www.rimi.ee{product_url[0]}"
            items["pic_url"] = thumbnail_picture[0]

            yield items

        next_page = f"https://www.rimi.ee/epood/ee/otsing?page={str(RimiEpoodSpider.page_number)}&pageSize=100&query="
        if RimiEpoodSpider.page_number < 20:
            RimiEpoodSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
