from ..items.ValueItem import ValueItem

class ValueDataParser:    
    @staticmethod
    def extract_item(x, response):
        item = ValueItem()
        
        link = response.url
        if link is not None:
            item['link'] = link
            
        rank = x.xpath(".//*[contains(., 'World Rank')]/following-sibling::div/text()").extract_first()
        if ValueDataParser.not_empty(rank):
            rank = rank.replace(",", "")
            item['rank'] = rank
        else:
            item['rank'] = "Not found"
            
        name = x.xpath(".//a[contains(@href, '/company/')]/text()").extract()
        if ValueDataParser.not_empty(name):
            item['name'] = name[0]
        else:
            item['name'] = "Not found"
            
        ceo = x.xpath(".//div/a[contains(@href, '/business-leader/')]/text()").extract()
        if ValueDataParser.not_empty(ceo):
            item['ceo'] = ceo[0]
        else:
            item['ceo'] = "Not found"
            
        founded = x.xpath(".//*[contains(., 'Founded')]/following-sibling::div/text()").extract()
        if ValueDataParser.not_empty(founded):
            item['founded'] = founded[0]
        else:
            item['founded'] = "Not found"
            
        revenue = x.xpath(".//div[contains(., 'Annual Revenue')]/following-sibling::div/text()").extract()
        if ValueDataParser.not_empty(revenue):
            item['revenue'] = revenue[0]
        else:
            item['revenue'] = "Not found"    
            
        country = x.xpath(".//div/a[contains(@href, '/headquarters/')]/text()").extract()
        if ValueDataParser.not_empty(country):
            item['country'] = country[0]
        else:
            item['country'] = "Not found"
            
        industry = x.xpath(".//div/a[contains(@href, '/world-top-companies/')]/text()").extract()
        if ValueDataParser.not_empty(industry):
            item['industry'] = industry
        else:
            item['industry'] = "Not found"
            
        return item
    
    @staticmethod
    def not_empty(data):
        if not data or len(data) < 1 or data == [] or data == "-":
            return False
        return True