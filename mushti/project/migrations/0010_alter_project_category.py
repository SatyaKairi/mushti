# Generated by Django 4.1 on 2022-08-12 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_rename_project_projectimages_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='category',
            field=models.CharField(choices=[('Art', 'Art'), ('Culture', 'Culture'), ('Social', 'Social'), ('Creativity', 'Creativity'), ('Education', 'Education'), ('Film', 'Film'), ('Food & Crafts', 'Food & Crafts'), ('Game', 'Game'), ('Music', 'Music'), ('Publishing', 'Publishing'), ('Others', 'Others')], default='Others', max_length=50),
        ),
    ]
