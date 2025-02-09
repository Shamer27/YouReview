import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():

    # Connect to the database and return the connection object
    db = sqlite3.connect(".database/reviewDB.db")
    db.row_factory = sqlite3.Row

    return db

def GetAllReviews():

    # Connect, query all guesses and then return the data
    db = GetDB()
    Games = db.execute("SELECT * FROM Games").fetchall()
    db.close()
    return Games







def RegisterUser(username, password):

    # Check if they gave us a username and password
    if username is None or password is None:
        return False

    # Attempt to add them to the database
    db = GetDB()
    hash = generate_password_hash(password)
    db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, hash,))
    db.commit()

    return True

def CheckLogin(username, password):

    db = GetDB()

    # Ask the database for a single user matching the provided name
    user = db.execute("SELECT * FROM Users WHERE username=?", (username,)).fetchone()

    # Do they exist?
    if user is not None:
        # OK they exist, is their password correct
        if check_password_hash(user['password'], password):
            # They got it right, return their details
            return user
    else:
        error = "User not found"
       
    # If we get here, the username or password failed.
    return None
def AddReview(user_id, title, review, date, game, score):
   
    # Check if any boxes were empty
    if date is None or game is None:
        return False
   
    # Get the DB and add the guess
    db = GetDB()
    db.execute("INSERT INTO Reviews(user_id, date, game, score, review, title) VALUES (?, ?, ?, ?, ?, ?)",
               (user_id, date, game, score, review, title))
    db.commit()

    return True

def viewReview(reviewId):
    db = GetDB()
    review = db.execute("SELECT * FROM Reviews WHERE id=?", (reviewId,)).fetchone()
    db.close()
    return review

def get_db_connection():
    conn = sqlite3.connect('.database/reviewDB.db')
    conn.row_factory = sqlite3.Row
    return conn

def RegisterUser(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the user already exists
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if user:
        conn.close()
        return False  # User already exists
    
    # Insert the new user into the database
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return True