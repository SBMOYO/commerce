# Generated by Django 4.2.1 on 2023-05-27 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auction_listings_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listings',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auctions.category'),
        ),
    ]
