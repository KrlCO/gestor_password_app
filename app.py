from flask import Flask, flash,render_template,request, send_file,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import csv
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SECRET_KEY"] = "this is secret"
db = SQLAlchemy(app)

#Model/Schema for data
class PasswordManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(520), nullable=False)
    site_url = db.Column(db.String(520), nullable=False)
    site_password = db.Column(db.String(520), nullable=False)

    def __repr__(self):
        return '<PasswordManager %r>' % self.email

""" with open("secret_key.txt", "rb") as f:
    key = f.read()

def encrypt_password(key,data):
    f = Fernet(key)
    encrypted_token = f.encrypt(str(data).encode())
    return encrypted_token """

#Routes
@app.route("/")
def index():
    passwordlist = PasswordManager.query.all()
    return render_template("index.html", passwordlist=passwordlist)


@app.route("/add", methods=["GET","POST"])
def add_details():#
    if request.method == "POST":
        email = request.form["email"]
        site_url = request.form["site_url"]
        site_password = request.form["site_password"]
        new_password_details = PasswordManager(email=email,
                                               site_url=site_url, site_password=site_password)
        db.session.add(new_password_details)
        db.session.commit()
        return redirect("/")


@app.route("/update/<int:id>", methods=["GET","POST"])
def update_details(id):
    updated_details = PasswordManager.query.get_or_404(id)
    if request.method == "POST":
        updated_details.email = request.form["email"]
        updated_details.site_url = request.form["site_url"]
        updated_details.site_password = request.form["site_password"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an error updating Password Details"

    return render_template("update.html",updated_details=updated_details)


@app.route("/delete/<int:id>")
def delete_details(id):
    new_details_to_delete = PasswordManager.query.get_or_404(id)
    try:
        db.session.delete(new_details_to_delete)
        db.commit()
        return redirect("/")
    except:
        return "There was an error deleting the details"


@app.route('/export')
def export_data():
    with open('dump.csv', 'w') as f:
        out = csv.writer(f)
        out.writerow(['id', 'email', 'site_url', 'site_password'])
        for item in PasswordManager.query.all():
            out.writerow([item.id, item.email, item.site_url, item.site_password])
        return send_file('dump.csv',
                         mimetype ='text/csv',
                         download_name = f"Export_Password_{timestr}.csv",
                         as_attachment =True)



if __name__ == '__main__':
    app.run(debug=True) #development & production set to False
