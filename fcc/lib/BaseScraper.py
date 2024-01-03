# /fcc/lib/BaseScraper.py

from datetime import date
import locale
import logging
import time

from playwright.sync_api import sync_playwright

from fcc.models import db, Check
from fcc.lib.FileCache import FileCache


class BaseScraper:
    
    FC_SCRAPE_COUNT = 6


    def __init__(self): 
        self.playwright = None
        self.browser = None
        self.page = None
        self.org = None
        self.useCache = True


    def init(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        # ua = 'Playwr1ght 1.40: FactCheckCentral (demo) | fcc.jbrcodes.com | rudolf@jbrcodes.com'
        # self.browser = self.browser.new_context(user_agent=ua)
        self.page = self.browser.new_page()
    

    def close(self):
        self.browser.close()
        self.playwright.stop()


    def scrape(self, org):
        self.org = org
        index_items = self._scrape_page('index', org.scrape_url)
        logging.info('%d items scraped', len(index_items))
        new_items = self._filter_new_items(index_items)
        tweaked_items = self._pre_save_items(new_items)
        self._save_items(tweaked_items)
        logging.info('%d new items saved', len(new_items))


    def _scrape_page(self, type, url):
        obj = None
        if self.useCache:
            obj = FileCache.get(url)
        if obj is None:
            if type == 'detail':
                time.sleep(2)  # let's pause...
            self.page.goto(url)
            self._wait_for_page_load(type)
            if type == 'index':
                obj = self._scrape_index_page()
            else:
                obj = self._scrape_detail_page()
            if self.useCache:
                FileCache.put(url, obj)

        return obj
        

    def _wait_for_page_load(self, type):
        pass


    def _scrape_detail_page(self):
        '''Return a 'detail' dict with result from scraping detail page'''

        return None
    

    def _filter_new_items(self, all_items):
        new_items = []

        for item in all_items:
            stmt = (
                db.select(Check)
                    .where(Check.organization_id == self.org.id)
                    .where(Check.stmt_text == item['stmt_text'])
            )
            if db.session.execute(stmt).first() is None:
                new_items.append(item)

        return new_items
    

    def _pre_save_items(self, items):
        '''Return 'items' with whatever modifications are desired before saving'''
        save_locale_time = locale.getlocale(locale.LC_TIME)
        locale.setlocale(locale.LC_TIME, self.org.locale)

        tweaked_items = []
        for item in items:
            item1 = dict(item)

            # Integrate stuff from detail page if applicable
            detail = self._scrape_page('detail', item1['stmt_url'])
            if detail is not None:
                item1 = item1 | detail

            # Tweak any other stuff
            item1 = self._pre_save_item(item1)
            # Save date in locale's format
            item1['stmt_date_locale'] = date.fromisoformat(item1['stmt_date_iso']).strftime('%d %b %Y')

            logging.info(f"new: {item1['stmt_date_iso']} {item1['stmt_text'][:40]}")
            
            tweaked_items.append(item1)

        locale.setlocale(locale.LC_TIME, save_locale_time)

        return tweaked_items
    

    def _pre_save_item(self, item):
        return item
    

    def _save_items(self, new_items):
        if len(new_items) == 0:
            return
        
        new_checks = [Check(**item) for item in new_items]
        self.org.checks.extend(new_checks)
        db.session.commit()
