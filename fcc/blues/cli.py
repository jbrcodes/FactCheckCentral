from datetime import date
import importlib
import logging
import traceback

import click
from flask import Blueprint, current_app

from fcc.models import db, Organization


bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.command('create')
def create():
    db.drop_all()
    db.create_all()


@bp.cli.command('seed')
def seed():
    from fcc.seed import seed_db
    seed_db()


@bp.cli.command('scrape')
@click.argument('args', nargs=-1)
def scrape(args):
    logging.info('Scrape: begin')
    logging.info(f'command: flask scrape {" ".join(args)}')

    orgs = _get_orgs_to_scrape(args)

    # Scrape the "chosen ones" (or all)
    for org in orgs:
        logging.info('%s: %s', org.name, org.scrape_url)

        # Dynamically load corresponding Scraper class
        # https://stackoverflow.com/a/4821120
        module_name = f'fcc.blues.scraper.{org.class_name}Scraper'
        module = importlib.import_module(module_name)
        class_ = getattr(module, f'{org.class_name}Scraper')
        
        # Let's go scraping!
        try:
            scraper = class_()
            scraper.init()
            scraper.scrape(org)
            scraper.close()
        except Exception as err:
            logging.error('Exception: %s', err)
            logging.error('Traceback: %s', traceback.format_exc())
    
    logging.info('Scrape: end')


def _get_orgs_to_scrape(args):
    all_orgs_list = list( db.session.execute( 
        db.select(Organization).order_by(Organization.id) 
    ).scalars() )

    all_orgs_dict = { o.slug: o for o in all_orgs_list }
    all_slugs_list = list( all_orgs_dict.keys() )

    if len(args) == 0:
        orgs_to_scrape = all_orgs_list
    else:
        orgs_to_scrape = []
        for arg in args:
            slug = arg.lower()
            if slug in all_slugs_list:
                orgs_to_scrape.append( all_orgs_dict[slug] )
            else:
                click.echo(f"warning: '{slug}' does not exist; skipping")

    return orgs_to_scrape


@bp.cli.command('mom')
def mom():
    print('Hi Mom!')