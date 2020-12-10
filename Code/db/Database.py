import pymysql
import os

class Database():
    def __init__(self):
        host = os.environ['MYSQLHost']
        user = os.environ['MYSQLName']
        password = os.environ['MYSQLPwd']
        db_name = "planning"
        self.db = pymysql.connect(
            user=user, 
            passwd=password, 
            host=host, 
            db=db_name, 
            charset='utf8'
        )

    def insertFeatureImportance(self, values):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO feature_importances (user_name, paralysis, voice, feeding_tube, vision, cognitive, perception, self_care, incontinence, emotion, sex) VALUES ('{0}', {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10});".format(*values)
        cursor.execute(sql)
        self.db.commit()

    def insertFeedback(self, values):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO feedbacks (user_name, feedback) VALUES ('{0}', '{1}');".format(*values)
        cursor.execute(sql)
        self.db.commit()

    def insertAnswers(self, values):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO answers (user_name, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}', '{20}', '{21}', '{22}', '{23}', '{24}');".format(*values)
        cursor.execute(sql)
        self.db.commit()

    def insertEval(self, values):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO evaluations (user_name, evaluation) VALUES ('{0}', {1});".format(*values)
        cursor.execute(sql)
        self.db.commit()

    def closeConnection(self):
        self.db.close()