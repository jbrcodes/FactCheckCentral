# /fcc/blues/scraper/VerificatScraper.py

from datetime import datetime
import re

from fcc.blues.scraper.BaseScraper import BaseScraper


class VerificatScraper(BaseScraper):

    def _scrape_index_page(self):
        all_items = []
        posts = self.page.query_selector_all('main .ultp-block-item')
        for post in posts:
            item = {}

            # statement
            a = post.query_selector('h5 a')
            item['stmt_text'] = a.text_content().strip()
            item['stmt_url'] = a.get_attribute('href')

            # summary (from detail page)
            item['misc'] = ''
            
            all_items.append(item)

        return all_items


    # def _wait_for_page_load(self, type):
    #     if type == 'index':
    #         self.page.wait_for_function('() => document.getElementById("scroll-load-more").hidden === false')


    def _scrape_detail_page(self):
        detail = {}

        iso_datetime = self.page.query_selector('main time').get_attribute('datetime')
        detail['stmt_date_iso'] = re.sub(r'T.*', '', iso_datetime)

        detail['misc'] = self.page.query_selector('main .post_subtitle p').text_content().strip()
        
        return detail


    # def _to_iso_date_str(self, date_str):
    #     """ Site doesn't use "official" month abbreviations? """
    #     # ensure month is only 3 letters
    #     m = re.match(r'(\S+) (\d\d?), (\d{4})', date_str)
    #     date1 = f'{MONTHS[m.group(1)]} {m.group(2)}, {m.group(3)}'
    #     iso_datetime = datetime.strptime(date1, '%b %d, %Y').isoformat()
    #     iso_date = re.sub(r'T.*', '', iso_datetime)

    #     return iso_date