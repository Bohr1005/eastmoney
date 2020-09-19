import scrapy
import pandas as pd
from eastmoney.items import EastmoneyItem
import urllib

df = pd.read_csv("~/eastmoney/codes.csv",index_col=0,encoding='gbk')
df.index = [index[3:] for index in df.index]
stocks_type = df['type'] == '股票型'
stockindex_type = df['type'] == '股票指数'
selected = df[stockindex_type | stocks_type].index


class FundInfoSpider(scrapy.Spider):
    name = 'fund_info'
    allowed_domains = ['fund.eastmoney.com']
    start_urls = [f'http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={code}&topline=10&year=2020&month=6&rt=0.4880541927789981' for code in selected]

    def parse(self, response):
        url_params = urllib.parse.parse_qs(response.url)
        fund_code = url_params['code'][0]
        date = url_params['year'][0] + url_params['month'][0]
        fund_name = response.selector.xpath('/html/body/div[1]/div/h4/label[1]/a/text()').get()
        table = response.selector.xpath('/html/body/div[1]/div/table/tbody/tr')
        for item in table:
            name_info = item.xpath('td/a/text()')
            code = name_info[0].get()
            name = name_info[1].get()
            weight_info = item.xpath('td/text()')
            weight = weight_info[1].get()
            share_num = weight_info[2].get()
            market_value = weight_info[3].get()

            fund_holding = EastmoneyItem()
            fund_holding['fund_code'] = fund_code
            fund_holding['fund_name'] = fund_name
            fund_holding['date'] = date
            fund_holding['code'] = code
            fund_holding['name'] = name
            fund_holding['weight'] = weight
            fund_holding['share_num'] = share_num
            fund_holding['market_value'] = market_value

            yield fund_holding

