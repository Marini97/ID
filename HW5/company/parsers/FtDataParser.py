from ..items.FtItem import FtItem

class FtDataParser:    
    @staticmethod
    def extract_item(x, response, i):
        item = FtItem()
        
        link = x.xpath("(//*/tr)["+ str(i) +"]/td[2]/a/@href").extract_first()
        if FtDataParser.not_empty(link):
            item['link'] = link
        else:
            item['link'] = 'Not found'
            
        name = x.xpath("(//*/tr)["+ str(i) +"]/td[2]/a/text() | (//*/tr)["+ str(i) +"]/td[2]/text()").extract_first()
        if FtDataParser.not_empty(name):
            item['name'] = name
        else:
            item['name'] = "Not found"
        
        country = x.xpath("(//*/tr)["+ str(i) +"]/td[5]/text()").extract_first()
        if FtDataParser.not_empty(country):
            item['country'] = country
        else:
            item['country'] = "Not found"
            
        industry = x.xpath("(//*/tr)["+ str(i) +"]/td[6]/text()").extract_first()
        if FtDataParser.not_empty(industry):
            item['industry'] = industry
        else:
            item['industry'] = "Not found"
    
        revenue = x.xpath("(//*/tr)["+ str(i) +"]/td[9]/text()").extract_first()
        if FtDataParser.not_empty(revenue):
            item['revenue'] = revenue
        else:
            item['revenue'] = "Not found"
            
        employees = x.xpath("(//*/tr)["+ str(i) +"]/td[11]/text()").extract_first()
        if FtDataParser.not_empty(employees):
            item['employees'] = employees
        else:
            item['employees'] = "Not found"
            
        founded = x.xpath("(//*/tr)["+ str(i) +"]/td[13]/text()").extract_first()
        if FtDataParser.not_empty(founded):
            item['founded'] = founded
        else:
            item['founded'] = "Not found"
            
        return item
    
    @staticmethod
    def not_empty(data):
        if not data or len(data) < 1 or data == [] or data == "-":
            return False
        return True