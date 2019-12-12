import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='dionis0799',
                             db='qwe',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

print("connect successful!!")


def operation(sql):
    try:
        with connection.cursor() as cursor:

            cursor.execute(sql)
            print("cursor.description: ", cursor.description)
            print()
            for row in cursor:
                print(row)

    finally:
        connection.close()
