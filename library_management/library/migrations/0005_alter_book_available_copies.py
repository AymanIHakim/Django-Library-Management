# Generated by Django 4.2.16 on 2024-11-28 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0004_book_available_copies"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="available_copies",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
