from ..items.DisfoldItem import DisfoldItem

class DisfoldDataParser:    
    @staticmethod
    def extract_item(x, response):
        item = DisfoldItem()
        
        link = response.url
        if link is not None:
            item['link'] = link
            
        name = x.xpath(".//h1/text()").extract_first()
        if DisfoldDataParser.not_empty(name):
            item['name'] = name
        else:
            item['name'] = "Not found"
            
        headquarters = x.xpath(".//p[contains(., 'Headquarters:')]/text()").extract_first()
        if DisfoldDataParser.not_empty(headquarters):
            headquarters = headquarters.replace("Headquarters: ", "")
            headquarters = headquarters.replace("  ", "")
            item['headquarters'] = headquarters.replace("\n", "")
        else:
            item['headquarters'] = "Not found"
            
        founded = x.xpath(".//p[contains(., 'Founded:')]/text()").extract_first()
        if DisfoldDataParser.not_empty(founded): 
            founded = founded.replace('\u00a0', " ")
            item['founded'] = founded.replace("Founded: ", "")
        else:
            item['founded'] = "Not found"
            
        employees = x.xpath(".//p[contains(., 'Employees:')]/text()").extract_first()
        if DisfoldDataParser.not_empty(employees):
            item['employees'] = employees.replace("Employees: ", "")
        else:
            item['employees'] = "Not found"
        
        ceo = x.xpath(".//p[contains(., 'CEO:')]/text()").extract_first()
        if DisfoldDataParser.not_empty(ceo):
            item['ceo'] = ceo.replace("CEO: ", "")
        else:
            item['ceo'] = "Not found"
            
        market_cap = x.xpath(".//p[contains(@class, 'mcap')]/text()").extract_first()
        if DisfoldDataParser.not_empty(market_cap):
            item['market_cap'] = market_cap
        else:
            item['market_cap'] = "Not found"
        
        return item
    
    @staticmethod
    def not_empty(data):
        if not data or len(data) < 1 or data == [] or data == "-":
            return False
        return True