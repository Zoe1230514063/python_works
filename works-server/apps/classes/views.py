from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection

@api_view(['GET'])
def class_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT CLASS_ID, CLASS_NAME FROM CLASSES")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    data = [dict(zip(columns, row)) for row in rows]
    return Response(data)