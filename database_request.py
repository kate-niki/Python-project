import mysql.connector

# Параметры подключения к базе данных dam29_movies_Kate
request_dbconfig = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''
}

def write_to_request(keyword):
    try:
        # Установка соединения с базой данных dam29_movies_Kate
        request_connection = mysql.connector.connect(**request_dbconfig)
        request_cursor = request_connection.cursor()

        # Запись данных в базу данных 290923_dam_Kate
        insert_query = "INSERT INTO request (keyword) VALUES (%s)"
        request_cursor.execute(insert_query, (keyword,))
        request_connection.commit()
        
        # Закрытие соединения с базой данных dam29_movies_Kate
        request_cursor.close()
        request_connection.close()  
    except mysql.connector.Error as err:
        print("Произошла ошибка при записи в базу данных:", err)

def read_from_request():
    try:
        # Установка соединения с базой данных dam29_movies_Kate
        request_connection = mysql.connector.connect(**request_dbconfig)
        request_cursor = request_connection.cursor()

        # Выполнение запроса для чтения данных из request
        read_query = "SELECT * FROM request"
        request_cursor.execute(read_query)
        request_data = request_cursor.fetchall()
        
        # Закрытие соединения с базой данных dam29_movies_Kate
        request_cursor.close()
        request_connection.close() 

        return request_data
    except mysql.connector.Error as err:
        print("Произошла ошибка при чтении данных из базы данных:", err)
        return None