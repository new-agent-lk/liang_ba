from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_userprofile_user_category"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UserCategory",
        ),
    ]
