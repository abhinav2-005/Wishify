from flask import *
from database_connection import establish_connection

app = Flask(__name__)
app.secret_key = "niggasorus"
session = {
    'userid' :0,
    'user_name':0
}
@app.route("/", methods=["GET", "POST"])
def rendering_singnup_page():
    global session
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if name and email and password == confirm_password:
            conn = establish_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchall()

            if existing_user:
                flash("Email Already Registered!", "error")
                return redirect(url_for('rendering_login_page'))

            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            values = (name, email, password)
            cursor.execute(query, values)
            conn.commit()

            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_data = cursor.fetchone()
            session['userid'] = user_data[0]
            session['user_name'] = user_data[1]

            cursor.close()
            conn.close()

            return redirect(url_for("home_page"))
        else:
            return render_template("sign_up_page.html", error="Passwords do not match!")

    return render_template("sign_up_page.html")


@app.route("/login", methods=["GET", "POST"])
def rendering_login_page():
    global session
    if request.method == "POST":
        email = request.form.get("check_email")
        password = request.form.get('check_password')

        conn = establish_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()

        cursor.close()
        conn.close()

        if user_data and user_data[3] == password:
            session['userid'] = user_data[0]
            session['user_name'] = user_data[1]
            return redirect(url_for('home_page'))
        else:
            flash("Email and password don't match", "error")
            return redirect(url_for('rendering_login_page'))

    return render_template("login_page.html")


@app.route("/home_page", methods=["GET"])
def home_page():
    global session
    user_id = session.get('userid')
    user_name = session.get('user_name')
    if not user_id:
        return redirect(url_for('rendering_login_page'))

    conn = establish_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, recipient_name, wish_type, wish_date,recipient_email FROM wishes WHERE user_id = %s", (user_id,))
    wishes = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("home.html", wishes=wishes,user_name = user_name)


@app.route("/add_item", methods=["GET", "POST"])
def adding_item():
    global session
    if request.method == "POST":
        name = request.form.get('name')
        date = request.form.get('date')
        wish_type = request.form.get('wish_type')
        email = request.form.get('Email')
        user_id = session.get('userid')

        if name and date and wish_type and user_id and email:
            conn = establish_connection()
            cursor = conn.cursor()

            query = "INSERT INTO wishes (user_id, recipient_name, wish_type, wish_date,recipient_email) VALUES (%s, %s, %s, %s,%s)"
            values = (user_id, name, wish_type, date,email)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('home_page'))

    return render_template("add_item.html")

@app.route("/delete_wish/<int:wish_id>",methods = ["GET","POST"])
def handling_delete(wish_id):
    global session
    user_id = session.get('userid')
   
    conn = establish_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wishes WHERE id = %s AND user_id = %s", (wish_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Wish deleted successfully.")
    return redirect(url_for("home_page"))

if __name__ == "__main__":
    app.run(debug=True)
