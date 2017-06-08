from flask import Flask, render_template, redirect,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///addressbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class PERSON(db.Model):
   id=db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
   name=db.Column(db.String(50), nullable=False, default='')
   number=db.Column(db.String(50), nullable=False, default='')
   email=db.Column(db.String(50), nullable=False, default='')

   def __init__(self, name, number, email):
      self.name=name
      self.number=number
      self.email=email


@app.route("/")
def main():
	return render_template('main.html', ADDRESSBOOK=PERSON.query.all(), contact_count=PERSON.query.count())

@app.route("/new", methods=['GET', 'POST'])
def new():
	 if request.method == 'POST':
	 	if not request.form['name'] or not request.form['number'] or not request.form['email']:
	 		flash('Please enter all the fields', 'error')
	 	else:
	 		NEW=PERSON(request.form['name'],request.form['number'],request.form['email'])
	 		db.session.add(NEW)
	 		db.session.commit()
	 		return redirect("/")
	 return render_template('plus.html', contact_count=PERSON.query.count())

@app.route("/favorite")
def favorite():
	return render_template('favorite.html',contact_count=PERSON.query.count())

@app.route("/trash")
def delete():
	return render_template('trash.html',contact_count=PERSON.query.count())

@app.route("/recent")
def recent():
	return render_template('recent.html',contact_count=PERSON.query.count())	

if __name__ == "__main__" :
	db.create_all()
	app.run(debug=True)
