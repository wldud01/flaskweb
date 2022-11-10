import pymysql
from flask import request

class MyEmpDao:
    def __init__(self):
        pass

    def getEmps(self, a):
        ret = []    # my sql 접근
        db = pymysql.connect(host='localhost', user='root', db='recipe', password='dbswldud04286!', charset='utf8')
        curs = db.cursor()
        mtr = len(a)
        sql = f"SELECT* FROM data WHERE "
        for i in range(0, mtr):
            if mtr == 1:
                plus = f"CKG_MTRL_CN LIKE '%{str(a[i])}%';"
                sql = sql + plus
            elif mtr != 1 and i == 0:
                plus = f"CKG_MTRL_CN LIKE '%{str(a[i])}%'"
                sql = sql + plus
            elif i >= 1 and a[i] == a[i-1]:
                print("same")
            else:
                plus = ' '+"AND" + ' ' + f"CKG_MTRL_CN LIKE '%{str(a[i])}%' "
                sql = sql + plus

            print(i, " ", sql)
        sql = sql + ' Limit 20;'
        curs.execute(sql)
        rows = curs.fetchall()
        for e in rows:
            temp = {'CKG_NM': e[0], 'CKG_MTH_ACTO_NM': e[1], 'CKG_STA_ACTO_NM': e[2],
                    'CKG_KND_ACTO_NM': e[3], 'CKG_IPDC': e[4], 'CKG_MTRL_CN': e[5]
                ,'CKG_INBUN_NM': e[6], 'CKG_DODF_NM': e[7], 'CKG_TIME_NM': e[8]
                    }
            ret.append(temp)
        db.commit()
        db.close()
        return ret

    def insEmp(self, CKG_NM, CKG_MTH_ACTO_NM, CKG_STA_ACTO_NM, CKG_KND_ACTO_NM, CKG_IPDC, CKG_MTRL_CN
                    ,CKG_INBUN_NM, CKG_DODF_NM, CKG_TIME_NM):
        db = pymysql.connect(host='localhost', user='root', db='recipe', password='dbswldud04286!', charset='utf8')
        curs = db.cursor()

        sql = '''insert into emp (CKG_NM, CKG_MTH_ACTO_NM, CKG_STA_ACTO_NM, CKG_KND_ACTO_NM, CKG_IPDC, CKG_MTRL_CN
                    ,CKG_INBUN_NM, CKG_DODF_NM, CKG_TIME_NM) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        curs.execute(sql, (CKG_NM, CKG_MTH_ACTO_NM, CKG_STA_ACTO_NM, CKG_KND_ACTO_NM, CKG_IPDC, CKG_MTRL_CN
                    ,CKG_INBUN_NM, CKG_DODF_NM, CKG_TIME_NM))
        db.commit()
        db.close()

    def updEmp(self, CKG_NM, CKG_MTH_ACTO_NM, CKG_STA_ACTO_NM, CKG_KND_ACTO_NM, CKG_IPDC, CKG_MTRL_CN
                    ,CKG_INBUN_NM, CKG_DODF_NM, CKG_TIME_NM):
        db = pymysql.connect(host='localhost', user='root', db='recipe', password='dbswldud04286!', charset='utf8')
        curs = db.cursor()

        sql = "update emp set name=%s, department=%s, phone=%s where empno=%s"
        curs.execute(sql, (CKG_NM, CKG_MTH_ACTO_NM, CKG_STA_ACTO_NM, CKG_KND_ACTO_NM, CKG_IPDC, CKG_MTRL_CN
                    ,CKG_INBUN_NM, CKG_DODF_NM, CKG_TIME_NM))
        db.commit()
        db.close()


if __name__ == '__main__':
#MyEmpDao().insEmp('aaa', 'bb', 'cc', 'dd')
#MyEmpDao().updEmp('aa', 'dd', 'dd', 'aa')
#MyEmpDao().delEmp('aaa')
    emplist = MyEmpDao().getEmps();
    print(emplist)