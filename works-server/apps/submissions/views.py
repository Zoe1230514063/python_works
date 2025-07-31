from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from django.db import transaction

@api_view(['POST'])
@transaction.atomic
def submit_assignment(request):
    aid = str(request.data.get('assignments_id')).strip()
    sno = str(request.data.get('sno')).strip()
    ans = request.data.get('answer', '')

    if not (aid and sno):
        return Response({'error': '参数缺失'}, status=400)

    sid = f"{aid}_{sno}"

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                MERGE SUBMISSIONS AS target
                USING (SELECT %s AS SUBMISSION_ID, %s AS ASSIGNMENT_ID, %s AS SNO, %s AS ANSWER) AS source
                ON target.SUBMISSION_ID = source.SUBMISSION_ID
                WHEN MATCHED THEN
                    UPDATE SET ANSWER = source.ANSWER, SUBMIT_TIME = GETDATE()
                WHEN NOT MATCHED THEN
                    INSERT (SUBMISSION_ID, ASSIGNMENT_ID, SNO, ANSWER, SUBMIT_TIME)
                    VALUES (source.SUBMISSION_ID, source.ASSIGNMENT_ID, source.SNO, source.ANSWER, GETDATE());
            """, [sid, aid, sno, ans])
        return Response({'message': '提交成功'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def to_mark_list(request):
    tno = request.GET.get('tno')
    if not tno:
        return Response({'error': '缺少 tno 参数'}, status=400)

    sql = """
        SELECT 
            S.SUBMISSION_ID                             AS submissions_id,
            A.ASSIGNMENT_TITLE                          AS assignments_title,
            ST.SNAME                                    AS sname,
            CAST(S.ANSWER AS NVARCHAR(MAX))             AS answer,
            FORMAT(S.SUBMIT_TIME, 'yyyy-MM-dd HH:mm')   AS submit_time,
            S.SCORE                                     AS score
        FROM SUBMISSIONS S
        JOIN ASSIGNMENTS A   ON A.ASSIGNMENT_ID = S.ASSIGNMENT_ID
        JOIN STUDENTS   ST   ON ST.SNO = S.SNO
        JOIN CLASSES    C    ON C.CLASS_ID = ST.CLASS_ID
        JOIN TEACHERS   T    ON T.CLASS_ID = C.CLASS_ID
        WHERE S.ANSWER IS NOT NULL 
          AND CAST(S.ANSWER AS NVARCHAR(MAX)) != ''
          AND T.TNO = %s
        ORDER BY S.SUBMIT_TIME DESC
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, [tno])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    return Response([dict(zip(columns, row)) for row in rows])


@api_view(['PUT'])
def update_score(request, sid):
    score = request.data.get('score')
    if score is None:
        return Response({'error': '缺少分数'}, status=400)

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE SUBMISSIONS SET SCORE = LTRIM(RTRIM(%s)) WHERE SUBMISSION_ID = %s",
                [str(score), sid.strip()]
            )
        return Response({'message': '已保存'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)