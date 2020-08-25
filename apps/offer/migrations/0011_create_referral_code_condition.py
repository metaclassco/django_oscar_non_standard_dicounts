# Generated by Django 2.2.13 on 2020-08-25 06:48

from django.db import migrations

from oscar.apps.offer.custom import create_condition


def create_referral_code_condition(apps, schema_editor):
    from apps.offer.conditions import ReferralCodeCondition

    create_condition(ReferralCodeCondition)


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0010_birthdaycondition'),
    ]

    operations = [
        migrations.RunPython(create_referral_code_condition)
    ]