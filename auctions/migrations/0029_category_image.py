# Generated by Django 4.2.3 on 2023-08-08 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0028_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]