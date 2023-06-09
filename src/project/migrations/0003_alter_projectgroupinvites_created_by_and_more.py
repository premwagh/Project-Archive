# Generated by Django 4.2.1 on 2023-05-09 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import project.models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("user", "0003_faculty"),
        ("project", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ProjectGroupInvite",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="created_invites",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="ProjectGroupInvite",
            name="expires_on",
            field=models.DateTimeField(
                default=project.models.get_invite_expiry, verbose_name="Expires On"
            ),
        ),
        migrations.AlterField(
            model_name="ProjectGroupInvite",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="invites",
                to="user.student",
            ),
        ),
    ]
