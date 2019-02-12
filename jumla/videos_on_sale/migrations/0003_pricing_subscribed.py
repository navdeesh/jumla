# Generated by Django 2.1.7 on 2019-02-12 09:48

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos_on_sale', '0002_auto_20190212_0914'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pricing_daily_basis', models.IntegerField(max_length=6)),
                ('pricing_weekly_basis', models.IntegerField(max_length=6)),
                ('pricing_monthly_basis', models.IntegerField(max_length=6)),
                ('pricing_yearly_basis', models.IntegerField(max_length=6)),
                ('content_foreign_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos_on_sale.ContentEntity')),
                ('user_foreign_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos_on_sale.Users')),
            ],
        ),
        migrations.CreateModel(
            name='Subscribed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribed_amount', models.IntegerField(max_length=6)),
                ('subscribed_duration', models.CharField(max_length=10)),
                ('subscribed_start_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('content_foreign_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos_on_sale.ContentEntity')),
                ('user_foreign_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos_on_sale.Users')),
            ],
        ),
    ]
