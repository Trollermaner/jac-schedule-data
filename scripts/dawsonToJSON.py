import bs4
import json

with open("./data/dawson.html", "r") as data:
    html_data = data.read()

def parseDawson(html_data, complementary_data):

    def parseTime(dawsonDay, dawsonTime):
        
        dayConvert = {
            "Monday": "M",
            "Tuesday": "T",
            "Wednesday": "W",
            "Thursday": "R",
            "Friday": "F"
        }

        day = dayConvert[dawsonDay] #9:00 AM - 1:00 PM

        splitTime = dawsonTime.split(" - ")
        startTime = splitTime[0]
        endTime = splitTime[1]

        #check if PM

        splitStartTime = startTime.split(" ")
        splitEndTime = endTime.split(" ")

        startTime = splitStartTime[0].split(":")
        endTime = splitEndTime[0].split(":")

        stTime = startTime[0]
        edTime = endTime[0]

        if splitStartTime[1] == "PM" and stTime != "12":
            stTime = int(startTime[0]) + 12
            stTime = str(stTime)

        if splitEndTime[1] == "PM" and edTime != "12":
            edTime = int(endTime[0]) + 12
            edTime = str(edTime)

        if int(stTime) < 10:
            stTime = "0" + stTime

        if int(edTime) < 10:
            edTime = "0" + edTime

        time = stTime + startTime[1] + "-" + edTime + endTime[1]

        return [day, time]


    soup = bs4.BeautifulSoup(html_data, "html.parser")

    class detailsClass:

        def __init__(self):
            self.fee = ""
            self.restrict = ""
            self.exclusive = ""
            self.blended = ""
            self.intensive = ""
            self.comment = ""

    class courseClass:
        def __init__(self): 
            #rating, lab, detail and schedule all individual classes
            self.section = ""
            self.teacher = ""
            self.title = ""
            self.rating = {}
            self.lab = {}
            self.details = detailsClass().__dict__
            self.schedule = {}

    class labClass:
        
        def __init__(self, teacher_name = "", rating = {}):
            self.teacher = teacher_name
            self.rating = rating

    class scheduleClass:

        def __init__(self):
            self.M = ""
            self.T = ""
            self.W = ""
            self.R = ""
            self.F = ""

    class complementaryClass:

        def __init__(self):
            self.courseCode = ""
            self.title = ""
            self.section = ""
            self.teacher = ""
            self.rating = ""
            self.details = detailsClass().__dict__
            self.schedule = {}
        
        def __str__(self):
            return f"section: {self.section}, title: {self.title}, teacher: {self.teacher}, rating: {self.rating}, lab: {self.lab}, details: {self.details}, schedule: {self.schedule}"

    #function to transform dawson time to military time

    class_object = {}

    teacherList = []

    courseList = []

    for each_div in soup.find_all("div", {"class": "course-wrap"}): #each course
        
        course_code = each_div.find("div", {"class": "cnumber"}).text
        courseList.append(course_code)

        course_title = each_div.find("div", {"class": "ctitle"}).text

        newCourse = []

        for section_class in each_div.find_all("ul", {"class": "section-details"}): #class

            course = courseClass().__dict__

            for row in section_class.find_all("li", {"class": "row"}): #class section and teacher

                row_label = row.find("label", {"class": "col-md-2"}).text

                if row_label == "Section":
                    course["section"] = row.find("strong").text

                if row_label == "Teacher":

                    teacherLine = row.find("div", {"class": "col-md-10"}).text
                    course["teacher"] = teacherLine

                    if teacherLine not in teacherList:
                        teacherList.append(teacherLine)

                if row_label == "Teachers":

                    teacherLine = row.find("div", {"class": "col-md-10"}).text

                    splittedLine = teacherLine.split(", ")
                    course["teacher"] = splittedLine[0]
                    course["lab"] = labClass().__dict__
                    course["lab"]["teacher"] = splittedLine[1] #teacher array return to show list of teachers for getrating function

                    if splittedLine[0] not in teacherList:
                        teacherList.append(splittedLine[0])

                    if splittedLine[1] not in teacherList:
                        teacherList.append(splittedLine[1])

                if row_label == "Section Title":
                    course["title"] = row.find("div", {"class": "col-md-10"}).text

                if row_label == "Fee":
                    fee = row.find("div", {"class": "col-md-10"}).text #fee into integer
                    feeSplit = fee.split("$")
                    
                    fee = feeSplit[1]

                    feeSplit = fee.split(".")
                    fee = int(feeSplit[0])
                    
                    if fee > 0:
                        course["details"]["fee"] = fee

                if row_label == "Comment":
                    course["details"]["comment"] = row.find("div", {"class": "col-md-10"}).text

                if row_label == "Extra Information:": #intensive or smth
                    course["details"]["intensive"] = 'Dawson Intensive' #make this show link in schedule maker https://timetable.dawsoncollege.qc.ca/
            
            for schedule in section_class.find_all("table", {"class": "schedule-details"}): #class schedule

                course["schedule"] = scheduleClass().__dict__
                
                for schedule_row in schedule.find_all("tr"):

                    class_type = schedule_row.find("td", {"data-label": "Type"}).text 
                    
                    if class_type != "Intensive": #if intensive, do nothing

                        day = schedule_row.find("td", {"data-label": "Day"}).text
                        time = schedule_row.find("td", {"data-label": "Time"}).text

                        schedule_results = parseTime(day, time)
                        
                        course["schedule"][schedule_results[0]] = schedule_results[1]


            if course["title"] == "":
                course["title"] = course_title

            newCourse.append(course)
        class_object[course_code] = newCourse

    def compParse(data):
        soupComp = bs4.BeautifulSoup(data, "html.parser") #complementary

        newCourse = []

        for each_div in soupComp.find_all("div", {"class": "course-wrap"}):
            course_code = each_div.find("div", {"class": "cnumber"}).text

            course_title = each_div.find("div", {"class": "ctitle"}).text

            for section_class in each_div.find_all("ul", {"class": "section-details"}): #class

                course = complementaryClass().__dict__

                course["courseCode"] = course_code

                for row in section_class.find_all("li", {"class": "row"}): #class section and teacher

                    row_label = row.find("label", {"class": "col-md-2"}).text

                    if row_label == "Section":
                        course["section"] = row.find("strong").text

                    if row_label == "Teacher":

                        teacherLine = row.find("div", {"class": "col-md-10"}).text
                        course["teacher"] = teacherLine

                        if "TBA" in teacherLine:
                            course["teacher"] = "To Be Announced"

                        if (teacherLine not in teacherList) and course["teacher"] != "To Be Announced":
                            teacherList.append(teacherLine)

                    if row_label == "Teachers":

                        teacherLine = row.find("div", {"class": "col-md-10"}).text

                        splittedLine = teacherLine.split(", ")
                        course["teacher"] = splittedLine[0]
                        course["lab"] = labClass().__dict__
                        course["lab"]["teacher"] = splittedLine[1] #teacher array return to show list of teachers for getrating function

                        if splittedLine[0] not in teacherList:
                            teacherList.append(splittedLine[0])

                        if splittedLine[1] not in teacherList:
                            teacherList.append(splittedLine[1])

                    if row_label == "Section Title":
                        course["title"] = row.find("div", {"class": "col-md-10"}).text

                    if row_label == "Fee":
                        fee = row.find("div", {"class": "col-md-10"}).text #fee into integer
                        feeSplit = fee.split("$")
                        
                        fee = feeSplit[1]

                        feeSplit = fee.split(".")
                        fee = int(feeSplit[0])
                        
                        if fee > 0:
                            course["details"]["fee"] = fee

                    if row_label == "Comment":
                        course["details"]["comment"] = row.find("div", {"class": "col-md-10"}).text

                    if row_label == "Extra Information:": #intensive or smth
                        course["details"]["intensive"] = 'Dawson Intensive' #make this show link in schedule maker https://timetable.dawsoncollege.qc.ca/
                
                for schedule in section_class.find_all("table", {"class": "schedule-details"}): #class schedule

                    course["schedule"] = scheduleClass().__dict__
                    
                    for schedule_row in schedule.find_all("tr"):

                        class_type = schedule_row.find("td", {"data-label": "Type"}).text 
                        
                        if class_type != "Intensive": #if intensive, do nothing

                            day = schedule_row.find("td", {"data-label": "Day"}).text
                            time = schedule_row.find("td", {"data-label": "Time"}).text

                            schedule_results = parseTime(day, time)
                            
                            course["schedule"][schedule_results[0]] = schedule_results[1]


                if course["title"] == "":
                    course["title"] = course_title

                newCourse.append(course)

        return newCourse
        

    class_object["COMPLEMENTARY"] = compParse(complementary_data)


    return [class_object, teacherList, courseList]
    #course title able to search up


