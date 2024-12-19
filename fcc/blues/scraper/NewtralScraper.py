# /fcc/blues/scraper/NewtralScraper.py

from datetime import datetime
import re

from fcc.blues.scraper.BaseScraper import BaseScraper


class NewtralScraper(BaseScraper):

    def _scrape_index_page(self):
        all_items = []
        cards = self.page.query_selector_all('#vog-verificaton-list .card-featured-archive')
        for card in cards:
            item = {}

            date_str = card.query_selector('.card-meta-date').text_content().strip()
            item['stmt_date_iso'] = self._to_iso_date_str(date_str)

            item['stmt_url'] = card.query_selector('.card-body a').get_attribute('href')
            
            all_items.append(item)

        return all_items


    def _scrape_detail_page(self):
        detail = {}
        card = self.page.query_selector('.section-post-single-card .card-body')

        detail['stmt_text'] = card.query_selector('mark').text_content().strip()

        author = card.query_selector('.card-author-text')
        detail['author_name'] = author.query_selector('span').text_content().strip()
        detail['author_title'] = author.inner_html().split('<br>')[1].strip()

        detail['rating'] = card.query_selector('.card-factcheck-result-text').text_content().strip()
        
        return detail


    def _to_iso_date_str(self, date_str):
        iso_datetime = datetime.strptime(date_str, '%d/%m/%Y').isoformat()
        iso_date = re.sub(r'T.*', '', iso_datetime)

        return iso_date