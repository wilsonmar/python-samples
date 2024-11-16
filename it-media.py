
""" it-media.py at https://github.com/wilsonmar/python-samples/blob/main/it-media.py

STATUS: WORKING 
git commit -m "v001 new :it-media.py"

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

def display_menu():
    print("\n==== IT Movie Database ====")
    print("v = View all movies")
    print("a = Add a new movie")
    print("s = Search for a movie")
    print("d = Delete a movie")
    print("r = Rate a movie")
    print("x = Exit")


def view_movies(movies):
    if not movies:
        print("No movies in the database.")
    else:
        print("\n==== IT Movie List ====")
        for i, movie in enumerate(movies, 1):
            print(f"{i}. {movie['title']} ({movie['year']}) - Rating: {movie['rating']}/10")
            print(f"   Description: {movie['description']}")


def search_movie(movies):
    print("\nSearch options:")
    print("1. Search by title or description")
    print("2. Search by minimum rating")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        search_term = input("Enter a search term: ").lower()
        results = [movie for movie in movies if search_term in movie['title'].lower() or search_term in movie['description'].lower()]
    elif choice == '2':
        while True:
            try:
                min_rating = float(input("Enter minimum rating (0-10): "))
                if 0 <= min_rating <= 10:
                    break
                else:
                    print("Rating must be between 0 and 10.")
            except ValueError:
                print("Please enter a valid number.")
        results = [movie for movie in movies if movie['rating'] >= min_rating]
    else:
        print("Invalid choice.")
        return

    if results:
        print("\n==== Search Results ====")
        for i, movie in enumerate(results, 1):
            print(f"{i}. {movie['title']} ({movie['year']}) - Rating: {movie['rating']}/10")
            print(f"   Description: {movie['description']}")
    else:
        print("No movies found matching your search criteria.")


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


def main():
    movies = [
        {"title": "The Social Network", "year": "2010", "description": "The founding of Facebook", "rating": 7.7},
        {"title": "Hackers", "year": "1995", "description": "Young hackers vs corporate extortion", "rating": 6.2},
        {"title": "The Imitation Game", "year": "2014", "description": "Alan Turing breaks the Enigma code", "rating": 8.0}
    ]

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == 'v':
            view_movies(movies)
        elif choice == 'a':
            add_movie(movies)
        elif choice == 's':
            search_movie(movies)
        elif choice == 'd':
            delete_movie(movies)
        elif choice == 'r':
            rate_movie(movies)
        elif choice == 'x':
            print("Thank you for using the IT Movie Database. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()


# TODO: List by ranking for where it's available to be seen (YouTube, Prime, NetFlix, DVD, Local Library, etc.), sorted by public ranking.
# TODO: List by title to look to buy the DVD (eBay, thrift stores, Amazon, etc.)
# TODO: GUI to select movies from among
# TODO: Load media to database from a CSV file.

