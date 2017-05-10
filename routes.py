import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from flask_mail import Mail, Message
from flask_errormail import mail_on_500
from searchForm import SearchForm
from lib.db_helper.dbHelper import DBHelper
from lib.config.initConfig import InitConfig
from facilitateProcess import FacilitateProcess

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_templates')

ADMINISTRATORS = [
    InitConfig.carbonGlue_mail,
]

app = Flask(__name__, template_folder = tmpl_dir)

app.secret_key = InitConfig.secret_key

app.config.update(
    DEBUG=False,
    # EMAIL SETTINGS
    MAIL_SERVER= InitConfig.googleServer,
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_DEFAULT_SENDER=(InitConfig.email),
    MAIL_MAX_EMAILS=10,
    MAIL_USERNAME= InitConfig.carbonGlue_mail,
    MAIL_PASSWORD= InitConfig.carbonGlue_pass
)

mail = Mail(app)

UPLOAD_FOLDER_DESTINATION = os.path.join(os.path.dirname(os.path.abspath(__file__)),"temp")


app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpeg', 'jpg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def uploadpage():
    return render_template('uploadpage.html')

@app.route('/upload', methods=['POST'])
def upload_document():

  #get the student id from the html
    studentID = request.form['text']
    newpath = '%s/%s' % (UPLOAD_FOLDER_DESTINATION, studentID)
    if not os.path.exists(newpath):
         os.makedirs(newpath)

    app.config['UPLOAD_FOLDER'] = '%s/'% (newpath)

        # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Save file in the designated uploads folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], InitConfig.transcriptName))
        isSaved = True
        # Redirect the user to the uploaded_file route, which will basicaly show on the browser the uploaded file
        #return redirect(url_for('uploaded_file',filename=filename))

    email = request.form['email'].strip()
    subject = 'Hello'
    message = 'Congratulations your transcript has been saved with us safely!!'
    msg = Message( 
        subject=subject,
        recipients=[email],
        html=message
    )

    mail.send(msg)
    return render_template('uploadpage.html'), FacilitateProcess.upload(FacilitateProcess(), studentID)


@app.errorhandler(404)
def pageNotFound(error):
    return "page not found"

@app.route("/search", methods=["GET", "POST"])
def search():
    """ Handles GET and POST on search form"""
    form = SearchForm()
    if request.method == "POST":
        if form.validate() is False:
            return render_template("/search.html", form=form) 
        else:
            query = {InitConfig.studentID:str(form.studentId.data)}
            subject_code = str(form.subjectCode.data)
            grade_point = float(form.gradePoint.data)
            document = DBHelper.findInDB(DBHelper(), query)
            if document is None:
                return "No data for this student exists"
            else:
                keys = document.keys()
                for key in keys:
                    if InitConfig.semester in key:
                        for subject in document[key][InitConfig.subjects]:
                            if subject_code == subject[InitConfig.code] and subject[InitConfig.grade_point] >= grade_point:
                                return "Student has cleared this Prerequisit"
                            else:
                                return "Student has failed to clear this Prerequisit"

    elif request.method == "GET":
        return render_template("/search.html", form=form)

    

if __name__ == "__main__":
    app.run(debug=True)
