from scrapy.item import Item, Field

class BeastItem(Item):
    title = Field()
    link = Field()
    article = Field()
