from django.db import models

class Student(models.Model):
    sno = models.IntegerField(primary_key=True, db_column='SNO')
    sname = models.CharField(max_length=50, db_column='SNAME')
    ssex = models.CharField(max_length=2, db_column='SSEX')
    scontact = models.CharField(max_length=50, db_column='SCONTACT', blank=True, null=True)

    class Meta:
        db_table = 'STUDENTS'
        managed = False

class Teacher(models.Model):
    tno = models.IntegerField(primary_key=True, db_column='TNO')
    tname = models.CharField(max_length=50, db_column='TNAME')
    tcontact = models.CharField(max_length=50, db_column='TCONTACT', blank=True, null=True)

    class Meta:
        db_table = 'TEACHERS'
        managed = False