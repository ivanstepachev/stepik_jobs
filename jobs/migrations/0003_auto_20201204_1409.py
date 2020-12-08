# Generated by Django 3.1.3 on 2020-12-04 14:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0002_auto_20201201_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('code', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='application',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='applications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='company_images'),
        ),
        migrations.AlterField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                       related_name='company', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('surname', models.CharField(max_length=64)),
                ('status', models.BooleanField(default=True)),
                ('salary', models.IntegerField()),
                ('education', models.TextField()),
                ('experience', models.TextField()),
                ('portfolio', models.URLField()),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            related_name='resumes', to='jobs.grade')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                related_name='resumes', to='jobs.specialty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                           related_name='resumes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]