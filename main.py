from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from datetime import datetime
from config import SECRET_KEY
import pandas as pd


app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)


## CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///humanResourcers.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




#Creating Tables
class HiredEmployees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    hire_datetime = db.Column(db.DateTime)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))


class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(250))


class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(250))


db.create_all()


#Creating form

class UploadForm(FlaskForm):
    csv_file = FileField('CSV File', validators=[DataRequired()])
    submit = SubmitField('Upload')



@app.route("/query")
def query():
    # Execute the query to get the number of employees hired for each job and department in 2021 divided by quarter
    button = request.args.get('button')
    if button == '1':

        query = text('''
        SELECT *
        FROM number_employees_job_department
        ''')

        # Execute the query using your database connection
        result = db.session.execute(query).fetchall()

        return render_template('query.html', result=result, query='query1')
    elif button == '2':

        query = text('''
        SELECT *
        FROM list_departments_with_more_employees_than_mean
        ''')

        result = db.session.execute(query).fetchall()

        return render_template('query.html', result=result, query='query2')
    else:
        return redirect(url_for('home'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        file = form.csv_file.data

        if file:
            # Check if the uploaded file is a CSV file
            filename = file.filename.lower()
            if not filename.endswith('.csv'):
                msg = f'Invalid file format. Please upload a CSV file. ({filename})'
                return render_template('error.html', msg=msg)

            # Read the CSV file using pandas
            df = pd.read_csv(file)

            # Validate batch size
            num_rows = df.shape[0]
            if num_rows < 1 or num_rows > 1000:
                msg = 'Invalid batch size. Batch size must be between 1 and 1000 rows.'
                return render_template('error.html', msg=msg)

            # Validate if the CSV file matches the table schema
            expected_headers = ['id', 'name', 'hire_datetime', 'department_id', 'job_id']
            if list(df.columns) != expected_headers:
                msg = 'Invalid CSV file. The file structure does not match the required schema.'
                return render_template('error.html', msg=msg)

            # Validate data types for each column
            expected_data_types = [int, str, datetime, int, int]
            for column, expected_data_type in zip(df.columns, expected_data_types):
                column_data_type = df[column].dtype
                if column_data_type != expected_data_type and column_data_type != object:
                    msg = f'Invalid data type in CSV file. Expected {expected_data_type.__name__} type for {column} column.'
                    return render_template('error.html', msg=msg)
                

            # Convert hire_datetime column to datetime object
            df['hire_datetime'] = pd.to_datetime(df['hire_datetime'])

            # Prepare data for insertion
            data = df.to_dict(orient='records')

            # Check uniqueness of id column
            existing_ids = db.session.query(HiredEmployees.id).all()
            existing_ids = [id for (id,) in existing_ids]
            new_ids = [row['id'] for row in data]
            duplicate_ids = set(new_ids).intersection(existing_ids)
            if duplicate_ids:
                msg = f'Duplicate id found in CSV file: {duplicate_ids}'
                return render_template('error.html', msg=msg)

            # Insert data into the database in batches
            batch_size = 100  # Adjust the batch size as needed
            batches = [data[i:i+batch_size] for i in range(0, num_rows, batch_size)]

            Session = sessionmaker(bind=db.engine)
            session = Session()

            try:
                for batch in batches:
                    session.execute(HiredEmployees.__table__.insert(), batch)

                session.commit()
            except Exception as e:
                session.rollback()
                msg = f'An error occurred while uploading data: {str(e)}'
                return render_template('error.html', msg=msg)
            finally:
                session.close()

            msg = 'Data uploaded successfully!'
            return render_template('error.html', msg=msg)


    return render_template('upload.html', form=form)




@app.route("/")
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)