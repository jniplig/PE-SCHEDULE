from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite database
db = SQLAlchemy(app)

class ScheduleEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_sorted = db.Column(db.String(10), nullable=False)
    day = db.Column(db.String(10), nullable=False)
    secondary_period = db.Column(db.String(10), nullable=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    year_group = db.Column(db.String(10), nullable=False)
    division = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f"<ScheduleEntry {self.class_name} - {self.day} - Period {self.secondary_period}>"

@app.route('/')
def index():
    return "Hello, this is the PE Schedule System!"

if __name__ == '__main__':
    app.run(debug=True)
db.create_all()