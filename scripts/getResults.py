from pdfToJSON import parseClassData
from getRating import getId
import pdfplumber

classData = pdfplumber.open("./dataCollector/data/classData.pdf")

data = parseClassData(classData)

jsonData = data[0]
teacherList = data[1]


with open("./dataCollector/results/results_no_rating.json", "w") as jsonFile:
    jsonFile.write(jsonData)

#teacher_id_json = getId(teacherList, "U2Nob29sLTEyMDUw")

#with open("./dataCollector/results/teacher_id.json", "w") as teacherIdFile:
#    teacherIdFile.write(teacher_id_json)

with open("./dataCollector/results/teacherList.txt", "w") as textFile:
    textFile.write(teacherList)