import scrapy
from scrapy.selector import Selector
from time import sleep


class IndeedJobSpider(scrapy.Spider):
    # identidade
    name = 'indeed_job_spider'
    id_counter = 0
    # Request

    def start_requests(self):
        # não esqueça de setar ROBOTSTXT_OBEY = False dentro do arquivo settings.py
        urls = ['https://br.indeed.com/jobs?q=python']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Response
    def parse(self, response):
        for job in response.xpath('//div[@class="job_seen_beacon"]'):
            yield {
                'job_id': self.id_counter,
                'role_name': job.xpath('.//span[contains(@id, "jobTitle")]/text()').get(),
                'company_name': job.xpath('.//span[@data-testid="company-name"]/text()').get(),
                'location': job.xpath('.//div[@data-testid="text-location"]/text()').get(),
                'link': job.xpath('.//a[contains(@class, "JobTitle")]/@href').get()
            }
            self.id_counter += 1
        try:
            next_page_url = response.xpath(
                '//a[@data-testid="pagination-page-next"]/@href').get()
            if next_page_url:
                yield scrapy.Request(url=next_page_url, callback=self.parse)
            else:
                print('='*10)
                print('ERROR next_page_url:' + next_page_url)
                print('='*10)
        except Exception as exp:
            print(exp)
