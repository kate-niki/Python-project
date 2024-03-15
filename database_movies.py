import mysql.connector

# Параметры подключения к базе данных movies
movies_dbconfig = {'host': '',
                   'user': '',
                   'password': '',
                   'database': ''}

def read_from_movies():
    try:
        # Установка соединения с базой данных movies
        movies_connection = mysql.connector.connect(**movies_dbconfig)
        movies_cursor = movies_connection.cursor()

        # Выполнение запроса для чтения данных из movies
        read_query = "SELECT * FROM movies.movies"
        movies_cursor.execute(read_query)
        movies_data = movies_cursor.fetchall()

        # Закрытие соединения с базой данных movies
        movies_cursor.close()
        movies_connection.close()

        return movies_data
    except mysql.connector.Error as err:
        print("Произошла ошибка при чтении данных из базы данных movies:", err)
        return None