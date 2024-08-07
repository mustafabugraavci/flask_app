from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'


class UploadForm(FlaskForm):
    file = FileField('Upload Image', validators=[DataRequired()])
    submit = SubmitField('Analyze')


@app.route('/', methods=['GET', 'POST'])
def index():
    '''Index page fun'''
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('result', filename=filename))
    return render_template('index.html', form=form)


@app.route('/result/<filename>')
def result(filename):
    '''Result page fun'''
    return render_template('result.html', filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
