from scrapy import Spider, Request

class PyconSpider(Spider):
    name = "pycon"
    
    def __init__(self):
        self.url = 'http://pycon.pk'
    
    def start_requests(self):
        yield Request(url=self.url, callback=self.extract_speakerslink)

    def extract_speakerslink(self, response):
        speakers_link = response.css("li[id='speakers-2019'] a::attr(href)").extract_first()
        url = "{0}{1}".format(self.url, speakers_link)
        yield Request(url=url) #Bydefault callback is parse method
    
    def parse(self, response):
        speakers_info = response.css("div[class='member-desc']")
        from pandas import DataFrame
        l = [[info.css("h3::text").extract_first(),info.css("h5::text").extract_first(),info.css("h6::text").extract_first()] for info in speakers_info]
        df = DataFrame(l, columns=["Name", "Designation", "Company"])
        df.to_csv("Speakers(Pycon2019).csv", index=False, sep=",")