# /fcc/blues/scraper/DPAScraper.py

from datetime import datetime
import re

from fcc.blues.scraper.BaseScraper import BaseScraper


class DPAScraper(BaseScraper):

    def _scrape_index_page(self):
        all_items = []

        # Get 3 "teaser" items
        teasers = self.page.query_selector_all(f'.columns .column')
        for teaser in teasers:
            item = {}

            # date
            datetime = teaser.query_selector('time').text_content().strip()
            item['stmt_date_iso'] = self._to_iso_date_str(datetime)

            # statement
            a = teaser.query_selector('h3 a')
            item['stmt_text'] = a.text_content().strip()
            item['stmt_url'] = self.org.scrape_url + a.get_attribute('href')[2:]

            # summary
            # (Unfortunately it unnecessarily gets scraped again in _scrape_detail_page())
            item['misc'] = teaser.query_selector('.image-box + p').text_content().strip()
            
            all_items.append(item)

        # Now get just a few more from list of (over 2K!) remaining items
        articles = self.page.query_selector_all(f'.article-list tr:nth-child(-n + 10)')
        for art in articles:
            item = {}

            # date
            datetime = art.query_selector('time').text_content().strip()
            item['stmt_date_iso'] = self._to_iso_date_str(datetime)

            # statement
            a = art.query_selector('a')
            item['stmt_text'] = a.text_content().strip()
            item['stmt_url'] = self.org.site_url + a.get_attribute('href')

            # summary
            item['misc'] = ''  # get from detail page

            all_items.append(item)

        return all_items


    def _scrape_detail_page(self):
        # Get the summary from the detail page if we didn't get it from a teaser
        # (Note: This gets the detail page even if we got the summary from the teaser)
        tease = self.page.query_selector('article .teaser')
        detail = { 'misc': tease.text_content().strip() }
        
        return detail
    

    def _to_iso_date_str(self, datetime_str):
        iso_datetime = datetime.strptime(datetime_str[:10], '%d.%m.%Y').isoformat()
        iso_date = re.sub(r'T.*', '', iso_datetime)

        return iso_date