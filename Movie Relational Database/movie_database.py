import sqlite3

# Connect to the SQL Relational Database
connection = sqlite3.connect('movie_record.db')
cursor = connection.cursor()

# Creates tables (if it does not already exist)
cursor.execute("CREATE TABLE IF NOT EXISTS movie (movie_id INT NOT NULL PRIMARY KEY, movie_name TEXT, release_year INT, age_rating TEXT, movie_length INT)")
cursor.execute("CREATE TABLE IF NOT EXISTS genre (genre_id INT NOT NULL PRIMARY KEY, genre_name TEXT, movie_id INT NOT NULL, FOREIGN KEY (movie_id)REFERENCES movie (movie_id) )")
# Joins two tables together
# cursor.execute("SELECT movie.movie_id, movie.movie_name, genre.name FROM movie.movie INNER JOIN genre ON genre.movie_id = movie.movie_id;")



def get_name(cursor):
    cursor.execute("SELECT movie_name FROM movie")
    results = cursor.fetchall()
    if len(results) == 0:
        print("No names in database")
        return None
    for i in range(len(results)):
        print(f"{i+1} - {results[i][0]}")
    choice = 0
    while choice < 1 or choice > len(results):
        choice = int(input("Movie ID: "))
    return results[choice - 1][0]


choice = None
while choice != "8":
    print("1: Show Movie")
    print("2: Show Newer Movie")
    print("3: Add Movie")
    print("4: Update Movie Info")
    print("5: Delete Movie")
    print("6: Add Genre")
    print("7: Show Genres")
    print("8: Exit")
    choice = input("> ")
    print()
    if choice == "1":
        # Display Movie List
        cursor.execute("SELECT * FROM movie ORDER BY movie_id ASC")
        print("{:>10}  {:>10}  {:>10}  {:>10}  {:>10}".format("Movie_ID", "Movie Name", "Release Year", "Rating", "Film Length"))
        for record in cursor.fetchall():
            print("{:>10}  {:>10}  {:>10}  {:>10}  {:>10}".format(record[0], record[1], record[2], record[3], record[4]))

    elif choice == "2":
        # Display Movie List
        cursor.execute("SELECT movie_name, release_year FROM movie WHERE release_year > 2018 ORDER BY release_year DESC")
        print("{:>10}  {:>10}".format("Movie_ID", "Release Year"))
        for record in cursor.fetchall():
            print("{:>10}  {:>10}".format(record[0], record[1]))
    elif choice == "3":
        # Add Movie
        # age1 = ('Pg')
        movie_id = input("ID: ")
        name = input("Movie Name: ")
        release_year = int(input("Release Year: "))
        rating = (input("Rating: "))
        length = int(input("Movie Length: "))
        values = (movie_id, name, release_year, rating, length)
        cursor.execute("INSERT INTO movie VALUES (?,?,?,?,?)", values)
        # if rating(input) != age1:
        #     print("Please write Pg, Pg-13, or R")
        connection.commit()

    elif choice == "4":
        # Update Movie Information
        name = input("Movie Name: ")
        release_year = int(input("Release Year: "))
        rating = int(input("Rating: "))
        length = int(input("Movie Length: "))
        values = (name, release_year, rating, length, name)
        cursor.execute("UPDATE movie SET movie_name = ?, release_year = ?, age_rating = ?, movie_length = ? WHERE movie_name = ?", values)
        if cursor.rowcount == 0:
            print("Movie doesn't exist.")
        connection.commit()

    elif choice == "5":
        # Delete Movie
        name = get_name(cursor)
        values = (name,)
        cursor.execute("DELETE FROM movie WHERE movie_name = ?", values)
        print("Movie has been deleted")
        connection.commit()

    #Add genre
    elif choice == "6":
        genre_id = input("G ID:")
        movie_id = input("ID:")
        gname = input("Genre: ")
        values = (genre_id, movie_id, gname)
        cursor.execute("INSERT INTO genre VALUES (?,?,?)", values)
        connection.commit()


    elif choice == "7":
    # Show Genre types of movies
        # cursor.execute("SELECT movie.movie FROM genre ORDER BY genre_name DESC")
        cursor.execute("SELECT movie.movie_id, movie.movie_name, genre.genre_name FROM movie INNER JOIN genre ON genre.movie_id = movie.movie_id;")
        print("{:>10}  {:>10}".format("Movie Name", "Genre"))
        for record in cursor.fetchall():
            print("{:>10}  {:>10}".format(record[0], record[1]))
    
    

# closes the database connection
connection.close()