from django.db import models

class Assignment(models.Model):
    assignments_id = models.IntegerField(primary_key=True, db_column='ASSIGNMENTS_ID')
    assignments_title = models.CharField(max_length=200, db_column='ASSIGNMENTS_TITLE')
    description = models.TextField(db_column='DESCRIPTION')
    publish_time = models.DateTimeField(db_column='PUBLISH_TIME')

    class Meta:
        db_table = 'ASSIGNMENTS'
        managed = False