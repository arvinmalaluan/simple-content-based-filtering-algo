# Generated by Django 4.2.5 on 2023-10-01 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_remove_conversation_id_alter_conversation_custom_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='custom_key',
            field=models.CharField(blank=True, max_length=20, primary_key=True, serialize=False),
        ),
    ]
