# /fcc/seed.py

from fcc.models import db, Organization

all_orgs_data = [
    {
        'name': 'PolitiFact',
        'country': 'USA',
        'locale': 'en_US',
        'slug': 'politifact',
        'class_name': 'PolitiFact',
        'site_url': 'https://www.politifact.com',
        'scrape_url': 'https://www.politifact.com/factchecks/'
    },{
        'name': 'Newtral',
        'country': 'Spain',
        'locale': 'es_ES',
        'slug': 'newtral',
        'class_name': 'Newtral',
        'site_url': 'https://www.newtral.es',
        'scrape_url': 'https://www.newtral.es/zona-verificacion/fact-check/'
    },{
        'name': 'Deutsche Presse-Agentur',
        'country': 'Germany',
        'locale': 'de_DE',
        'slug': 'dpa',
        'class_name': 'DPA',
        'site_url': 'https://dpa-factchecking.com',
        'scrape_url': 'https://dpa-factchecking.com/germany/'
    },{
        'name': 'Les Surligneurs',
        'country': 'France',
        'locale': 'fr_FR',
        'slug': 'surligneurs',
        'class_name': 'Surligneurs',
        'site_url': 'https://www.lessurligneurs.eu',
        'scrape_url': 'https://lessurligneurs.eu/fact-checking/'
    },{
        'name': 'Snopes',
        'country': 'USA',
        'locale': 'en_US',
        'slug': 'snopes',
        'class_name': 'Snopes',
        'site_url': 'https://www.snopes.com',
        'scrape_url': 'https://www.snopes.com/fact-check/'
    },{
        'name': 'Verificat',
        'country': 'Spain',
        'locale': 'ca_ES',
        'slug': 'verificat',
        'class_name': 'Verificat',
        'site_url': 'https://www.verificat.cat',
        'scrape_url': 'https://www.verificat.cat/fact-checking/'
    }
]


def seed_db():
    for data in all_orgs_data:
        org = Organization(**data)
        db.session.add(org)

    db.session.commit()