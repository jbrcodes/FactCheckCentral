# /fcc/checks/routes.py

from flask import Blueprint, render_template
from fcc.models import db, Check, Organization


bp = Blueprint('checks', __name__, url_prefix='/checks')


@bp.route('/')
def index():
    org = db.get_or_404(Organization, 1)
    checks = db.session.execute( 
        db.select(Check).order_by(Check.stmt_date_iso.desc(), Check.id) 
    ).scalars()

    return render_template('check/index.html', organization=org, checks=checks)


@bp.route('/<org_slug>')
def index2(org_slug):
    org = db.one_or_404( db.select(Organization).filter_by(slug=org_slug) )
    checks = db.session.execute( 
        db.select(Check)
            .filter_by(organization_id=org.id)
            .order_by(Check.stmt_date_iso.desc(), Check.id)
            .limit(6)
    ).scalars()

    return render_template(f'check/index-{org_slug}.html', organization=org, checks=checks)
