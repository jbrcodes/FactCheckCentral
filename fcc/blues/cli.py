from datetime import date
import importlib
import logging

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
    fn = 'scrape-' + date.today().strftime('%Y-%m') + '.log'
    logging.basicConfig(
        level=logging.DEBUG,
        filename=current_app.config['LOG_DIR'] + '/' + fn,
        format='%(asctime)s %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S'    
    )
    logging.info('')
    logging.info('Scrape: begin')
    logging.info(f'command: flask scrape {" ".join(args)}')

    orgs = _get_orgs_to_scrape(args)

    # Scrape the "chosen ones" (or all)
    for org in orgs:
        logging.info('%s: %s', org.name, org.scrape_url)
        click.echo(f'{org.name}...')

        # Dynamically load corresponding Scraper class
        # https://stackoverflow.com/a/4821120
        module_name = f'fcc.blues.scraper.{org.class_name}Scraper'
        module = importlib.import_module(module_name)
        class_ = getattr(module, f'{org.class_name}Scraper')
        
        # Let's go scraping!
        scraper = class_()
        scraper.init()
        scraper.scrape(org)
        scraper.close()
    
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
