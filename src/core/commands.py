import os

import click
from flask import current_app
from sqlalchemy import select

from src.core.extensions import db

def register_commands(app):
    @app.cli.command()
    @click.option('--drop',is_flag=True,help='Crate after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm(
                'This operation will delete the database, do you want to continue?',
                abort=True
            )
            db.drop_all()
            click.echo('Dropped tables.')
        db.create_all()
        click.echo('Initialized the database.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    @click.option('--reply', default=50, help='Quantity of replies, default is 50.')
    def fake(category, post, comment, reply):
        """Generate fake data."""
        from src.fakes import fake_admin, fake_menu, fake_role_menu,\
            fake_role,fake_user_role

        db.drop_all()
        db.create_all()

        click.echo('Generated the administrator.')
        fake_admin()

        fake_menu()
        click.echo(f'Generated menu.')

        fake_role()
        click.echo(f'Generated role')

        fake_role_menu()
        click.echo(f'Generated fake_role_menu.')


        fake_user_role()
        click.echo(f'fake_user_role')

        click.echo(f'fake_customer_info')