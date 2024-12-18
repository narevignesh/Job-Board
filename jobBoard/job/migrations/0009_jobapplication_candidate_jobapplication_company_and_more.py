from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('job', '0008_jobpost_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='candidate',
            field=models.ForeignKey(
                null=True, 
                blank=True, 
                on_delete=django.db.models.deletion.CASCADE, 
                related_name='applications', 
                to='job.candidate'
            ),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='company',
            field=models.ForeignKey(
                null=True, 
                blank=True, 
                on_delete=django.db.models.deletion.CASCADE, 
                related_name='applications', 
                to='job.company'
            ),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='job_post',
            field=models.ForeignKey(
                null=True, 
                blank=True, 
                on_delete=django.db.models.deletion.CASCADE, 
                related_name='applications', 
                to='job.jobpost'
            ),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='user',
            field=models.ForeignKey(
                null=True, 
                blank=True, 
                on_delete=django.db.models.deletion.CASCADE, 
                related_name='applications', 
                to='job.usermaster'
            ),
        ),
    ]
