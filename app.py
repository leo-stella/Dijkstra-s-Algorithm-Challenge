from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = '.json'


@app.route('/upload')
def upload_file():
    return render_template('index.html')


@app.route('/uploader', methods=['POST'])
def uploader():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        file_pre = os.path.splitext(filename)[0]
        file_ext = os.path.splitext(filename)[1]
        if filename != '' and file_ext in app.config['UPLOAD_EXTENSIONS'] and file_pre == 'empire':
            os.remove("empire.json") if os.path.exists("empire.json") else None
            uploaded_file.save(filename)
            return render_template('index.html', message='JSON File Uploaded Successfully', success=True)
        else:
            return render_template('index.html',
                                   error_message='Please upload a JSON file format (File name must be "empire.json")')


@app.route('/result')
def get_result():
    import resources as rs
    capture_prob, mf_error, db_error, em_error = rs.get_data()
    if mf_error:
        return render_template('index.html',
                               error_message='There is something wrong with the millennium-falcon.json file')
    elif db_error:
        return render_template('index.html',
                               error_message='There is something wrong with the database')
    elif em_error:
        return render_template('index.html',
                               error_message='There is something wrong with the empire.json file')
    else:
        return render_template('result.html', capture_prob=capture_prob)


if __name__ == '__main__':
    app.run(debug=True)
