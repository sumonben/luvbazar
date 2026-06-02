# Generated migration to remove last_name field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='last_name',
        ),
    ]
