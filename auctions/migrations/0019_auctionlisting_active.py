# Generated by Django 4.2.3 on 2023-07-31 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_rename_bid_amount_bid_bid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='active',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
