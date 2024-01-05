# /fcc/blues/scraper/SurligneursScraper.py

from datetime import datetime
import re

from fcc.blues.scraper.BaseScraper import BaseScraper


class SurligneursScraper(BaseScraper):

    def _scrape_index_page(self):
        all_items = []

        grid_items = self.page.query_selector_all(f'#grid .grid-item')
        for grid_item in grid_items[:self.FC_SCRAPE_COUNT]:
            item = {}

            # statement
            item['stmt_text'] = grid_item.query_selector('button + p').text_content()
            item['stmt_url'] = grid_item.query_selector('a').get_attribute('href')
            item['stmt_date_iso'] = ''  # from detail page

            # summary
            item['misc'] = ''  # from detail page

            # rating
            item['rating'] = grid_item.query_selector('button').text_content()

            all_items.append(item)

        return all_items


    def _scrape_detail_page(self):
        detail = {}

        # date
        source = self.page.query_selector('h2 a').text_content().strip()
        date_str = re.search(r'((\d\d?) (\w+) (\d{4}))$', source).group(1)
        detail['stmt_date_iso'] = self._to_iso_date_str(date_str)

        # summary
        detail['misc'] = self.page.query_selector('.correction p').text_content().strip()
        
        return detail
    

    def _to_iso_date_str(self, date_str):
        iso_datetime = datetime.strptime(date_str, '%d %B %Y').isoformat()
        iso_date = re.sub(r'T.*', '', iso_datetime)

        return iso_date