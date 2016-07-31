from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
mail=Mail(app)

app.config.update(
   DEBUG=True,
   #EMAIL SETTINGS
   MAIL_SERVER='smtp.gmail.com',
   MAIL_PORT=465,
   MAIL_USE_SSL=True,
   MAIL_USERNAME = 'harjot.kaur.panag@gmail.com',
   MAIL_PASSWORD = 'SOKHAJEHA'
   )

mail = Mail(app)

class register(db.Model):
   id = db.Column('register_id', db.Integer, primary_key = True)
   first = db.Column(db.String(100))
   email = db.Column(db.String(200), unique=True)

def __init__(self,first,email):
   self.first=first
   self.email=email

class post(db.Model):
   id = db.Column('post_id', db.Integer, primary_key = True)
   fullname = db.Column(db.String(20))
   email  = db.Column(db.String(20))
   phoneno = db.Column(db.String(20))
   itemname= db.Column(db.String(20))
   pickuptime = db.Column(db.String(20))
   address = db.Column(db.String(20))
   expire = db.Column(db.String(20))
   description = db.Column(db.String(500))

def __init__(self,fullname,email,phoneno,itemname,pickuptime,address,expire,description):
   self.fullname=fullname
   self.email=email
   self.phoneno=phoneno
   self.itemname=itemname
   self.pickuptime=pickuptime
   self.address=address
   self.expire=expire
   self.description=description

class donation(db.Model):
   id = db.Column('donation_id', db.Integer, primary_key = True)
   firstname = db.Column(db.String(20))
   lastname  = db.Column(db.String(20))
   demail= db.Column(db.String(20))
   dphoneno = db.Column(db.String(20))
   daddress = db.Column(db.String(20))
   cardno = db.Column(db.String(20), unique=True)
   amount = db.Column(db.String(20))
   check = db.Column(db.String(50))

def __init__(self,firstname,lastname,demail,dphoneno,daddress,cardno,amount,check):
   self.firstname=firstname
   self.lastname=lastname
   self.demail=demail
   self.dphoneno=dphoneno
   self.daddress=daddress
   self.cardno=cardno
   self.amount=amount
   self.check=check


@app.route('/')
def all_main():
    return render_template('index.html')

@app.route('/show_all')
def show_all():
   return render_template('get.html', post=post.query.all())
@app.route('/about')
def about():
   return render_template('about.html')
# @app.route('/u')
# def u():
#    result=donation.query.all()
#    return render_template('show_all.html',result=result)

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['Name'] or not request.form['email'] :
         flash('Please enter all the fields', 'error')
      else:
         registers = register(first=request.form['Name'], email=request.form['email'])

         db.session.add(registers)
         db.session.commit()
         flash('Record was successfully added')
         # return redirect(url_for('all_main'))
   return render_template('register.html')

@app.route('/dny', methods = ['GET', 'POST'])
def dny():
   if request.method == 'POST':
      if not request.form['Fname'] or not request.form['Lname'] or not request.form['Email'] or not request.form['Telephone'] or not request.form['Address'] or not request.form['CardNumber'] or not request.form['Amount'] or not request.form['check']:
         flash('Please enter all the fields', 'error')
      else:
         donations = donation(firstname=request.form['Fname'], lastname=request.form['Lname'], demail=request.form['Email'], dphoneno=request.form['Telephone'], daddress=request.form['Address'], cardno=request.form['CardNumber'], amount=request.form['Amount'], check=request.form['check'])

         db.session.add(donations)
         db.session.commit()
         flash('Record was successfully added')
         # return redirect(url_for('all_main'))
   return render_template('donation.html')


@app.route('/postfood', methods = ['GET', 'POST'])
def postfood():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['email'] or not request.form['Phoneno'] or not request.form['itemname'] or not request.form['PickUpTime'] or not request.form['Address'] or not request.form['Expire'] or not request.form['comments']:
         flash('Please enter all the fields', 'error')
      else:
         posts = post(fullname=request.form['name'], email=request.form['email'],
            phoneno=request.form['Phoneno'], itemname=request.form['itemname'], pickuptime=request.form['PickUpTime'], address=request.form['Address'], expire=request.form['Expire'], description=request.form['comments'])
         users=register.query.all()
         emails = []
         for em in users:
            emails.append(em.email)
            msg = Message(
              'Hello',
             sender='harjot.kaur.panag@gmail.com',
             recipients=emails)
         msg.body = posts.address
         msg.body += posts.description
         mail.send(msg)

         db.session.add(posts)
         db.session.commit()
         flash('Record was successfully added')
         # return redirect(url_for('show_all'))
   return render_template('post.html')

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
