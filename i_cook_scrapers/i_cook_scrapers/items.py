# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Ingredient(scrapy.Item):
    amount = scrapy.Field()
    name = scrapy.Field()
    notes = scrapy.Field()

class Recipe(scrapy.Item):
    title = scrapy.Field()
    img = scrapy.Field()
    link = scrapy.Field()
    summary = scrapy.Field()
    times = scrapy.Field()
    ingredients = scrapy.Field()
