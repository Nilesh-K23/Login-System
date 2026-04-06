from flask import Flask, render_template, request, redirect, session
from database import db, cursor
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash


app = Flask(__name__)
app.secret_key = "secretkey"

import time

@app.before_request
def session_timeout():
    if request.endpoint in ['login', 'logout', 'static']:
        return

    if "user" in session:
        current_time = time.time()

        if current_time - session.get("login_time", 0) > 60:
            session.clear()
            flash("Session expired! Please login again.", "warning")
            return redirect("/login")

        # reset timer if user is active
        session["login_time"] = current_time
        
# Create default admin
def create_admin():
    cursor.execute("SELECT * FROM users WHERE role='admin'")
    if not cursor.fetchone():
        password = generate_password_hash("admin1234")
        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            ("admin", "admin@gmail.com", password, "admin")
        )
        db.commit()

create_admin()

# Home
@app.route("/")
def home():
    return redirect("/login")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already exists", "error")
        else:
            password = generate_password_hash(request.form["password"])
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            db.commit()
            flash("Registration successful, please login", "success")
            return redirect("/login")
    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
         session["user"] = user[1]
         session["login_time"] = time.time()
        #  flash("Login successful", "success")
         return redirect("/dashboard")
        else:
         flash("Invalid username or password", "error")
    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        current_time = time.time()

        # 60 seconds = 1 minute
        if current_time - session.get("login_time", 0) > 60:
            session.pop("user", None)
            session.pop("login_time", None)
            flash("Session expired! Please login again.", "warning")
            return redirect("/login")

        return render_template("dashboard.html", user=session["user"])

    flash("Please login first", "warning")
    return redirect("/login")
    
    # if "user" not in session:
    #  flash("Please login first", "warning")
    # return redirect("/login")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully", "success")
    return redirect("/login")

# Change Password
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if "user" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    if request.method == "POST":
        old = request.form["old_password"]
        new = generate_password_hash(request.form["new_password"])

        cursor.execute("SELECT * FROM users WHERE username=%s", (session["user"],))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], old):
            cursor.execute(
                "UPDATE users SET password=%s WHERE username=%s",
                (new, session["user"])
            )
            db.commit()
            flash("Password updated successfully", "success")
            return redirect("/dashboard")

        else:
            flash("Old password is incorrect", "error")
            return redirect("/change_password")   # 🔥 MUST

    return render_template("change_password.html")


if __name__ == "__main__":
    app.run(debug=True)