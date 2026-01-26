# Generated migration for SSL Commerz fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='method',
        ),
        migrations.AddField(
            model_name='payment',
            name='method',
            field=models.CharField(
                choices=[
                    ('sslcommerz', 'SSL Commerz'),
                    ('stripe', 'Stripe'),
                    ('paypal', 'PayPal'),
                    ('bank_transfer', 'Bank Transfer'),
                    ('cash_on_delivery', 'Cash on Delivery'),
                ],
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='payment',
            name='sslc_val_id',
            field=models.CharField(
                blank=True,
                help_text='SSL Commerz Validation ID',
                max_length=100,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='payment',
            name='sslc_tran_id',
            field=models.CharField(
                blank=True,
                help_text='SSL Commerz Transaction ID',
                max_length=100,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='payment',
            name='bank_tran_id',
            field=models.CharField(
                blank=True,
                help_text='Bank Transaction ID',
                max_length=100,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='payment',
            name='card_type',
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='payment',
            name='card_issuer',
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='payment',
            name='card_number',
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True
            ),
        ),
    ]
