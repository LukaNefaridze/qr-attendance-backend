# Generated manually for adding nonce field to Session

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_course_created_at_course_updated_at_timetable_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='nonce',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

