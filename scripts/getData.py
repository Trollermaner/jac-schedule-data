import pdfplumber
import re
import asyncio
from time import perf_counter
#teacherData = open("./dataCollector/results/results_no_rating.json", "r")
#ratingData = open("./dataCollector/results/teacher_id.json", "r")
pdfData = pdfplumber.open("./dataCollector/data/classData.pdf")

from async_rating import asyncGetRating
from pdfToJSON import parseClassData

import json

startParse = perf_counter()
classData = parseClassData(pdfData)
stopParse = perf_counter()

print(f"Time to parse: {stopParse - startParse} seconds")

teacherData = classData[0]
teacherList = classData[1]


school_id = "U2Nob29sLTEyMDUw"

startRating = perf_counter()
ratingData = asyncio.run(asyncGetRating(school_id, teacherList))
stopRating = perf_counter()

print(f"Time to get ratings {stopRating - startRating} seconds")

teacher_json = teacherData
rating_json = ratingData

for course in teacher_json.keys():
    if course == "complementary":
        num = 0
        for lesson in teacher_json["complementary"]:
            teacher = lesson["teacher"]
            
            if teacher != "To Be Announced":
                rating = rating_json[teacher]
                teacher_json["complementary"][num]["rating"] = rating
                num += 1
    
    else:
        num = 0
        for lesson in teacher_json[course]:
            teacher = lesson["teacher"]
            if teacher != "To Be Announced":
                rating = rating_json[teacher]

                teacher_json[course][num]["rating"] = rating

            if lesson["lab"] != {}:
                teacher = lesson["lab"]["teacher"]

                if teacher != "To Be Announced":
                    rating = rating_json[teacher]

                    teacher_json[course][num]["lab"]["rating"] = rating
            num+=1 

with open("./dataCollector/results/final_results.json", "w") as results_json:
    results_json.write(json.dumps(teacher_json, indent=4))
