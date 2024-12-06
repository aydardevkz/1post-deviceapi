# Generated by Django 4.2.5 on 2024-12-01 14:27

import config.settings.s3config
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppBanner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('title', models.TextField(db_index=True, max_length=500, verbose_name='title')),
                ('description', models.TextField(max_length=5000, verbose_name='description')),
                ('image', models.ImageField(storage=config.settings.s3config.NewsMediaStorage(), upload_to='avatar', verbose_name='image')),
                ('banner_type', models.SmallIntegerField(choices=[(1, 'Photo'), (2, 'News')], verbose_name='banner_type')),
                ('create_by', models.UUIDField(db_index=True, verbose_name='create_by')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created_at')),
            ],
            options={
                'verbose_name': 'AppBanner',
                'verbose_name_plural': 'AppBanner',
                'db_table': 'mdl_app_banner',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AppCountry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('country_name_kk', models.CharField(max_length=250, unique=True, verbose_name='country_name')),
                ('country_name_en', models.CharField(max_length=250, unique=True, verbose_name='country_name_en')),
                ('country_name_ru', models.CharField(max_length=250, unique=True, verbose_name='country_name_ru')),
                ('country_code', models.CharField(max_length=80, unique=True, verbose_name='country_code')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created_at')),
            ],
            options={
                'verbose_name': 'AppCountry',
                'verbose_name_plural': 'AppCountry',
                'db_table': 'mdl_app_country',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AppNews',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('title', models.TextField(db_index=True, max_length=500, verbose_name='title')),
                ('description', models.TextField(max_length=5000, verbose_name='description')),
                ('image', models.ImageField(storage=config.settings.s3config.NewsMediaStorage(), upload_to='avatar', verbose_name='image')),
                ('source_link', models.URLField(blank=True, null=True, verbose_name='source_link')),
                ('create_by', models.UUIDField(db_index=True, verbose_name='create_by')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created_at')),
            ],
            options={
                'verbose_name': 'AppNews',
                'verbose_name_plural': 'AppNews',
                'db_table': 'mdl_app_news',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AppValuta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('valuta_type', models.CharField(choices=[('USD', 'USD'), ('RUB', 'RUB'), ('KZT', 'KZT'), ('CNY', 'CNY')], max_length=80, verbose_name='valuta_type')),
                ('valuta_rate', models.DecimalField(decimal_places=6, max_digits=10, verbose_name='valuta_rate')),
                ('create_by', models.UUIDField(db_index=True, verbose_name='create_by')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created_at')),
            ],
            options={
                'verbose_name': 'AppValuta',
                'verbose_name_plural': 'AppValuta',
                'db_table': 'mdl_app_valuta',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AppArea',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('area_name_kk', models.CharField(max_length=250, verbose_name='area_name_kz')),
                ('area_name_en', models.CharField(max_length=250, verbose_name='area_name_en')),
                ('area_name_ru', models.CharField(max_length=250, verbose_name='area_name_ru')),
                ('area_code', models.CharField(db_index=True, max_length=80, unique=True, verbose_name='area_code')),
                ('area_type', models.SmallIntegerField(choices=[(1, 'province'), (2, 'city'), (3, 'district')], verbose_name='category_type')),
                ('post_code', models.CharField(blank=True, max_length=80, null=True, verbose_name='post_code')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='station_latitude')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='station_longitude')),
                ('zoom', models.FloatField(blank=True, null=True, verbose_name='zoom')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created_at')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_service.appcountry', verbose_name='country')),
                ('parent_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_area', to='app_service.apparea', verbose_name='parent_area')),
            ],
            options={
                'verbose_name': 'AppArea',
                'verbose_name_plural': 'AppArea',
                'db_table': 'mdl_app_area',
                'ordering': ['-created_at'],
            },
        ),
    ]
