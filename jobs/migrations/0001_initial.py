# Generated by Django 3.1.3 on 2020-11-26 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('location', models.CharField(max_length=64)),
                ('logo', models.URLField(default='https://place-hold.it/100x60')),
                ('description', models.TextField()),
                ('employee_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('picture', models.URLField(default='https://place-hold.it/100x60')),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('skills', models.TextField()),
                ('description', models.TextField()),
                ('salary_min', models.IntegerField()),
                ('salary_max', models.IntegerField()),
                ('published_at', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='vacancies', to='jobs.company')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                related_name='vacancies', to='jobs.specialty')),
            ],
        ),
    ]
