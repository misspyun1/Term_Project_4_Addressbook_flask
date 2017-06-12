from flask import Flask, render_template, redirect,request, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///addressbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = "random string"

db=SQLAlchemy(app)

class PERSON(db.Model):
   id=db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
   name=db.Column(db.String(50), nullable=False, default='')
   number=db.Column(db.String(50), nullable=False, default='')
   email=db.Column(db.String(50), nullable=False, default='')
   favorite=db.Column(db.String(10), default="♡")
   deleted=db.Column(db.Boolean, default=False)

   def __init__(self, name, number, email):
      self.name=name
      self.number=number
      self.email=email
      self.favorite="♡"
      self.deleted=False

@app.route("/")
def main():
	return render_template('main.html', ADDRESSBOOK=PERSON.query.filter_by(deleted=False).order_by("name").all(), contact_count=PERSON.query.filter_by(deleted=False).count(),trashcount=PERSON.query.filter_by(deleted=True).count())

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

@app.route("/favorite")
def show_favorite():
	return render_template('favorite.html',contact_count=PERSON.query.filter_by(deleted=False).count(),FAVORITE=PERSON.query.filter_by(favorite='♥').order_by("name"),trashcount=PERSON.query.filter_by(deleted=True).count())

@app.route("/abdelete/<name>")
def abdelete(name):
	abdeleted=PERSON.query.filter_by(name=name)
	abdeleted.delete()
	db.session.commit()
	return redirect("/")

@app.route("/trash")
def trash():
	return render_template('trash.html',contact_count=PERSON.query.filter_by(deleted=False).count(),trash=PERSON.query.filter_by(deleted=True),trashcount=PERSON.query.filter_by(deleted=True).count())

@app.route("/restore/<id>")
def restore(id):
	deleted=PERSON.query.get(id)
	deleted.deleted=False
	db.session.commit()
	return redirect("/")

@app.route("/delete/<id>")
def delete(id):
	deleted=PERSON.query.get(id)
	if deleted.deleted==True:
		deleted.deleted=False
	else :
		deleted.deleted=True
	db.session.commit()
	return redirect("/")

@app.route("/favorite/<id>")
def favorite(id):
	favorite=PERSON.query.get(id)
	if favorite.favorite=="♥":
		favorite.favorite="♡"
	else :
		favorite.favorite="♥"
	db.session.commit()
	return redirect("/")


@app.route("/search", methods=['POST'])
def search():
	string=request.form['string']
	return render_template('search.html', namesearch=PERSON.query.filter_by(name=string).order_by("name").all(),
	numbersearch=PERSON.query.filter_by(number=string).order_by("name").all(),contact_count=PERSON.query.filter_by(deleted=False).count(),trashcount=PERSON.query.filter_by(deleted=True).count())

@app.route("/search/favorite", methods=['POST'])
def search_favorite():
	string=request.form['string']
	return render_template('search.html', namesearch=PERSON.query.filter_by(name=string, favorite=True).order_by("name").all(),
	numbersearch=PERSON.query.filter_by(number=string, favorite=True).order_by("name").all(),contact_count=PERSON.query.filter_by(deleted=False).count(),trashcount=PERSON.query.filter_by(deleted=True).count())


@app.route("/edit/<id>", methods=['POST'])
def edit(id):
   edited=PERSON.query.get(id)
   edited.name=request.form['name']
   edited.number=request.form['number']
   edited.email=request.form['email']
   db.session.commit()
   return redirect("/")

@app.route("/recent")
def recent():
	return render_template('recent.html',contact_count=PERSON.query.filter_by(deleted=False).count(),trashcount=PERSON.query.filter_by(deleted=True).count())

@app.route("/recent/<id>")
def recentdetail(id):
	RECENT=PERSON.query.get(id)
	return render_template('recent.html',contact_count=PERSON.query.filter_by(deleted=False).count(),trashcount=PERSON.query.filter_by(deleted=True).count(),
		recentname=RECENT.name, recentnum=RECENT.number, recentemail=RECENT.email)


if __name__ == "__main__" :
	db.create_all()
	app.run(debug=True)
