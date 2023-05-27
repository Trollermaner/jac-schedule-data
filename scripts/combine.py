teacherData = open("./dataCollector/results/results_no_rating.json", "r")
ratingData = open("./dataCollector/results/teacher_id.json", "r")

import json

teacher_json = json.load(teacherData)
rating_json = json.load(ratingData)

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
