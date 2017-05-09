from flask import Flask, render_template, request
from searchForm import SearchForm
from lib.db_helper.dbHelper import DBHelper
from lib.config.initConfig import InitConfig 
app = Flask(__name__)


app.secret_key = InitConfig.secret_key

@app.route("/search", methods=[InitConfig.get_string, InitConfig.post_string])
def search():
    """ Handles GET and POST on search form"""
    form = SearchForm()
    if request.method == InitConfig.post_string:
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

    elif request.method == InitConfig.get_string:
        return render_template("/search.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
