# fcc/routes.py

from flask import Blueprint, render_template

from fcc.models import db, Organization, Check


bp = Blueprint('routes', __name__)


@bp.route('/')
def home():
    orgs = list( db.session.execute( 
        db.select(Organization).order_by(Organization.slug)
    ).scalars() )

    cards = {}
    for org in orgs:
        result = db.session.execute( 
            db.select(Check)
                .filter_by(organization_id=org.id)
                .order_by(Check.stmt_date_iso.desc(), Check.id)
                .limit(3)
        ).scalars()
        cards[org.slug] = list(result)

    return render_template('page/home.html', orgs=orgs, cards=cards)


@bp.route('/about')
def about():
    return render_template('page/about.html')