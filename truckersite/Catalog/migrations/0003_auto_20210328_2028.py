# Generated by Django 3.1.7 on 2021-03-29 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Catalog', '0002_auto_20210328_2015'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default='NO_DESCRIPTION', max_length=2000),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='SLUG'),
        ),
    ]