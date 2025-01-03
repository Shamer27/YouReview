from flask import Flask, render_template, request, session, redirect
import db

app = Flask(__name__)
app.secret_key = "gtg"

@app.route("/")
def Home():
    reviewData = db.GetAllReviews()
    return render_template("index.html", reviews=reviewData)

@app.route("/login", methods=["GET", "POST"])
def Login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def Register():

    # If they click the submit button, let's register
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Try and add them to the DB
        if db.RegisterUser(username, password):
            # Success! Let's go to the homepage
            return redirect("/")
        
    return render_template("register.html")

@app.route("/createReview", methods=["GET","POST"])
def createReview():

    # Did they click submit?
    if request.method == "POST":
        user_id = session['id']
        title = request.form['title']
        review = request.form['review']
        date = request.form['date']
        game = request.form['game']
        score = request.form['score']

        # Send the data to add our new guess to the db
        db.AddGuess(user_id, date, game, score)

    return render_template("createReview.html")

app.run(debug=True, port=5000)