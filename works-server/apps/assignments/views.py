from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from django.db import transaction

@api_view(['GET'])
def assignment_list(request):
    sno = request.GET.get('sno', '').strip()
    if not sno:
        return Response([])
    sql = """
        SELECT  A.ASSIGNMENT_ID                             AS assignments_id,
                A.ASSIGNMENT_TITLE                          AS assignments_title,
                A.DESCRIPTION                               AS description,
                FORMAT(A.PUBLISH_TIME, 'yyyy-MM-dd HH:mm')  AS publish_time,
                T.TNAME                                     AS teacher,
                CASE WHEN ISNULL(CAST(S.ANSWER AS NVARCHAR(MAX)), '') <> '' THEN 1 ELSE 0 END AS submitted,
                ISNULL(S.SCORE, '')                         AS score
        FROM ASSIGNMENTS A
        JOIN TEACHERS T ON T.TNO = A.TNO
        JOIN CLASSES C ON C.CLASS_ID = A.CLASS_ID
        JOIN STUDENTS ST ON ST.CLASS_ID = C.CLASS_ID
        LEFT JOIN SUBMISSIONS S ON S.ASSIGNMENT_ID = A.ASSIGNMENT_ID AND S.SNO = %s
        WHERE ST.SNO = %s
        ORDER BY A.PUBLISH_TIME DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, [sno, sno])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    return Response([dict(zip(columns, row)) for row in rows])


@api_view(['POST'])
@transaction.atomic
def publish_assignment(request):
    tno           = request.data.get('tno')
    assignment_id = str(request.data.get('assignment_id')).strip()
    title         = request.data.get('title')
    description   = request.data.get('description')
    class_id      = str(request.data.get('class_id')).strip()

    if not all([assignment_id, tno, title, description, class_id]):
        return Response({'error': '参数缺失'}, status=400)

    try:
        with connection.cursor() as cursor:
            # 1. 插入作业
            cursor.execute("""
                INSERT INTO ASSIGNMENTS
                (ASSIGNMENT_ID, ASSIGNMENT_TITLE, DESCRIPTION, PUBLISH_TIME, CLASS_ID, TNO)
                VALUES (%s, %s, %s, GETDATE(), %s, %s)
            """, [assignment_id, title, description, class_id, tno])

            # 2. 分发作业
            cursor.execute("""
                INSERT INTO SUBMISSIONS (SUBMISSION_ID, ASSIGNMENT_ID, SNO, SUBMIT_TIME)
                SELECT CONCAT(%s, '_', SNO), %s, SNO, NULL
                FROM STUDENTS
                WHERE CLASS_ID = %s
            """, [assignment_id, assignment_id, class_id])

        return Response({'message': '发布并分发成功'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['DELETE'])
def delete_assignment(request, assignment_id):
    try:
        with connection.cursor() as cursor:
            # 1. 删除作业
            cursor.execute("DELETE FROM ASSIGNMENTS WHERE ASSIGNMENT_ID = %s", [assignment_id])
            # 2. 级联删除所有提交记录
            cursor.execute("DELETE FROM SUBMISSIONS WHERE ASSIGNMENT_ID = %s", [assignment_id])
        return Response({'message': '作业及提交记录已删除'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def my_assignments(request):
    tno = request.GET.get('tno')
    if not tno:
        return Response([])

    sql = """
        SELECT A.ASSIGNMENT_ID          AS assignment_id,
               A.ASSIGNMENT_TITLE       AS assignment_title,
               A.DESCRIPTION            AS description,
               FORMAT(A.PUBLISH_TIME, 'yyyy-MM-dd HH:mm') AS publish_time,
               C.CLASS_NAME             AS class_name
        FROM ASSIGNMENTS A
        JOIN CLASSES C ON C.CLASS_ID = A.CLASS_ID
        WHERE A.TNO = %s
        ORDER BY A.PUBLISH_TIME DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, [tno])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    return Response([dict(zip(columns, row)) for row in rows])

@api_view(['GET'])
def assignment_detail(request):
    aid = request.GET.get('assignment_id')
    sql = "SELECT ASSIGNMENT_TITLE AS title FROM ASSIGNMENTS WHERE ASSIGNMENT_ID = %s"
    with connection.cursor() as cursor:
        cursor.execute(sql, [aid])
        row = cursor.fetchone()
    return Response({'title': row[0] if row else ''})

@api_view(['GET'])
def student_list_for_assignment(request):
    aid = request.GET.get('assignment_id')
    tno = request.GET.get('tno')
    if not aid or not tno:
        return Response({'error': '缺少参数'}, status=400)

    sql = """
        SELECT  ST.SNAME                                    AS sname,
                CAST(S.ANSWER AS NVARCHAR(MAX))             AS answer,
                FORMAT(S.SUBMIT_TIME, 'yyyy-MM-dd HH:mm')   AS submit_time,
                ISNULL(S.SCORE, '')                         AS score
        FROM    STUDENTS ST
        JOIN    CLASSES   C  ON C.CLASS_ID = ST.CLASS_ID
        JOIN    TEACHERS  T  ON T.CLASS_ID = C.CLASS_ID
        LEFT JOIN SUBMISSIONS S
            ON S.SNO = ST.SNO
            AND S.ASSIGNMENT_ID = %s
        WHERE   T.TNO = %s
        ORDER BY ST.SNO
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, [aid, tno])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    return Response([dict(zip(columns, row)) for row in rows])