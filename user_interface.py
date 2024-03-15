from database_movies import read_from_movies
from database_request import write_to_request, read_from_request
import json
import re


def print_top_10(found_movies, keyword):
    # Сортировка найденных фильмов по рейтингу
    found_movies.sort(key=lambda x: x[11], reverse=True)
    # Вывод топ-10 найденных фильмов
    for idx, movie in enumerate(found_movies[:10], start=1):
        # Преобразование списка жанров в строку с кавычками вокруг каждого жанра
        genres_str = ', '.join([f'"{genre}"' for genre in movie[2]])
        # Преобразование данных из JSON в списки
        directors = json.loads(movie[8])
        cast = json.loads(movie[4])
        languages = json.loads(movie[7])
        
        # Подсветка ключевого слова в тексте с помощью регулярного выражения
        title = movie[6]
        plot = movie[1]
        awards = movie[9]
        
        # Подсветка ключевого слова в заголовке, сюжете, наградах и остальных столбцах
        title = re.sub(re.escape(keyword), lambda match: f"**{match.group().upper()}**", title, flags=re.IGNORECASE)
        plot = re.sub(re.escape(keyword), lambda match: f"**{match.group().upper()}**", plot, flags=re.IGNORECASE)
        awards = re.sub(re.escape(keyword), lambda match: f"**{match.group().upper()}**", awards, flags=re.IGNORECASE)
        directors = [re.sub(re.escape(keyword), lambda match: f"**{match.group().upper()}**", director, flags=re.IGNORECASE) for director in directors]
        cast = [re.sub(re.escape(keyword), lambda match: f"**{match.group().upper()}**", actor, flags=re.IGNORECASE) for actor in cast]
        languages = [re.sub(re.escape(keyword), lambda match: f"**{match.group().upper()}**", language, flags=re.IGNORECASE) for language in languages]
        
        # Вывод информации о фильме
        print(f"{idx}. Title: {title} (Year: {movie[10]}, Genres: {genres_str}, Runtime: {movie[3]}, Rating: {movie[11]})")
        print(f"    Plot: {plot}")
        print(f"    Directors: {', '.join([director.strip('\"') for director in directors])}, "
              f"Cast: {', '.join([actor.strip('\"') for actor in cast])}, "
              f"Languages: {', '.join([language.strip('\"') for language in languages])}")


def search_movie_by_keyword():
    # Поиск фильмов по ключевому слову
    keyword = input("Введите ключевое слово для поиска фильма: ").strip().lower()
    write_to_request(keyword)  # Записываем ключевое слово в базу данных dam29_movies_Kate
    found_movies = []  # Список для хранения найденных фильмов
    # Проверяем каждый столбец каждого фильма на наличие ключевого слова
    for movie in read_from_movies():
        for column in movie:
            if isinstance(column, str) and keyword.lower() in column.lower():
                found_movies.append(movie)
                break  # Прерываем цикл, если фильм уже был добавлен
    if found_movies:
        print_top_10(found_movies,keyword )
    else:
        print("Фильмы с таким ключевым словом не найдены.")
#_____________________________________________________________ 
def get_available_genres():
    # Получаем данные о фильмах из базы данных movies
    movies_data = read_from_movies()
    
    # Создаем множество для хранения всех жанров
    all_genres = set()
    
    # Проходим по каждому фильму и добавляем его жанры в множество
    for movie in movies_data:
        all_genres.update(movie[2])
    
    # Преобразуем множество в отсортированный список
    sorted_genres = sorted(all_genres)
    
    return sorted_genres

def get_available_years():
    try:
        # Получение списка всех доступных годов
        movies_data = read_from_movies()
        all_years = sorted(set(movie[10] for movie in movies_data))  # Годы из столбца индекса 10
        return ' '.join(str(year) for year in all_years)
    except Exception as e:
        print("Произошла ошибка при получении доступных годов:", e)
        return None

def search_movie_by_genre_and_year():
    # Поиск фильмов по жанру и/или году
    print("Доступные жанры:")
    genres_string = ' '.join(get_available_genres())
    print(genres_string)
    
    print()  # Добавляем пустую строку для перехода на новую строку
    
    genre_choice = input("Выберите жанр фильма (или нажмите Enter для пропуска): ")
    
    print("Доступные годы:")
    print(''.join(get_available_years()))
        
    year = input("Введите год выпуска фильма (или нажмите Enter для пропуска): ")
    movies_data = read_from_movies()  
    
    found_movies = []
    
    # Проверка условий и выполнение соответствующих действий
    if genre_choice and not year:
        # Поиск по жанру
        for movie in movies_data:
            if genre_choice in movie[2]:
                found_movies.append(movie)
        if found_movies:       
            print_top_10(found_movies, genre_choice)
        else:
            print("Фильмов по этому жанру не найдено.")
        # Запись ключевого слова в базу данных
        write_to_request(genre_choice.strip().lower())
        
    elif not genre_choice and year:
    # Поиск по году
        for movie in movies_data:
            if str(year) == str(movie[10]):  # Ensure year comparison is correct
                found_movies.append(movie)
        if found_movies:
            print_top_10(found_movies, year)  # Pass year as the keyword
        else:
            print("Фильмов за указанный год не найдено.")
        # Запись года в базу данных
        write_to_request(str(year))  # Ensure year is converted to string
    
        
    elif genre_choice and year:
        # Поиск по жанру и году
        for movie in movies_data:
            if genre_choice in movie[2] and str(year) == str(movie[10]):
                found_movies.append(movie)
        if found_movies:
            print_top_10(found_movies,year)
        else:
            print("Фильмов за указанный жанр и год не найдено.")
        # Запись жанра и года в базу данных
        keyword1 = f"{genre_choice} {year}"
        write_to_request(keyword1.strip().lower())
#____________________________________

def display_popular_queries():
    try:
        num_queries = input("Введите количество популярных запросов для вывода: ")
        try:
            num_queries = int(num_queries)
            if num_queries <= 0:
                print("Количество запросов должно быть больше нуля.")
                return
        except ValueError:
            print("Пожалуйста, введите целое положительное число.")
            return

        # Получение данных о популярных запросах
        request_data = read_from_request()
        
        if request_data:
            # Создание словаря для подсчета количества запросов
            query_counts = {}
            for row in request_data:
                keyword = row[1]
                if keyword in query_counts:
                    query_counts[keyword] += 1
                else:
                    query_counts[keyword] = 1
            
            # Сортировка словаря по убыванию значения
            sorted_queries = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Вывод популярных запросов
            print("Популярные запросы:")
            for idx, (keyword, count) in enumerate(sorted_queries[:num_queries], start=1):
                print(f"Запрос: {keyword}, Количество запросов: {count}")
        else:
            print("Нет данных о популярных запросах")
            
    except Exception as e:
        print("Произошла ошибка при выводе популярных запросов:", e)