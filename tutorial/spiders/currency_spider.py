import scrapy
from datetime import datetime
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

    
data = ''

class QuotesSpider(scrapy.Spider):
    name = "currency"

    def start_requests(self):
        url = 'https://www.forex.pk/open_market_rates.asp'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'currencyRateToday.txt'
        today = datetime.now()
        longAndWeirdPath = "//table/tr/td/table/tr[3]/td/div/div[2]/table/tr/td[2]/table[2]/tr[contains(., '%s')]/td[3]/text()"
        curr_dict = {'USD' : longAndWeirdPath % 'USD',
        'AED' : longAndWeirdPath % 'AED',
        'BHD' : longAndWeirdPath % 'BHD',
        'EUR' : longAndWeirdPath % 'EUR',
        'THB' : longAndWeirdPath % 'THB'}
        with open(filename, 'a') as f:
            f.write(f'''
{today}''')
            for i in curr_dict:
                result = response.xpath(curr_dict[i]).getall()
                f.write(f'''
    {i} to PKR is {result[0]}''')


@app.route('/', methods=['GET'])
def home():
    with open('../../currencyRateToday.txt', 'r') as f:
        data = f.read()
        return data

app.run()