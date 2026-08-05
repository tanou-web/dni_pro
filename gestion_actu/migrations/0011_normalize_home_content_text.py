from django.db import migrations


REPLACEMENTS = {
    'ZÃ©ro': 'Zero',
    'vÃ©rifiÃ©es': 'verifiees',
    'contrÃ´lÃ©s': 'controles',
    'personnalisÃ©s': 'personnalises',
    'sÃ©curisÃ©es': 'securisees',
    'simplicitÃ©': 'simplicite',
    'IntÃ©rieur': 'Interieur',
}


def normalize_text(value):
    for old, new in REPLACEMENTS.items():
        value = value.replace(old, new)
    return value


def normalize_home_content(apps, schema_editor):
    HomeFeature = apps.get_model('gestion_actu', 'HomeFeature')
    Partner = apps.get_model('gestion_actu', 'Partner')

    for feature in HomeFeature.objects.all():
        feature.title = normalize_text(feature.title)
        feature.description = normalize_text(feature.description)
        feature.save(update_fields=['title', 'description'])

    for partner in Partner.objects.all():
        partner.nom = normalize_text(partner.nom)
        partner.description = normalize_text(partner.description)
        partner.save(update_fields=['nom', 'description'])


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_actu', '0010_homefeature_partner'),
    ]

    operations = [
        migrations.RunPython(normalize_home_content, migrations.RunPython.noop),
    ]
