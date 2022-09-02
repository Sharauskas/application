import base64
import json
from datetime import datetime

import boto3
import botocore
from cryptography.fernet import Fernet
from flask import Flask, redirect, render_template, url_for, request
from flask_httpauth import HTTPBasicAuth
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms_validators import AlphaNumeric

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
auth = HTTPBasicAuth()


client_s3 = boto3.client('s3')
client_sm = boto3.client('secretsmanager',
                         region_name='eu-central-1'
                         )

### VARIABLES ###
message = "Hello world!"
file = "logs.txt"
bucket = "cg-testas-prod"
secretmanager_id = 'cg-testas-secret-prod'


class NewPostForm(FlaskForm):
    title = StringField('', validators=[DataRequired(), Length(32, 32), AlphaNumeric()])
    save = SubmitField('Update')


@app.route('/')
def index():
    response = client_sm.get_secret_value(
        SecretId=secretmanager_id
    )
    database_secrets = json.loads(response['SecretString'])

    key = base64.urlsafe_b64encode(str.encode(database_secrets['Secret']))
    fernet = Fernet(key)
    encMsg = fernet.encrypt(message.encode())
    return f"{encMsg}"


@app.route('/secret', methods=['GET', 'POST'])
@auth.login_required
def get_response():
    form = NewPostForm()
    if form.validate_on_submit():
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip = request.environ['REMOTE_ADDR']
        else:
            ip = request.environ['HTTP_X_FORWARDED_FOR']

        user_agent = request.headers.get('User-Agent')

        response = client_sm.get_secret_value(
            SecretId=secretmanager_id
        )

        database_secrets = json.loads(response['SecretString'])

        try:
            client_s3.head_object(
                Bucket=bucket,
                Key=file,
            )
        except botocore.exceptions.ClientError as e:
            client_s3.put_object(
                Bucket=bucket,
                Key=file
            )

        client_s3.get_object(Bucket=bucket, Key=file)
        client_s3.download_file(bucket, file, file)

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

        opened = open(file, 'a')
        opened.write(dt_string + " " + ip + " " + user_agent + " " + database_secrets['Secret'] + "\n")
        opened.close()
        client_s3.upload_file(file, bucket, file)

        sec_str = '{"Secret": ' + f'"{request.form["title"]}"' + '}'

        response = client_sm.update_secret(
            SecretId=secretmanager_id,
            SecretString=sec_str
        )

        return redirect(url_for('index'))
    return render_template('submit.html', form=form)


@auth.verify_password
def authenticate(username, password):
    if username and password:
        if username == 'coingate' and password == 'thebest':
            return True
        else:
            return False
    return False


if __name__ == "__main__":
    app.run(debug=True)
