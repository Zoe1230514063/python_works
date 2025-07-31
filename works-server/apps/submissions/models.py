from django.db import models

class Submission(models.Model):
    submissions_id = models.IntegerField(primary_key=True, db_column='SUBMISSIONS_ID')
    assignments_id = models.IntegerField(db_column='ASSIGNMENTS_ID')
    sno = models.IntegerField(db_column='SNO')
    answer = models.TextField(db_column='ANSWER', blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'SUBMISSIONS'
        managed = False