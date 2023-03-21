from ..items.ForbesItem import ForbesItem

class ForbesDataParser:    
    @staticmethod
    def extract_item(x, response):
        item = ForbesItem()
        
        link = response.url
        if link is not None:
            link = link.replace('/?list=global2000', '')
            item['link'] = link
            
        name = x.xpath('.//div[@class="listuser-header__name"]/text()').extract_first()
        if ForbesDataParser.not_empty(name):
            item['name'] = name
            
        industry = x.xpath('.//span[contains(.,"Industry")]/following-sibling::*/span/text()').extract_first(),
        if ForbesDataParser.not_empty(industry[0]):
            item['industry'] = industry[0]
        else:
            item['industry'] = "Not found"
            
        founded = x.xpath('.//span[contains(.,"Founded")]/following-sibling::*/span/text()').extract_first(),
        if ForbesDataParser.not_empty(founded[0]):
            item['founded'] = founded[0]
        else:
            item['founded'] = "Not found"
            
        country = x.xpath('.//span[contains(.,"Country")]/following-sibling::*/span/text()').extract_first(),
        if ForbesDataParser.not_empty(country[0]):
            item['country'] = country[0]
        else:
            item['country'] = "Not found"
            
        ceo = x.xpath('.//span[contains(.,"Chief Executive Officer") or contains(.,"CEO") or'+ 
                      'contains(.,"Chairman")]/following-sibling::*/span/text()').extract_first(),
        if ForbesDataParser.not_empty(ceo[0]):
            item['ceo'] = ceo[0]
        else:
            item['ceo'] = "Not found"
            
        employees = x.xpath('.//span[contains(.,"Employees")]/following-sibling::*/span/text()').extract_first(),
        if ForbesDataParser.not_empty(employees[0]):
            item['employees'] = employees[0]
        else:
            item['employees'] = "Not found"
            
        revenue = x.xpath('.//div[contains(.,"Revenue")]/following-sibling::div/text()').extract_first(),
        if ForbesDataParser.not_empty(revenue[0]):
            item['revenue'] = revenue[0]
        else:
            item['revenue'] = "Not found"
                    
        return item
    
    @staticmethod
    def not_empty(data):
        if not data or len(data) < 1 or data == []:
            return False
        return True