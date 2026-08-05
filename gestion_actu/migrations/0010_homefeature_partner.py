from django.db import migrations, models


def seed_home_features(apps, schema_editor):
    HomeFeature = apps.get_model('gestion_actu', 'HomeFeature')
    ParametresAgence = apps.get_model('gestion_actu', 'ParametresAgence')
    settings = ParametresAgence.objects.first()

    defaults = [
        ('Site officiel', 'Zero arnaque'),
        ('Annonces verifiees', 'Biens controles'),
        ('Accompagnement', 'Conseils personnalises'),
        ('Transactions securisees', 'En toute simplicite'),
    ]

    if settings:
        defaults = [
            (settings.feature1_title, settings.feature1_desc),
            (settings.feature2_title, settings.feature2_desc),
            (settings.feature3_title, settings.feature3_desc),
            (settings.feature4_title, settings.feature4_desc),
        ]

    replacements = {
        'ZÃ©ro': 'Zero',
        'vÃ©rifiÃ©es': 'verifiees',
        'contrÃ´lÃ©s': 'controles',
        'personnalisÃ©s': 'personnalises',
        'sÃ©curisÃ©es': 'securisees',
        'simplicitÃ©': 'simplicite',
    }

    def clean(value):
        for old, new in replacements.items():
            value = value.replace(old, new)
        return value

    for index, (title, description) in enumerate(defaults, start=1):
        HomeFeature.objects.create(
            title=clean(title or f'Champ {index}'),
            description=clean(description or ''),
            ordre=index,
            actif=True,
        )


def seed_partners(apps, schema_editor):
    Partner = apps.get_model('gestion_actu', 'Partner')
    names = [
        'Cimasso',
        'Sapec Burkina',
        'Neige Peinture',
        'Wendpanga Industrie',
        'Interieur Maison',
        'MutiHome Burkina',
    ]

    for index, name in enumerate(names, start=1):
        Partner.objects.create(nom=name, ordre=index, actif=True)


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_actu', '0009_parametresagence_feature1_desc_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('ordre', models.PositiveIntegerField(default=0)),
                ('actif', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Champ accueil',
                'verbose_name_plural': 'Champs accueil',
                'db_table': 'home_feature',
                'ordering': ['ordre', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=120)),
                ('description', models.CharField(blank=True, max_length=220)),
                ('site_web', models.URLField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='partenaires/')),
                ('ordre', models.PositiveIntegerField(default=0)),
                ('actif', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Partenaire',
                'verbose_name_plural': 'Partenaires',
                'db_table': 'partner',
                'ordering': ['ordre', 'pk'],
            },
        ),
        migrations.RunPython(seed_home_features, migrations.RunPython.noop),
        migrations.RunPython(seed_partners, migrations.RunPython.noop),
    ]
