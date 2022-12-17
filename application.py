from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
import os
from form import SubmitForm
from flask_bootstrap import Bootstrap
import boto3
from botocore.exceptions import ClientError
from flaskext.mysql import MySQL


#region_name = "us-east-1"

# Create a Secrets Manager client
#session = boto3.session.Session()
#boto3.setup_default_session(profile_name='iamadmin-production')
#client = boto3.client(service_name='secretsmanager')

#secret_name = "conventions"

#try:
#    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
#except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
 #   raise e

    # Decrypts secret using the associated KMS key.
#secret = get_secret_value_response['SecretString']


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'jCOo4PAnmU6A0j2lpKeI-A'

db_endpoint = open("/home/ec2-user/dbserver.endpoint", 'r', encoding='UTF-8')
#db_endpoint="database-1.cluster-cax8xbchtiwa.us-east-1.rds.amazonaws.com"
# Configure mysql database
app.config['MYSQL_DATABASE_HOST'] = db_endpoint.readline().strip()
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = '123abc79'
app.config['MYSQL_DATABASE_DB'] = 'convention'
app.config['MYSQL_DATABASE_PORT'] = 3306
#db_endpoint.close()
#
mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()
#print(connection)

def init_convention_db():
    drop_table = 'DROP TABLE IF EXISTS convention.convention;'
    convention_table = """
    CREATE TABLE convention(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    data = """
    INSERT INTO convention.convention (name, email)
    VALUES
        ("Venkat", "vramshesh@gmail.com");

    """
    cursor.execute(drop_table)
    cursor.execute(convention_table)
    cursor.execute(data)

# Write a function named `insert_person` which inserts person into the phonebook table in the db,
# and returns text info about result of the operation
def insert_person(name, email):
    query = f"""
    SELECT * FROM convention WHERE name like '{name.strip().lower()}';
    """
    cursor.execute(query)
    row = cursor.fetchone()
    if row is not None:
        return f'Person with name {row[1].title()} already exists.'

    insert = f"""
    INSERT INTO convention (name, email)
    VALUES ('{name.strip().lower()}', '{email}');
    """
    cursor.execute(insert)
    result = cursor.fetchall()
    return f'Person {name.strip().title()} added to convention successfully'


@app.route('/',methods=["GET","POST"])
def home():
    form = SubmitForm()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        result = insert_person(name, email)
    return render_template('index.html',form=form)


if __name__=="__main__":
    init_convention_db()
    #application.run(debug=True)
    app.run(host='0.0.0.0', port=80)


