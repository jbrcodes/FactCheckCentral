# /fcc/blues/scraper/NewtralScraper.py

from datetime import datetime
import re

from fcc.blues.scraper.BaseScraper import BaseScraper


class NewtralScraper(BaseScraper):

    def _scrape_index_page(self):
        all_items = []
        cards = self.page.query_selector_all('section.s-verification-cards div[id^="item"]')
        for card in cards:
            item = {}

            # statement
            a = card.query_selector('mark a')
            item['stmt_text'] = a.text_content().strip()
            item['stmt_url'] = a.get_attribute('href')
            item['stmt_date_iso'] = ''  # temporary; the date's on the detail page

            # author
            who = card.query_selector('.c-card__verification__who')
            item['author_name'] = who.query_selector('.c-card__verification__who__name').text_content().strip()
            item['author_title'] = who.query_selector('.c-card__verification__who__position').text_content().strip()

            # rating
            item['rating'] = card.query_selector('aside .c-card__verification__rating__text').text_content().strip()
            
            all_items.append(item)

        return all_items


    def _wait_for_page_load(self, type):
        if type == 'index':
            self.page.wait_for_function('() => document.getElementById("scroll-load-more").hidden === false')


    def _scrape_detail_page(self):
        # Get the date in format 'dd-mm-yy'
        when = self.page.query_selector('.c-card__verification__when').text_content().strip()
        detail = { 'stmt_date_iso': self._to_iso_date_str(when) }
        
        return detail


    def _to_iso_date_str(self, date_str):
        iso_datetime = datetime.strptime(date_str, '%d-%m-%y').isoformat()
        iso_date = re.sub(r'T.*', '', iso_datetime)

        return iso_date