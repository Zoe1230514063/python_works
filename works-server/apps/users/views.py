from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudentSerializer
from django.db import connection

@api_view(['POST'])
def login(request):
    role = request.data.get('role')
    uid  = request.data.get('uid')
    name = request.data.get('name')

    if role == 'student':
        user = StudentSerializer.get_student(uid, name)
        return Response({'role': 'student', 'data': user} if user else {'error': '无此学生'})

    if role == 'teacher':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT TNO, TNAME, TCONTACT
                FROM TEACHERS
                WHERE TNO = %s AND TNAME = %s
            """, [uid, name])
            row = cursor.fetchone()
        if row:
            return Response({'role': 'teacher', 'data': {
                'tno': row[0],
                'tname': row[1],
                'tcontact': row[2]
            }})
        return Response({'error': '无此教师'})

    return Response({'error': '参数错误'})


@api_view(['GET'])
def students_list(request):
    tno = request.GET.get('tno')
    if not tno:
        return Response({'error': '缺少 tno 参数'}, status=400)

    sql = """
        SELECT SNO           AS sno,
               SNAME         AS sname,
               SSEX          AS ssex,
               C.CLASS_NAME  AS class_name,
               SCONTACT      AS scontact
        FROM students S
        INNER JOIN classes  C ON C.CLASS_ID = S.CLASS_ID
        INNER JOIN teachers T ON T.CLASS_ID = S.CLASS_ID
        WHERE T.TNO = %s
        ORDER BY S.SNO
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, [tno])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    data = [dict(zip(columns, row)) for row in rows]
    return Response(data)


@api_view(['POST'])
def student_add(request):
    sno   = request.data.get('sno')
    sname = request.data.get('sname')
    ssex  = request.data.get('ssex')
    class_id = request.data.get('class_id')
    scontact = request.data.get('scontact') or None

    if not all([sno, sname, ssex, class_id]):
        return Response({'error': '缺少必填字段'}, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO STUDENTS (SNO, SNAME, SSEX, CLASS_ID, SCONTACT)
                VALUES (%s, %s, %s, %s, %s)
            """, [sno, sname, ssex, class_id, scontact])
        return Response({'message': '学生已新增'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['DELETE'])
def student_delete(request, sno):
    """按学号删除学生"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM STUDENTS WHERE SNO = %s", [sno])
        return Response({'message': '学生已删除'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)