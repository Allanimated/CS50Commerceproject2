# Generated by Django 4.2.3 on 2023-07-24 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_auctionlisting_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(upload_to='auctions/static/images/'),
        ),
    ]
