# Generated by Django 4.2.3 on 2023-07-31 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auctionlisting_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bidder',
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
