# Generated by Django 4.2.2 on 2023-07-24 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_categorymodel_is_top_category_votemodel_finger_print_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidatemodel',
            name='category',
            field=models.ManyToManyField(related_name='candidates', to='vote.categorymodel'),
        ),
    ]
