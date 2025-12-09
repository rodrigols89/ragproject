from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("workspace", "0002_alter_file_folder"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="file",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="folder",
            name="deleted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="folder",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]

