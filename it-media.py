
""" it-media.py at https://github.com/wilsonmar/python-samples/blob/main/it-media.py

STATUS: WORKING 
git commit -m "v003 + list by title :it-media.py"

This program maintains a database of movies, YouTube videos, articles, etc. about 
IT (Information Technology), (not just sci-fi) related to
cyber security, software development, and the internet.
Much like https://alfilatov.com/awesome-IT-films/#/build/movies?id=disconnect

Content shown here contain links to YouTube, Reddit, 
imdb.com (Internet movie database), and
the movies API.

The program starts with a pre-populated list of three IT-related movies and uses a menu-driven interface to interact with the user. It employs functions to organize the code and improve readability15.
To run this program, simply copy the code into a Python file (e.g., it_movie_database.py) and execute it. 
You'll be presented with a menu where you can choose various options to manage the IT movie database5.
This program provides a basic framework that you can expand upon. For example, you could add features like saving the movie list to a file, sorting movies by different criteria, or implementing a rating system for the movies56.

Based on https://www.perplexity.ai/search/write-a-python-program-to-list-GqIwg5tYT.GxfslPtEcl9w
"""

class bcolors:  # ANSI escape sequences:
    BOLD = '\033[1m'       # Begin bold text
    UNDERLINE = '\033[4m'  # Begin underlined text

    HEADING = '\033[37m'   # [37 white
    FAIL = '\033[91m'      # [91 red
    ERROR = '\033[91m'     # [91 red
    WARNING = '\033[93m'   # [93 yellow
    INFO      = '\033[92m'      # [92 green
    VERBOSE   = '\033[95m'   # [95 purple
    TRACE     = '\033[96m'     # [96 blue/green
                 # [94 blue (bad on black background)

    CVIOLET = '\033[35m'
    CBEIGE = '\033[36m'
    CWHITE = '\033[37m'
    DARK_GREY = '\033[100m'  # Grey background

    RESET = '\033[0m'   # switch back to default color

def display_menu():
    print("\n==== IT Movie Database ====")
    print("l = List by rating")
    print("y = List by year")
    print("t = List by title")
    print("s = Search for a movie")
    print("")
    print("r = Rate a movie")
    print("n = Add a new movie")
    print("d = Delete a movie")
    print("x = Exit")

def view_movies(movies, sorted_by_rating=False, sorted_by_year=False, sorted_by_title=False):
    if not movies:
        print("No movies in the database.")
    else:
        if sorted_by_rating:
            sorted_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)
            print("\n==== IT Movie List (Sorted by Rating) ====")
        elif sorted_by_year:
            sorted_movies = sorted(movies, key=lambda x: x['year'], reverse=True)
            print("\n==== IT Movie List (Sorted by Year) ====")
        elif sorted_by_title:
            sorted_movies = sorted(movies, key=lambda x: x['title'], reverse=False)
            print("\n==== IT Movie List (Sorted by Title) ====")
        else:
            sorted_movies = movies
            print("\n==== IT Movie List ====")

        for i, movie in enumerate(sorted_movies, 1):
            print(f"{i}. {movie['rating']}/10 {bcolors.BOLD}{bcolors.WARNING}{movie['title']} ({movie['year']}{bcolors.RESET})")
            print(f"      {bcolors.CBEIGE}{movie['description']}{bcolors.RESET}")

def add_movie(movies):
    title = input("Enter movie title: ")
    year = input("Enter release year: ")
    description = input("*** Enter a brief description: ")
    while True:
        try:
            rating = float(input("*** Enter rating (0-10): "))
            if 0 <= rating <= 10:
                break
            else:
                print("*** Rating must be between 0 and 10.")

        except ValueError:
            movies.append({
            "title": title,
            "year": year,
            "description": description,
            "rating": rating
        })
    print(f"\n'{title}' has been added to the database.")

def search_movie(movies):
    try:
        print("\nSearch options:")
        print("1. Search by title or description")
        print("2. Search by minimum rating")
        choice = input("Enter your choice (1 or 2): ")
        # control+C on macOS or Ctrl+C on Windows.
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"*** ERROR {e}")
        return None

    if choice == '1':
        search_term = input("*** Enter a search term: ").lower()
        results = [movie for movie in movies if search_term in movie['title'].lower() or search_term in movie['description'].lower()]
    elif choice == '2':
        while True:
            try:
                min_rating = float(input("*** Enter minimum rating (0-10): "))
                if 0 <= min_rating <= 10:
                    break
                else:
                    print("*** Rating must be between 0 and 10.")
            except ValueError:
                print("*** Please enter a valid number.")
        results = [movie for movie in movies if movie['rating'] >= min_rating]
    else:
        print("Invalid choice.")
        return

    if results:
        print("\n==== Search Results ====")
        for i, movie in enumerate(results, 1):
            print(f"{i}. {movie['rating']}/10 {bcolors.BOLD}{bcolors.WARNING}{movie['title']} ({movie['year']}{bcolors.RESET})")
            print(f"      {bcolors.CBEIGE}{movie['description']}{bcolors.RESET}")
    else:
        print("*** No movies found matching your search criteria.")

def delete_movie(movies):
    view_movies(movies)
    if movies:
        try:
            index = int(input("Enter the number of the movie to delete: ")) - 1
            if 0 <= index < len(movies):
                deleted_movie = movies.pop(index)
                print(f"\n'{deleted_movie['title']}' has been deleted from the database.")
            else:
                print("Invalid movie number.")
        except ValueError:
            print("Please enter a valid number.")

def rate_movie(movies):
    view_movies(movies)
    if movies:
        try:
            index = int(input("Enter the number of the movie to rate: ")) - 1
            if 0 <= index < len(movies):
                while True:
                    try:
                        new_rating = float(input("Enter new rating (0-10): "))
                        if 0 <= new_rating <= 10:
                            movies[index]['rating'] = new_rating
                            print(f"\nRating for '{movies[index]['title']}' has been updated to {new_rating}/10.")
                            break
                        else:
                            print("Rating must be between 0 and 10.")
                    except ValueError:
                        print("Please enter a valid number.")
            else:
                print("Invalid movie number.")
        except ValueError:
            print("Please enter a valid number.")

def sort_movies_by_rating(movies):
    view_movies(movies, sorted_by_rating=True)

def sort_movies_by_year(movies):
    view_movies(movies, sorted_by_year=True)

def sort_movies_by_title(movies):
    view_movies(movies, sorted_by_title=True)

def main():
    movies = [
        {"title": "The Social Network", "year": "2010", "description": "The founding of Facebook", "rating": 7.7},
        {"title": "Hackers", "year": "1995", "description": "Young hackers vs corporate extortion", "rating": 6.2},
        {"title": "The Imitation Game", "year": "2014", "description": "Alan Turing breaks the Enigma code", "rating": 8.0}
    ]

    try:
        while True:
            display_menu()
            choice = input("Enter your choice: ")

            if choice == 'x':
                print("Thank you for using the IT Movie Database. Goodbye!")
                break
            elif choice == 'l':
                sort_movies_by_rating(movies)
            elif choice == 'y':
                sort_movies_by_year(movies)
            elif choice == 't':
                sort_movies_by_title(movies)
            elif choice == 'y':
                view_movies(movies)
            elif choice == 's':
                search_movie(movies)

            elif choice == 'n':
                add_movie(movies)
            elif choice == 'd':
                delete_movie(movies)
            elif choice == 'r':
                rate_movie(movies)
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"*** ERROR {e}")
        return None



if __name__ == "__main__":
    main()


# TODO: Add a field to track when it was last viewed.
# TODO: List by ranking for where it's available to be seen (YouTube, Prime, NetFlix, DVD, Local Library, etc.), sorted by public ranking.
# TODO: List by title to look to buy the DVD (eBay, thrift stores, Amazon, etc.)
# TODO: GUI to select movies from among
# TODO: Load media to database from a CSV file.
# TODO: Make API calls to movies (https://rapidapi.com/blog/movie-api/) themoviedb.org, MoviesDatabase API (from IMDb.com), Streaming Availability API,MoviesMiniDatabase API
