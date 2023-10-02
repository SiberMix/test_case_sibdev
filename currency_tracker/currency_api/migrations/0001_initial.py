# Generated by Django 4.2.5 on 2023-10-02 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyQuote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_currency', models.CharField(max_length=3)),
                ('quoted_currency', models.CharField(max_length=3)),
                ('date', models.DateField()),
                ('value', models.DecimalField(decimal_places=4, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='TrackedQuote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold_value', models.DecimalField(decimal_places=4, max_digits=10)),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currency_api.currencyquote')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuoteAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold_exceeded', models.BooleanField()),
                ('max_value', models.BooleanField()),
                ('min_value', models.BooleanField()),
                ('percentage_difference', models.DecimalField(decimal_places=4, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currency_api.currencyquote')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
