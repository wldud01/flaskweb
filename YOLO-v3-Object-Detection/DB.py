import pymysql
from flask import jsonify

# mysql imformation
HOST = '127.0.0.1'
PORT = 
USER = 'root'
PASSWORD = 
conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database='recipe', charset='utf8')
#-----------------------------------------------------------------

#f for connect
curs = conn.cursor()
sql = "SELECT* FROM data WHERE CKG_NM LIKE '%어묵%'"
curs.execute(sql)
rows = curs.fetchall()


def food():
    food = rows
    return food
print(food())
if conn.open:
    with conn.cursor() as curs:
        print('connected')
conn.close()
#execute 객체에 sql문을 실행
#executemany cursor 객체에 동일한 sql문에 파라미터를 변경하여 실행
#executescript cursor 객체에 세미콜론으로 구분된 여러줄의 sql문
#fetchone 데이터 한개 반환
# fechall 리스트 형태로 모두 반환
