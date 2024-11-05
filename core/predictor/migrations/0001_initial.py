# Generated by Django 4.2.16 on 2024-11-05 14:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Predictor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "female_age",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(10),
                            django.core.validators.MaxValueValidator(99),
                        ]
                    ),
                ),
                ("AMH", models.DecimalField(decimal_places=2, max_digits=4)),
                ("FSH", models.DecimalField(decimal_places=2, max_digits=4)),
                ("no_embryos", models.IntegerField()),
                (
                    "endoendometerial_tickness",
                    models.DecimalField(decimal_places=2, max_digits=4),
                ),
                ("sperm_count", models.DecimalField(decimal_places=2, max_digits=4)),
                ("sperm_morphology", models.IntegerField()),
                ("follicle_size", models.IntegerField()),
                ("no_of_retreived_oocytes", models.IntegerField()),
                ("qality_of_embryo", models.IntegerField()),
                ("quality_of_retreived_oocytes_MI", models.IntegerField()),
                ("quality_of_retreived_oocytes_MII", models.IntegerField()),
                ("result", models.IntegerField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.profile",
                    ),
                ),
            ],
        ),
    ]
