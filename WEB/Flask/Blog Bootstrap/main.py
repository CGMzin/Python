from flask import Flask, render_template, request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests, smtplib

app = Flask(__name__)
all_blogs = requests.get('https://api.npoint.io/3c540308a25f171fc745').json()
posts = [post for post in all_blogs]

my_email = "email" 
password = "password"

@app.route('/')
def start():
    return render_template('index.html', posts=all_blogs)

@app.route('/post/<blog_id>')
def get_post(blog_id):
    return render_template("post.html", post=posts[int(blog_id) - 1])

@app.route('/about')
def get_about():
    return render_template("about.html")

@app.route('/contact', methods=["POST", "GET"])
def get_contact():
    sent = False
    if request.method == 'POST':
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "New Message"
        msg.attach( MIMEText(f"Name: {request.form['name']} \nEmail: {request.form['email']} \nPhone: {request.form['phone']} \nMessage: {request.form['message']}", "plain", "utf-8" ) )
        msg = msg.as_string().encode('ascii')
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=msg)
        sent = True
    else:
        sent = False
    return render_template("contact.html", sent=sent)


if __name__ == "__main__":
    app.run()