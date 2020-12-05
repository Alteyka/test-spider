import datetime
import scrapy
from scrapy_splash import SplashRequest


class WildberriesGoodsSpider(scrapy.Spider):
    name = 'wildberries_goods'
    allowed_domains = ['www.wildberries.ru']
    start_urls = ['https://www.wildberries.ru/catalog/obuv/zhenskaya/sabo-i-myuli/myuli/']
    result_list = []
    custom_settings = {'FEED_URI': "wildberries_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    # Активирует js скрипты, но так как я не обнаружил где там POST отправляется, закомментил

    # def start_requests(self):
    #     yield SplashRequest(
    #         url='https://www.wildberries.ru/catalog/obuv/zhenskaya/sabo-i-myuli/myuli/',
    #         callback=self.parse
    #     )

    # Насколько я понял, Выбор города осуществляется примерно так

    # chose_city_url = 'https://www.wildberries.ru/catalog/obuv/zhenskaya/sabo-i-myuli/myuli/'
    # def chose_city(self, response):
    #     city = response.css(".input-text.j-validate-id::attr(value)").extract_first()
    #     data = {'city_field': 'Москва'}
    #     yield scrapy.FormRequest(url=self.chose_city_url, formdata=data, callback=self.parse)

    def parse(self, response):
        cards = response.css(".dtList.i-dtList.j-card-item")
        section = response.css(".bread-crumbs span::text").getall()
        for card in cards:
            time = datetime.datetime.now()
            timestamp = datetime.datetime.timestamp(time)
            url = card.css("a::attr(href)").extract_first()
            rpc = card.css(".dtList.i-dtList.j-card-item div::attr(id)").extract_first()
            title = card.css("span .goods-name::text").extract_first()
            brand = card.css(".dtlist-inner-brand-name .brand-name::text").extract_first()
            price_dict = {
                'price_data': card.css(".lower-price::text").extract_first().strip(),
                'old_price': card.css(".price-old-block > ::text").extract_first(),
                'sale_tag': card.css(".price-sale.active::text").extract_first()
            }
            stock = True
            assets = card.css(".l_class img::attr(src)").extract_first()
            comments_count = card.css(".dtList-comments-count.c-text-sm::text").extract_first()
            scrapped_info = {
                'timestamp': timestamp,
                'url': url,
                'RPC': rpc,
                'title': title,
                'brand': brand,
                'section': section,
                'price_data': price_dict,
                'stock': stock,
                'assets': assets,
                'comments_count': comments_count,

            }
            yield scrapped_info
        next_page_url = response.css(".pageToInsert .pagination-next::attr(href)").extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)



