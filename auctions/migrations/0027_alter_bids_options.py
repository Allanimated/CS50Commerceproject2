# Generated by Django 4.2.3 on 2023-08-08 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_category_alter_bids_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bids',
            options={'verbose_name_plural': 'Bids'},
        ),
    ]