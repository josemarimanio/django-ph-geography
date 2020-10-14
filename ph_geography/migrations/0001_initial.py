from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('population', models.PositiveIntegerField(null=True, verbose_name='Population')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('island_group', models.CharField(choices=[('L', 'LUZON'), ('V', 'VISAYAS'), ('M', 'MINDANAO')], max_length=1, verbose_name='Island Group')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
                'db_table': 'ph_geography_region',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('population', models.PositiveIntegerField(null=True, verbose_name='Population')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('income_class', models.CharField(blank=True, choices=[('1', '1ST'), ('2', '2ND'), ('3', '3RD'), ('4', '4TH'), ('5', '5TH'), ('6', '6TH'), ('S', 'SPECIAL')], max_length=1, verbose_name='Income Class')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provinces', related_query_name='province', to='ph_geography.region', verbose_name='Region')),
            ],
            options={
                'verbose_name': 'Province',
                'verbose_name_plural': 'Provinces',
                'db_table': 'ph_geography_province',
            },
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('population', models.PositiveIntegerField(null=True, verbose_name='Population')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('is_city', models.BooleanField(verbose_name='Is City')),
                ('is_capital', models.BooleanField(verbose_name='Is Capital')),
                ('city_class', models.CharField(blank=True, choices=[('C', 'CC'), ('I', 'ICC'), ('H', 'HUC')], max_length=1, verbose_name='City Class')),
                ('income_class', models.CharField(blank=True, choices=[('1', '1ST'), ('2', '2ND'), ('3', '3RD'), ('4', '4TH'), ('5', '5TH'), ('6', '6TH'), ('S', 'SPECIAL')], max_length=1, verbose_name='Income Class')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipalities', related_query_name='municipality', to='ph_geography.province', verbose_name='Province')),
            ],
            options={
                'verbose_name': 'Municipality',
                'verbose_name_plural': 'Municipalities',
                'db_table': 'ph_geography_municipality',
            },
        ),
        migrations.CreateModel(
            name='Barangay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('population', models.PositiveIntegerField(null=True, verbose_name='Population')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('is_urban', models.NullBooleanField(null=True, verbose_name='Is Urban')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barangays', related_query_name='barangays', to='ph_geography.municipality', verbose_name='Barangay')),
            ],
            options={
                'verbose_name': 'Barangay',
                'verbose_name_plural': 'Barangays',
                'db_table': 'ph_geography_barangay',
            },
        ),
    ]
