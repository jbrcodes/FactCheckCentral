# /fcc/blues/scraper/PolitiFactScraper.py

from datetime import datetime
import re

from fcc.blues.scraper.BaseScraper import BaseScraper


Rating_Strings = {
    'barely-true': 'Barely true',
    'false': 'False',
    'half-true': 'Half true',
    'mostly-true': 'Mostly true',
    'pants-fire': 'Pants on fire!',
    'true': 'True',
}


class PolitiFactScraper(BaseScraper):

    def _scrape_index_page(self):
        all_items = []
        articles = self.page.query_selector_all(f'li.o-listicle__item:nth-child(-n + {self.FC_SCRAPE_COUNT})')
        for art in articles:
            item = {}

            # statement
            a = art.query_selector('.m-statement__quote a')
            item['stmt_text'] = a.text_content().strip()
            item['stmt_url'] = self.org.site_url + a.get_attribute('href')
            desc_text = art.query_selector('.m-statement__desc').text_content().strip()
            m = re.match(r'stated on (.*?) in (.*?):', desc_text)
            item['stmt_date_iso'] = self._to_iso_date_str( m.group(1) )

            # author
            item['author_name'] = art.query_selector('.m-statement__meta a').text_content().strip()

            # rating
            item['rating'] = art.query_selector('.m-statement__meter img.c-image__thumb').get_attribute('alt')
            
            all_items.append(item)

        return all_items
    

    def _pre_save_item(self, item):
        item1 = dict(item)

        # Modify a few things...
        item1['author_name'] = re.sub(r' posts$', '', item1['author_name'])
        item1['author_name'] = re.sub(r'^X$', 'X (Twitter)', item1['author_name'])
        item1['rating'] = Rating_Strings[ item1['rating'] ]

        return item1
    

    def _to_iso_date_str(self, date_str):
        '''Convert 'May 10, 2020' to ISO format'''
        iso_datetime = datetime.strptime(date_str, '%B %d, %Y').isoformat()
        iso_date = re.sub(r'T.*', '', iso_datetime)

        return iso_date
