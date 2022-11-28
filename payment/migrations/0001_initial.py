# Generated by Django 4.1.3 on 2022-11-28 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('amount', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='income', to='courier.courier')),
            ],
        ),
        migrations.CreateModel(
            name='DailyIncome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_income', to='courier.courier')),
            ],
        ),
    ]