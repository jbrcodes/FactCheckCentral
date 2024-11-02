# /fcc/blues/scraper/VerificatScraper.py

from datetime import datetime
import re

from fcc.blues.scraper.BaseScraper import BaseScraper


# I have to convert Verificat's "unconventional" months in Catalan from the index page
# because some detail pages don't contain the date!!!

VERIFICAT_MONTHS = {
    'gen.': 'jan',
    'febr.': 'feb',
    'març': 'mar',
    'abr.': 'apr',
    'maig': 'may',
    'juny': 'jun',
    'jul.': 'jul',
    'ag.': 'aug',
    'set.': 'sep',
    'oct.': 'oct',
    'nov.': 'nov',
    'des.': 'dec'
}


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

            # date
            cat_date_str = post.query_selector('span.ultp-block-date').text_content().strip()
            item['stmt_date_iso'] = self._to_iso_date_str(cat_date_str)

            # summary (from detail page)
            item['misc'] = ''
            
            all_items.append(item)

        return all_items


    def _scrape_detail_page(self):
        detail = {}

        # There isn't always a summary/subtitle
        subt = self.page.query_selector('main .post_subtitle')
        if subt:
            detail['misc'] = subt.query_selector('p').text_content().strip()
        else:
            detail['misc'] = ''
        # detail['misc'] = self.page.query_selector('main .post_subtitle p').text_content().strip()
        
        return detail


    def _to_iso_date_str(self, cat_date_str):
        """ index page does not use 'official' Catalan abbreviated months """

        m = re.match(r'(\S+) (\d\d?), (\d{4})', cat_date_str)
        date1 = f'{VERIFICAT_MONTHS[m.group(1)]} {m.group(2)}, {m.group(3)}'
        iso_datetime = datetime.strptime(date1, '%b %d, %Y').isoformat()
        iso_date = re.sub(r'T.*', '', iso_datetime)

        return iso_date