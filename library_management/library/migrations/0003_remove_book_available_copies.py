# Generated by Django 4.2.16 on 2024-11-28 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0002_alter_book_available_copies"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="available_copies",
        ),
    ]
