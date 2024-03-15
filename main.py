# Импорт модулей для работы с базой данных и пользовательским интерфейсом
from database_movies import read_from_movies
from database_request import write_to_request
from user_interface import (
    search_movie_by_keyword,
    search_movie_by_genre_and_year,
    display_popular_queries
)

def main():
    try:
        print("Добро пожаловать в приложение по поиску фильмов!")
        # Основной цикл работы приложения
        while True:
            print("\nМеню:")
            print("1. Поиск фильма по ключевому слову")
            print("2. Поиск фильма по жанру и/или году")
            print("3. Вывод запросов пользователя")
            print("4. Выход")

            # Получение выбора пользователя
            choice = input("Выберите действие: ")

            # Выполнение соответствующего действия в зависимости от выбора пользователя
            if choice == '1':
                search_movie_by_keyword()  # Поиск фильма по ключевому слову
            elif choice == '2':
                search_movie_by_genre_and_year()  # Поиск фильма по жанру и/или году
            elif choice == '3':
                display_popular_queries()  # Реализация вывода наиболее популярных запросов
            elif choice == '4':
                print("Выход из приложения...")
                break  # Выход из цикла и завершение программы
            else:
                print("Некорректный ввод. Пожалуйста, выберите действие из списка.")
    except Exception as e:
        print("Произошла ошибка:", e)

if __name__ == "__main__":
    main()  # Запуск основной функции приложения