from django.db import models

class Class(models.Model):
    class_id   = models.IntegerField(primary_key=True, db_column='CLASS_ID')
    class_name = models.CharField(max_length=50, db_column='CLASS_NAME')

    class Meta:
        db_table = 'CLASSES'
        managed = False