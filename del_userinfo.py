import pymysql

host = "localhost"
port = 3306
user = "root"
passwd = "2020Cnic@!"

db = "oj"
table = "User"

def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=passwd)
    return conn

def del_oj_User():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("drop table %s" % table)
    
    cursor.close()
    conn.close()
if __name__ == '__main__':
    del_oj_User()