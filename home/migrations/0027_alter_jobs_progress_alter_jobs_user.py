# Generated by Django 4.1.7 on 2023-05-15 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_delete_chat_data_delete_contacts_delete_earnings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='progress',
            field=models.SmallIntegerField(max_length=110),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='user',
            field=models.EmailField(max_length=300),
        ),
    ]
