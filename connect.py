import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='dionis0799',
                             db='qwe',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print("connect successful!!")

try:
    with connection.cursor() as cursor:

        sql = "source hostel.txt"
        cursor.execute(sql)
        print("cursor.description: ", cursor.description)
        print()
        for row in cursor:
            print(row)

finally:
    connection.close()
