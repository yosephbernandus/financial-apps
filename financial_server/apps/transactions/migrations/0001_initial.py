# Generated by Django 3.1.6 on 2021-02-13 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import financial_server.core.utils
import thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('balances', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Income'), (2, 'Outcome')])),
                ('amount', models.FloatField()),
                ('notes', models.TextField(blank=True, default='', null=True)),
                ('photo', thumbnails.fields.ImageField(blank=True, null=True, upload_to=financial_server.core.utils.FilenameGenerator(prefix='transactions'))),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('balance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='balances.balance')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
