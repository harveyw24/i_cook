from bs4 import BeautifulSoup
import scrapy
from i_cook_scrapers.items import Recipe, Ingredient

class JustOneCookbookSpider(scrapy.Spider):
    name = 'just_one_cookbook'
    allowed_domains = ['justonecookbook.com']
    start_urls = [f'https://www.justonecookbook.com/recipes/page/{i}/' for i in range(1, 12)]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        recipes = soup.find_all('article', {'class': 'post-filter'})

        for recipe in recipes:
            title = recipe.find('h3').text.strip()
            img = recipe.find('img')['src']
            link = recipe.find('h3').find('a')['href']
            # Schedule a request to the recipe detail page
            yield response.follow(link, self.parse_recipe, meta={'title': title, 'img': img, 'link': link})

    def parse_recipe(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        summary = soup.find('div', {'class': 'wprm-recipe-summary'})
        summary = summary.text.strip() if summary else None

        def get_time(selector):
            container = soup.find('div', {'class': selector})
            if container:
                time_span = container.find('span', {'class': 'wprm-recipe-time'})
                return time_span.text.strip() if time_span else None
            return None

        times = {
            'prep_time': get_time('wprm-recipe-prep-time-container'),
            'cook_time': get_time('wprm-recipe-cook-time-container'),
            'total_time': get_time('wprm-recipe-total-time-container'),
        }
        if all(time is None for time in times.values()):
            self.logger.warning(f"No times found for recipe: {response.meta['title']}")
            return

        ingredients = []
        ingredients_ul = soup.find('ul', {'class': 'wprm-recipe-ingredients'})
        if ingredients_ul:
            for li in ingredients_ul.find_all('li'):
                amount = li.find(class_='wprm-recipe-ingredient-amount')
                name = li.find(class_='wprm-recipe-ingredient-name')
                notes = li.find(class_='wprm-recipe-ingredient-notes')
                ingredient = Ingredient(
                    amount = amount.text.strip() if amount else None,
                    name = name.text.strip() if name else None,
                    notes = notes.text.strip() if notes else None
                )
                ingredients.append(ingredient)
        
        if not ingredients:
            self.logger.warning(f"No ingredients found for recipe: {response.meta['title']}")
            return

        recipe_item = Recipe(
            title=response.meta['title'],
            img=response.meta['img'],
            link=response.meta['link'],
            summary=summary,
            times=times,
            ingredients=ingredients
        )
        yield recipe_item
