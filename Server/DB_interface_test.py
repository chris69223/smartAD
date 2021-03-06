import pymysql

conn_info = {
    'host': '*********',
    'user': '*******',
    'password': '******',
    'db': '*****',
    'charset': 'utf8'
}


class DB_interface:
    # 객체 생성과 동시에 DB 서버와 연결
    def __init__(self):
        self.conn = pymysql.connect(
            host=conn_info['host'],
            user=conn_info['user'],
            password=conn_info['password'],
            db=conn_info['db'],
            charset=conn_info['charset'])
        print("+++ Database connecting success! database:", conn_info['db'])
        self.curs = self.conn.cursor()

    # 서버가 닫히면 DB 연결도 종료
    def __del__(self):
        print("---Database connecting terminate")
        self.conn.close()

    # 광고정보 조회시 호출
    def showAD(self):
        try:
            sql = "select * from AD"
            self.curs.execute(sql)
            rows = self.curs.fetchall()
            return rows
        except Exception as e:
            print("에러 발생!!", e)

    # 광고정보 추가시 호출
    def insertAD(self, AD_ID, target, gender, age):
        try:
            sql = "insert into AD values " \
                  "(%s, %s, %s, %s, %s)"
            self.curs.execute(sql, (AD_ID, target, gender, age, '0'))
            self.conn.commit()
        except Exception as e:
            print("에러 발생!!", e)

    # 광고정보 삭제시 호출
    def deleteAD(self, target):
        try:
            sql = "delete from AD where target = %s"
            self.curs.execute(sql, target)
            self.conn.commit()
        except Exception as e:
            print("에러 발생!!", e)

    # 최종 결정된 성별, 연령대를 바탕으로 송출 광고 결정
    def decideID(self, gender, age):
        try:
            sql = "select target from AD where " \
                  "target_gender = %s and target_age = %s order by rand() limit 1"
            self.curs.execute(sql, (gender, age))
            rows = self.curs.fetchone()
            return rows[0]
        except Exception as e:
            print("에러 발생!!", e)

    # 얼굴이 인식되지 않았을 경우 해당 시간대에 많이 인식된 성별과 연령대 추출
    def findMajority(self, time):
        try:
            sql = "select gender, age, count(*) as cnt from recog_result where " \
                  "time = %s group by gender, age order by cnt desc"
            self.curs.execute(sql, (time))
            rows = self.curs.fetchone()
            return rows[0], rows[1]
        except Exception as e:
            print("에러 발생!!", e)

    # 얼굴인식에 성공했을 경우 인식결과를 통계 테이블에 추가
    def insertRecogResult(self, gender, age, time):
        try:
            sql = "insert into recog_result " \
                  "values(%s, %s, default, %s)"
            self.curs.execute(sql, (gender, age, time))
            self.conn.commit()
        except Exception as e:
            print("에러 발생!!", e)

    # 광고판에서 디지털 트윈 광고 선택 시/QR 링크 스캔 시 광고 관심지수 상승
    def increaseInterestIndex(self, AD_ID, num):
        try:
            sql = "update AD set int_point = int_point + %s " \
                  "where AD_ID = %s"
            self.curs.execute(sql, (num, AD_ID))
            self.conn.commit()
        except Exception as e:
            print("에러 발생!!", e)

    def lookUpTimeStat(self, time):
        try:
            sql = "select gender, age, count(*) as cnt " \
                  "from recog_result where time=%s "\
                  "group by gender, age"
            self.curs.execute(sql, time)
            rows = self.curs.fetchall()
            return rows
        except Exception as e:
            print("에러 발생!!", e)

    def lookUpADStat(self):
        try:
            sql = "select AD_ID, int_point from AD " \
                  "order by int_point desc"
            self.curs.execute(sql)
            rows = self.curs.fetchmany(10)
            return rows
        except Exception as e:
            print("에러 발생!!", e)

    # 인식결과에서 max 값을 가진 인덱스가 여러개일 경우, 해당 튜플들의 인식횟수를 리턴
    def recogCount(self, gender, age, time):
        try:
            sql = "select count(*) from recog_result" \
                  "where time=%s and gender=%s and age=%s group by gender, age"
            self.curs.execute(sql, (time, gender, age))
            row = self.curs.fetchone()
            return row
        except Exception as e:
            print("에러 발생!!", e)
            return int(0)
