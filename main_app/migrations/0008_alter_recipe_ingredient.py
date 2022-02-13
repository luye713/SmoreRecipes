# Generated by Django 4.0.2 on 2022-02-12 23:02

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_alter_recipe_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredient',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=30), blank=True, default=list, null=True, size=None),
        ),
    ]
