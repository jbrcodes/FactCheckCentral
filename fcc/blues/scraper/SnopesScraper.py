# /fcc/blues/scraper/SnopesScraper.py

from datetime import datetime
import re

from fcc.blues.scraper.BaseScraper import BaseScraper


class SnopesScraper(BaseScraper):

    def _scrape_index_page(self):
        all_items = []

        articles = self.page.query_selector_all('#list_template_wrapper .article_wrapper')
        for art in articles:
            item = {}

            # statement
            item['stmt_text'] = art.query_selector('h3.article_title').text_content().strip()
            item['stmt_url'] = art.query_selector('a.outer_article_link_wrapper').get_attribute('href')
            artdate = art.query_selector('span.article_date').text_content().strip()
            item['stmt_date_iso'] = self._to_iso_date_str(artdate)

            # summary
            item['misc'] = art.query_selector('span.article_byline').text_content().strip()

            # rating
            item['rating'] = ''  # get from detail page

            all_items.append(item)

        return all_items


    def _scrape_detail_page(self):
        detail = {}

        # rating
        elem = self.page.query_selector('div.rating_title_wrap')
        if elem:
            # (I wish I could grab the first text node in elem...)
            messy_rating = elem.text_content()
            detail['rating'] = re.search(r'\n\t+((\w| )+)\t+\n', messy_rating).group(1)
        else:
            # (I'm not sure this is even possible)
            detail['rating'] = '(none found)'
        
        return detail


    def _to_iso_date_str(self, date_str):
        # Get the original date in case there is original & updated date
        first_date_str = re.search(r'(\w{3} \d\d?, \d{4})', date_str).group(1)
        iso_datetime = datetime.strptime(first_date_str, '%b %d, %Y').isoformat()
        iso_date = re.sub(r'T.*', '', iso_datetime)

        return iso_date