# Generated by Django 2.2.6 on 2019-12-16 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HerokuTeam',
            fields=[
                ('pk_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HerokuCost',
            fields=[
                ('pk_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('report_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportDate')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heroku.HerokuTeam')),
            ],
        ),
    ]
