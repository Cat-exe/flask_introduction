from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Telling our app where our database is located. We are using sqlite to keep things simple. (3 forward slashes is a relative path, 4 is an absolute path. We use 3 because we want it to reside in the present location)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)  # initialize our database with the settings from our app


# Create a model
class Todo(db.Model):
    # Set up some columns
    id = db.Column(db.Integer, primary_key=True)
    # 200 stands for 200 characters, nullable = False means this cannot be a blank space from the user
    content = db.Column(db.String(200), nullable=False)
    # Any time a to-do entry is created, the date created will be set to the time automatically
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Need a function that will return a string everytime we create a new element.
    def __repr__(self):
        # Everytime we make a new element, it will just return the task and the ID of that task that has been created
        return '<Task %r>' % self.id

# Create an index route so that we don't immediately 404 when we go to the browser.


@app.route('/', methods=['POST', 'GET'])
def index():  # Define function for ^that route.
    # If the request that is sent to this route is a POST, ...
    if request.method == 'POST':
        # Pass ID of input, that we want contents of (which is 'content')
        task_content = request.form['content']

        # Create a new task from the input.
        new_task = Todo(content=task_content)

        # Push it to our database
        try:
            db.session.add(new_task)
            db.session.commit()  # Commmit it to our database
            return redirect('/')  # Redirect it to our index page.

        except:  # If this fails..
            return "There was an issue adding your task."
    else:
        # This is going to look at all of the database contents in the order that they were created and return ALL of them
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id): #Define function for our delete route.
    task_to_delete = Todo.query.get_or_404(id) #Attempts to get task by ID (if it doesn't exist, it will 404)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task."

#Update route
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    #Create a variable representing the task
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task.'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)  # set debug to True so we can see errors on the webpage
