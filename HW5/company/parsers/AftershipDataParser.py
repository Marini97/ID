from ..items.AftershipItem import AftershipItem

class AftershipDataParser:    
    @staticmethod
    def extract_item(x, response):
        item = AftershipItem()
        
        link = response.url
        if link is not None:
            item['link'] = link
            
        name = x.xpath(".//h1/text()").extract_first()
        if AftershipDataParser.not_empty(name):
            item['name'] = name
            
        founded = x.xpath(".//h4[contains(., 'Created')]/following-sibling::*/text()").extract_first()
        if AftershipDataParser.not_empty(founded):
            item['founded'] = founded
        else:
            item['founded'] = "Not found"
            
        employees = x.xpath(".//h4[contains(., 'Employees')]/following-sibling::*/text()").extract_first()
        if AftershipDataParser.not_empty(employees):
            item['employees'] = employees
        else:
            item['employees'] = "Not found"
            
        montly_sales = x.xpath(".//h4[contains(., 'Monthly Sales')]/following-sibling::*/text()").extract_first() 
        if AftershipDataParser.not_empty(montly_sales):
            item['monthly_sales'] = montly_sales
        else:
            item['monthly_sales'] = "Not found"
            
        headquarters = x.xpath(".//h4[contains(., 'Headquarters')]/following-sibling::*/text()").extract_first()
        if AftershipDataParser.not_empty(headquarters):
            item['headquarters'] = headquarters
        else:
            item['headquarters'] = "Not found"
            
        speed_score = x.xpath(".//h4[contains(., 'Desktop')]/following-sibling::*/text()").extract_first()
        if AftershipDataParser.not_empty(speed_score):
            item['speed_score'] = speed_score
        else:
            item['speed_score'] = "Not found"
        
        return item
    
    @staticmethod
    def not_empty(data):
        if not data or len(data) < 1 or data == [] or data == "-":
            return False
        return True