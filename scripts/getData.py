import pdfplumber
import re
import asyncio
from time import perf_counter
startProgram = perf_counter()
#teacherData = open("./dataCollector/results/results_no_rating.json", "r")
#ratingData = open("./dataCollector/results/teacher_id.json", "r")
pdfData = pdfplumber.open("./data/F23_JAC_June.pdf")

with open("./data/dawson.html", "r") as dawson_html:
    dawson_data1 = dawson_html.read()
with open("./data/dawson_complementary.html", "r") as dawson_complementary:
    dawson_data2 = dawson_complementary.read()

from dawsonToJSON import parseDawson

from async_rating import asyncGetRating
from pdfToJSON import parseClassData

import json

school = input("school? (jac or dawson)")

if school == "jac":
    classData = parseClassData(pdfData)

else:
    classData = parseDawson(dawson_data1, dawson_data2)

startParse = perf_counter()
stopParse = perf_counter()

print(f"Time to parse: {stopParse - startParse} seconds")

teacherData = classData[0]
teacherList = classData[1]

school_id_dict = {"jac": "U2Nob29sLTEyMDUw", "dawson": "U2Nob29sLTEyMDQ0"}

school_id = school_id_dict[school]

startRating = perf_counter()
ratingData = asyncio.run(asyncGetRating(school_id, teacherList))
stopRating = perf_counter()

print(f"Time to get ratings: {stopRating - startRating} seconds")

teacher_json = teacherData
rating_json = ratingData

for course in teacher_json.keys():
    if course == "COMPLEMENTARY":
        num = 0
        for lesson in teacher_json["COMPLEMENTARY"]:
            teacher = lesson["teacher"]
            teacher_json["COMPLEMENTARY"][num]["rating"] = "DNE"
            if teacher != "To Be Announced":
                rating = rating_json[teacher]
                teacher_json["COMPLEMENTARY"][num]["rating"] = rating
            num += 1
    
    else:
        num = 0
        for lesson in teacher_json[course]:
            teacher = lesson["teacher"]
            teacher_json[course][num]["rating"] = "DNE"

            if teacher != "To Be Announced":
                rating = rating_json[teacher]

                teacher_json[course][num]["rating"] = rating

            if lesson["lab"] != {}:
                teacher = lesson["lab"]["teacher"]
                teacher_json[course][num]["lab"]["rating"] = "DNE"
                if teacher != "To Be Announced":
                    rating = rating_json[teacher]

                    teacher_json[course][num]["lab"]["rating"] = rating
            num+=1 

endProgram = perf_counter()
print(f"Time to run program: {endProgram - startProgram} seconds")

if school == "jac":
    with open("./results/final_results.json", "w") as results_json:
        results_json.write(json.dumps(teacher_json, indent=4))

elif school == "dawson":
    with open("./results/dawson.json", "w") as results_json:
        results_json.write(json.dumps(teacher_json, indent=4))