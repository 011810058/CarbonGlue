from flask import Flask, render_template, request
from searchForm import SearchForm
from lib.db_helper.dbHelper import DBHelper
app = Flask(__name__)


app.secret_key = "abhishek-jasmeet-parag-vinayak"

@app.route("/search", methods=["GET", "POST"])
def search():
	form = SearchForm()

	if request.method == "POST":
		print "From POST"
		if form.validate() == False:
			return render_template("/search.html", form=form)
		else:
			query = {"studentID":str(form.studentId.data)}
			subject_code = str(form.subjectCode.data)
			gradePoint = float(form.gradePoint.data)
			# if(form.gradePoint.data != ''):
			# 	query["Semester1.Subjects"]= {'$elemMatch':{'code':subject_code,'GP':{'$gte':float(form.gradePoint.data)}}}
			# else:
			# 	query["Semester1.Subjects"] = {'$elemMatch':{'code':subject_code}}
			print query
			document = DBHelper.findInDB(DBHelper(), query)
			if document is None :
				return "No data for this student exists"
			else:
				 keys = document.keys()
				 for key in keys:
					 if "Semester" in key:
						for subject in document[key]["Subjects"]:
							if subject_code == subject["code"] and gradePoint >= subject["GP"]:
								return "Student has cleared this Prerequisit"
							else:
								return "Student has failed to clear this Prerequisit"

			
			
			
	elif request.method == "GET":
	    return render_template("/search.html", form=form)

if __name__ == "__main__":
		app.run(debug=True)