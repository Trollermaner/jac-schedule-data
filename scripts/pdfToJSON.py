import pdfplumber
import re
import json

classData = pdfplumber.open("./dataCollector/data/classData.pdf")

class detailsClass:

    def __init__(self, fee = "", program_restriction = "", blended = "", intensive = "", notes = ""):
        self.fee = fee
        self.restrict = program_restriction
        self.exclusive = ""
        self.blended = blended
        self.intensive = intensive


class courseClass:
    def __init__(self, section, course_title, teacher_name = "", rating_map = {}, lab_map = {}, schedule_map = {}): 
        #rating, lab, detail and schedule all individual classes
        self.section = section
        self.teacher = teacher_name
        self.title = course_title
        self.rating = ""
        self.lab = lab_map
        self.details = detailsClass().__dict__
        self.schedule = schedule_map
    
    def __str__(self):
        return f"section: {self.section}, title: {self.title}, teacher: {self.teacher}, rating: {self.rating}, lab: {self.lab}, details: {self.details}, schedule: {self.schedule}"

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
        self.domain = ""
        self.ensemble = ""
        self.courseCode = ""
        self.title = ""
        self.section = ""
        self.teacher = ""
        self.rating = ""
        self.details = detailsClass().__dict__
        self.schedule = {}
    

def removeImpurities(line): #returns string

    trash = "(cid:10)"
    garbage = "(cid:13)"
    cleanLine = line

    while ( cleanLine.__contains__( trash ) or cleanLine.__contains__( garbage ) ):

        if cleanLine.__contains__( trash ):
            cleanLine = cleanLine.replace( trash , "" )

        if cleanLine.__contains__("(cid:13)"):
            cleanLine = cleanLine.replace( garbage , "" )

    return cleanLine

def allText(text, input): #returns string, input is array

    for line in input:
        text += line + "\n"

    return text

def addText(input):
    joined = " ".join(input)
    return joined

def splitLine(text, type = False): #return array #make it remove complementary rules completely
    lineArr = text.split("\n")

    if type:
        return lineArr

    if lineArr[2].__contains__("DOMAIN"):
        cleanArr = lineArr[2:-1]

        return cleanArr

    cleanArr = lineArr[3:-1]

    return cleanArr


def timeFormat(days, time, schedule = {}): #just put in course[index][schedule] blablabla (default is {})

    if schedule == {}:
        schedule = scheduleClass()
        schedule = schedule.__dict__

        for day in days:
            schedule[day] = time

        return schedule

    for day in days:
        schedule[day] = time
    
    return schedule

def isNewCourse(product, line): # newCourse = 0, newLesson = 1, Lab = 2

    try:
        section = line[0]
        course = line[2]
    except:
        return -1

    if re.match("[0-9][0-9][0-9][0-9][0-9]", section):

        if course not in product:
            return 0
        
        return 1

    return -1

def isBadFormat(line): #returns changed line to fit formatting
    newLine = line

    try:
        disc = line[1]
        lecture = line[0]

    except:
        return newLine
    
    garbage = "TRANSDIS"
    trash = "ENGINEER"
    feces = "CIPLINARY"
    poop = "ING"
    
    if (disc.__contains__(garbage)):
        courseCode = disc.replace( garbage, "" )
        newLine.insert(2, courseCode)
        return newLine

    elif (disc.__contains__(trash)):
        courseCode = disc.replace( trash, "" )
        newLine.insert(2, courseCode)
        return newLine

    if (lecture.__contains__(feces)):
        newLine[0] = "Lecture"

        return newLine

    elif (lecture.__contains__(poop)):
        newLine.pop(0)

        return newLine

    return newLine

def addLesson(line): #information: section, discipline, course number, course title, day, times

    section = line[0]
    courseTitle = addText(line[3:-2])
    
    lesson = courseClass(section, courseTitle)
    lesson = lesson.__dict__

    if courseTitle.__contains__("Blended"):
        lesson["details"]["blended"] = True

    return lesson

def addLab(line):
    teacher = teacherSeperate(line)
    lab = labClass(teacher)
    lab = lab.__dict__

    return lab


def teacherSeperate(line):

    if len(line) == 1:
        return "To Be Announced"
    
    elif line[1].__contains__("TBA"):
        return "To Be Announced"
    
    else:
        line.pop(0)
        joinTeacher = " ".join(line)
        splitTeacher = joinTeacher.split(", ")

        splitLastName = splitTeacher[0].split(" ")
        splitFirstName = splitTeacher[1].split(" ")

        firstName = splitFirstName[0]
        lastName = splitLastName[-1]

        teacherName = firstName + " " + lastName

    return teacherName

    
def isTeacher(line): #only gives true or false

    classType = line[0]

    if classType == "Lecture":
        return 0

    if classType == "Laboratory":
        return 1

    return -1

def isFee(line):
    fee = "fee:"
    Fee = "FEE:"
    feee = "fee."
    if fee in line or Fee in line or feee in line:
        return True

    return False

def getFee(line):
    
    for word in line:
        
        if word.__contains__("$"):

            money = word.replace("$", "")
            money = money.split(".")
            money = int(money[0])
            return money

def isRestriction(line):
    trigger = line[0]
    
    if trigger == "Not" and ("students." in line or "students" in line):
        return True
    
    return False

def getRestriction(line):
    studentLine = line[2 :]
    student = []
    for word in studentLine:

        if word == "students." or word == "students":
            student = " ".join(student)
            return student
        
        student.append(word)

def isExclusive(line):
    if line[-1] == "only" or line[-1] == "only.":
        return True

    return False

def getExclusive(line):
    newLine = line
    program = []
    if newLine[0] == "For":
        newLine.pop(0)
    
    for word in newLine:
        
        if word == "students":
            programWord = " ".join(program)
            return programWord

        program.append(word)

def isIntensive(line):
    if "Intensive" in line or "intensive" in line:
        return True

    return False

def setIntensive(line):
    passed = False
    stringLine = []
    for word in line:
        if word == "Intensive" or word == "intensive":
            passed = True
            stringLine.append(word)
        
        elif passed:
            stringLine.append(word)

    stringLine = " ".join(stringLine)
    return stringLine

def isHeader(line):

    if line[0] == "SECTION" and line[1] == "DISC":
        return True
    
    return False

def addExtraTitle(line):
    if re.match("[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", line[-1]):
        line = " ".join(line[0: -2])
        return line
    
    line = " ".join(line)
    return line
        
def addTeacherList(list, teacher):
    splitTeacher = teacher.split(" ")
    if (teacher not in list) and (teacher != "To Be Announced") and len(splitTeacher) > 1:
        list.append(teacher)
    
    return list

def isComplementary(line): #continue!!
    text = addText(line)

    if text == "Complementary Courses":
        return True
    
    return False

def addComplementary(line):
    complementary = complementaryClass()
    complementary = complementary.__dict__
    section = line[0]
    courseTitle = addText(line[3:-2])
    
    complementary["section"] = section
    complementary["title"] = courseTitle

    if courseTitle.__contains__("Blended"):
        complementary["details"]["blended"] = True

    return complementary

def isDomain(line):
    domain = line[0]

    if domain == "DOMAIN:":
        return True

    return False

def getDomain(line):
    domain = int(line[1])

    return domain

def isEnsemble(line):
    ensemble = line[0]

    if ensemble == "ENSEMBLE:":
        return True

    return False  

def getEnsemble(line):
    ensemble = int(line[1])

    return ensemble

def checkLine(lineArr): #parse and organize data into JSON

    product = {} # final product
    teacherList = []
    courseIndex = 0 # index of course we're adding information to
    courseCode = "" # code of course we're adding information to
    previousStatus = "" #is this next part of prereqs? Title? or wtv
    compIndex = -1
    domain = 0
    ensemble = 0
    complementary = False

    for line in lineArr:
        splittedLine = line.split(" ")
        newLine = isBadFormat(splittedLine)
        newCourseStatus = isNewCourse(product, newLine)
        teacherQ = isTeacher(newLine)
        if complementary == False:
            complementary = isComplementary(newLine) #make it add a Complementary to product

        if isHeader(newLine):
            newLine = ["bad"]

        elif newCourseStatus == 0: #add new course
            previousStatus = "lesson"
            courseIndex = 0
            courseCode = newLine[2]
            product[courseCode] = [addLesson(newLine)]

            if complementary:
                compCourse = addComplementary(newLine)
                compCourse["domain"] = domain
                compCourse["ensemble"] = ensemble
                compCourse["courseCode"] = courseCode
                product["complementary"].append(compCourse)
                compIndex += 1

        elif newCourseStatus == 1: #add lesson
            previousStatus = "lesson"
            courseCode = newLine[2]
            courseIndex = len(product[courseCode])
            product[courseCode].append(addLesson(newLine))

            if complementary:
                compCourse = addComplementary(newLine)
                compCourse["domain"] = domain
                compCourse["ensemble"] = ensemble
                compCourse["courseCode"] = courseCode
                product["complementary"].append(compCourse)
                compIndex += 1

        elif teacherQ == 0:
            teacher = teacherSeperate(newLine)
            previousStatus = "lecture"
            product[courseCode][courseIndex]["teacher"] = teacher
            
            teacherList = addTeacherList(teacherList, teacher)

            if complementary:
                product["complementary"][compIndex]["teacher"] = teacher
        
        elif teacherQ == 1:
            previousStatus = "lab"
            product[courseCode][courseIndex]["lab"] = addLab(newLine)
            
            teacher = product[courseCode][courseIndex]["lab"]["teacher"]
            
            teacherList = addTeacherList(teacherList, teacher)
            
        else:

            if complementary:
                if "complementary" not in product.keys():
                    product["complementary"] = []

                if isDomain(newLine):
                    previousStatus = "domain"
                    domain = getDomain(newLine)
                
                elif isEnsemble(newLine):
                    previousStatus = "ensemble"
                    ensemble = getEnsemble(newLine)
                
            
            if isFee(newLine):
                previousStatus = "fee"
                fee = getFee(newLine)
                product[courseCode][courseIndex]["details"]["fee"] = fee

                if complementary:
                    product["complementary"][compIndex]["details"]["fee"] = fee
            
            if isRestriction(newLine):
                previousStatus = "restriction"
                restriction = getRestriction(newLine)
                product[courseCode][courseIndex]["details"]["restrict"] = restriction

                if complementary:
                    product["complementary"][compIndex]["details"]["restrict"] = restriction

            if isExclusive(newLine):
                previousStatus = "exclusive"
                exclusive = getExclusive(newLine)
                product[courseCode][courseIndex]["details"]["exclusive"] = exclusive

                if complementary:
                    product["complementary"][compIndex]["details"]["exclusive"] = exclusive

            if isIntensive(newLine):
                previousStatus = "intensive"
                intensive = setIntensive(newLine)
                product[courseCode][courseIndex]["details"]["intensive"] = intensive

                if complementary:
                    product["complementary"][compIndex]["details"]["intensive"] = intensive
            
            elif previousStatus == "intensive":

                if re.match("[A-Z0-9][A-Z0-9][A-Z0-9]-[A-Z0-9][A-Z0-9][A-Z0-9]-[A-Z0-9][A-Z0-9]:", newLine[0]):
                    previousStatus = ""
                
                else:
                    intensive = addText(newLine)
                    product[courseCode][courseIndex]["details"]["intensive"] += intensive

                    if complementary:
                        product["complementary"][compIndex]["details"]["intensive"] += intensive

            if previousStatus == "lesson":
                extraTitle = addExtraTitle(newLine)

                product[courseCode][courseIndex]["title"] += extraTitle

                if complementary:
                    product["complementary"][compIndex]["title"] += extraTitle

        if re.match("[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", newLine[-1]): 
            scheduleDir = product[courseCode][courseIndex]["schedule"]
            days = newLine[-2]
            time = newLine[-1]
            product[courseCode][courseIndex]["schedule"] = timeFormat(days, time, scheduleDir)

            if complementary:
                scheduleDir = product["complementary"][compIndex]["schedule"]
                product["complementary"][compIndex]["schedule"] = timeFormat(days, time, scheduleDir)
    
    return [product, teacherList]

def parseClassData(pdf): #returns array: index[0] = JSON, index[1] = list of teachers

    text = ""

    for page in pdf.pages:

        pageText = page.extract_text()
        newPage = splitLine( removeImpurities(pageText) )
        text = allText(text, newPage) 
    
    cleanTextArray = splitLine(text, True) #array
    result = checkLine(cleanTextArray)
    product = result[0]
    teacherList = result[1]

    return [product, teacherList, text]

if False:
    with open("./dataCollector/results/text.txt", "w") as textFile:
        textFile.write(parseClassData(classData)[2])


