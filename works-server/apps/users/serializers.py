from rest_framework import serializers
from django.db import connection

class StudentSerializer(serializers.Serializer):
    sno        = serializers.IntegerField()
    sname      = serializers.CharField()
    class_name = serializers.CharField()
    scontact   = serializers.CharField()

    @staticmethod
    def get_student(sno, name):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT  S.SNO,
                        S.SNAME,
                        C.CLASS_NAME  AS class_name,
                        S.SCONTACT
                FROM    STUDENTS S
                JOIN    CLASSES  C ON C.CLASS_ID = S.CLASS_ID
                WHERE   S.SNO = %s AND S.SNAME = %s
            """, [sno, name])
            row = cursor.fetchone()
            if row:
                return dict(zip(['sno', 'sname', 'class_name', 'scontact'], row))
        return None