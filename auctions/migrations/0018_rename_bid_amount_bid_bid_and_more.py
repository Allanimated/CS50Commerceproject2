# Generated by Django 4.2.3 on 2023-07-31 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='bid_amount',
            new_name='bid',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='active_listing',
            new_name='listing',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='active_listing',
            new_name='listing',
        ),
    ]
