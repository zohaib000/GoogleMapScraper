# Generated by Django 4.0.2 on 2022-07-11 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_contacts_whatsapp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='account_type',
        ),
        migrations.DeleteModel(
            name='daily_ads_clicks',
        ),
        migrations.DeleteModel(
            name='display_article_ads',
        ),
        migrations.DeleteModel(
            name='display_daimond_ads',
        ),
        migrations.DeleteModel(
            name='display_feed_ads',
        ),
        migrations.DeleteModel(
            name='display_square_ads',
        ),
        migrations.DeleteModel(
            name='investment_payments',
        ),
        migrations.DeleteModel(
            name='investment_plan_activation',
        ),
        migrations.DeleteModel(
            name='request_for_investment_plan_activation',
        ),
        migrations.DeleteModel(
            name='user_clicks_ads',
        ),
    ]
