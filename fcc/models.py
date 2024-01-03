from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship  # v2
from typing import List  # v2

# For utcnow()
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
# from sqlalchemy.types import DateTime


# Note: I'm using the new SQLAlchemy v2 syntax
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Organization(db.Model):
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(200), nullable=False)
    country: Mapped[str] = mapped_column(db.String(50), nullable=False)
    locale: Mapped[str] = mapped_column(db.String(5), nullable=False)
    slug: Mapped[str] = mapped_column(db.String(50), nullable=False)
    class_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    site_url: Mapped[str] = mapped_column(db.String(200), nullable=False)
    scrape_url: Mapped[str] = mapped_column(db.String(200), nullable=False)

    checks: Mapped[List['Check']] = relationship(
        back_populates='organization', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Org {self.id} | {self.name}>'



# Postgres-specific code to set server-side UTC timestamp
# https://docs.sqlalchemy.org/en/20/core/compiler.html#utc-timestamp-function
class utcnow(expression.FunctionElement):
    type = db.DateTime
    inherit_cache = True

@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
# End of Postgres-specific code


class Check(db.Model):
    __tablename__ = 'checks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    stmt_text: Mapped[str] = mapped_column(db.Text, nullable=False)
    stmt_date_iso: Mapped[str] = mapped_column(db.String(10), nullable=False)  # ISO date str
    stmt_date_locale: Mapped[str] = mapped_column(db.String(20), nullable=False)
    stmt_url: Mapped[str] = mapped_column(db.String(400), nullable=False)

    author_name: Mapped[str] = mapped_column(db.String(100), default='')
    author_title: Mapped[str] = mapped_column(db.String(200), default='')

    rating: Mapped[str] = mapped_column(db.String(50), default='')
    misc: Mapped[str] = mapped_column(db.Text, default='')
    
    scraped_at: Mapped[datetime] = mapped_column(db.DateTime, server_default=utcnow())

    organization_id: Mapped[int] = mapped_column(db.ForeignKey('organizations.id'))
    organization: Mapped['Organization'] = relationship(back_populates='checks')

    def __repr__(self):
        return f'<Check {self.id} | {self.stmt_text[:20]} | {self.organization_id}>'
