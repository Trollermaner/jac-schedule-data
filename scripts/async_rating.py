import asyncio
import aiohttp
import json

class ratingClass:
    
    def __init__(self, teacher_rating = "", number_reviews = "", link = ""):
        self.rating = teacher_rating
        self.reviews = number_reviews
        self.link = link

async def getRating(s, id):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Basic dGVzdDp0ZXN0',
        'Content-Type': 'application/json',
    }

    json_data = {
        'query': 'query TeacherRatingsPageQuery(\n  $id: ID!\n) {\n  node(id: $id) {\n    __typename\n    ... on Teacher {\n      id\n      legacyId\n      firstName\n      lastName\n      department\n      school {\n        legacyId\n        name\n        city\n        state\n        country\n        id\n      }\n      lockStatus\n      ...StickyHeader_teacher\n      ...RatingDistributionWrapper_teacher\n      ...TeacherInfo_teacher\n      ...SimilarProfessors_teacher\n      ...TeacherRatingTabs_teacher\n    }\n    id\n  }\n}\n\nfragment StickyHeader_teacher on Teacher {\n  ...HeaderDescription_teacher\n  ...HeaderRateButton_teacher\n}\n\nfragment RatingDistributionWrapper_teacher on Teacher {\n  ...NoRatingsArea_teacher\n  ratingsDistribution {\n    total\n    ...RatingDistributionChart_ratingsDistribution\n  }\n}\n\nfragment TeacherInfo_teacher on Teacher {\n  id\n  lastName\n  numRatings\n  ...RatingValue_teacher\n  ...NameTitle_teacher\n  ...TeacherTags_teacher\n  ...NameLink_teacher\n  ...TeacherFeedback_teacher\n  ...RateTeacherLink_teacher\n}\n\nfragment SimilarProfessors_teacher on Teacher {\n  department\n  relatedTeachers {\n    legacyId\n    ...SimilarProfessorListItem_teacher\n    id\n  }\n}\n\nfragment TeacherRatingTabs_teacher on Teacher {\n  numRatings\n  courseCodes {\n    courseName\n    courseCount\n  }\n  ...RatingsList_teacher\n  ...RatingsFilter_teacher\n}\n\nfragment RatingsList_teacher on Teacher {\n  id\n  legacyId\n  lastName\n  numRatings\n  school {\n    id\n    legacyId\n    name\n    city\n    state\n    avgRating\n    numRatings\n  }\n  ...Rating_teacher\n  ...NoRatingsArea_teacher\n  ratings(first: 20) {\n    edges {\n      cursor\n      node {\n        ...Rating_rating\n        id\n        __typename\n      }\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n    }\n  }\n}\n\nfragment RatingsFilter_teacher on Teacher {\n  courseCodes {\n    courseCount\n    courseName\n  }\n}\n\nfragment Rating_teacher on Teacher {\n  ...RatingFooter_teacher\n  ...RatingSuperHeader_teacher\n  ...ProfessorNoteSection_teacher\n}\n\nfragment NoRatingsArea_teacher on Teacher {\n  lastName\n  ...RateTeacherLink_teacher\n}\n\nfragment Rating_rating on Rating {\n  comment\n  flagStatus\n  createdByUser\n  teacherNote {\n    id\n  }\n  ...RatingHeader_rating\n  ...RatingSuperHeader_rating\n  ...RatingValues_rating\n  ...CourseMeta_rating\n  ...RatingTags_rating\n  ...RatingFooter_rating\n  ...ProfessorNoteSection_rating\n}\n\nfragment RatingHeader_rating on Rating {\n  date\n  class\n  helpfulRating\n  clarityRating\n  isForOnlineClass\n}\n\nfragment RatingSuperHeader_rating on Rating {\n  legacyId\n}\n\nfragment RatingValues_rating on Rating {\n  helpfulRating\n  clarityRating\n  difficultyRating\n}\n\nfragment CourseMeta_rating on Rating {\n  attendanceMandatory\n  wouldTakeAgain\n  grade\n  textbookUse\n  isForOnlineClass\n  isForCredit\n}\n\nfragment RatingTags_rating on Rating {\n  ratingTags\n}\n\nfragment RatingFooter_rating on Rating {\n  id\n  comment\n  adminReviewedAt\n  flagStatus\n  legacyId\n  thumbsUpTotal\n  thumbsDownTotal\n  thumbs {\n    thumbsUp\n    thumbsDown\n    computerId\n    id\n  }\n  teacherNote {\n    id\n  }\n}\n\nfragment ProfessorNoteSection_rating on Rating {\n  teacherNote {\n    ...ProfessorNote_note\n    id\n  }\n  ...ProfessorNoteEditor_rating\n}\n\nfragment ProfessorNote_note on TeacherNotes {\n  comment\n  ...ProfessorNoteHeader_note\n  ...ProfessorNoteFooter_note\n}\n\nfragment ProfessorNoteEditor_rating on Rating {\n  id\n  legacyId\n  class\n  teacherNote {\n    id\n    teacherId\n    comment\n  }\n}\n\nfragment ProfessorNoteHeader_note on TeacherNotes {\n  createdAt\n  updatedAt\n}\n\nfragment ProfessorNoteFooter_note on TeacherNotes {\n  legacyId\n  flagStatus\n}\n\nfragment RateTeacherLink_teacher on Teacher {\n  legacyId\n  numRatings\n  lockStatus\n}\n\nfragment RatingFooter_teacher on Teacher {\n  id\n  legacyId\n  lockStatus\n  isProfCurrentUser\n}\n\nfragment RatingSuperHeader_teacher on Teacher {\n  firstName\n  lastName\n  legacyId\n  school {\n    name\n    id\n  }\n}\n\nfragment ProfessorNoteSection_teacher on Teacher {\n  ...ProfessorNote_teacher\n  ...ProfessorNoteEditor_teacher\n}\n\nfragment ProfessorNote_teacher on Teacher {\n  ...ProfessorNoteHeader_teacher\n  ...ProfessorNoteFooter_teacher\n}\n\nfragment ProfessorNoteEditor_teacher on Teacher {\n  id\n}\n\nfragment ProfessorNoteHeader_teacher on Teacher {\n  lastName\n}\n\nfragment ProfessorNoteFooter_teacher on Teacher {\n  legacyId\n  isProfCurrentUser\n}\n\nfragment SimilarProfessorListItem_teacher on RelatedTeacher {\n  legacyId\n  firstName\n  lastName\n  avgRating\n}\n\nfragment RatingValue_teacher on Teacher {\n  avgRating\n  numRatings\n  ...NumRatingsLink_teacher\n}\n\nfragment NameTitle_teacher on Teacher {\n  id\n  firstName\n  lastName\n  department\n  school {\n    legacyId\n    name\n    id\n  }\n  ...TeacherDepartment_teacher\n  ...TeacherBookmark_teacher\n}\n\nfragment TeacherTags_teacher on Teacher {\n  lastName\n  teacherRatingTags {\n    legacyId\n    tagCount\n    tagName\n    id\n  }\n}\n\nfragment NameLink_teacher on Teacher {\n  isProfCurrentUser\n  id\n  legacyId\n  firstName\n  lastName\n  school {\n    name\n    id\n  }\n}\n\nfragment TeacherFeedback_teacher on Teacher {\n  numRatings\n  avgDifficulty\n  wouldTakeAgainPercent\n}\n\nfragment TeacherDepartment_teacher on Teacher {\n  department\n  departmentId\n  school {\n    legacyId\n    name\n    id\n  }\n}\n\nfragment TeacherBookmark_teacher on Teacher {\n  id\n  isSaved\n}\n\nfragment NumRatingsLink_teacher on Teacher {\n  numRatings\n  ...RateTeacherLink_teacher\n}\n\nfragment RatingDistributionChart_ratingsDistribution on ratingsDistribution {\n  r1\n  r2\n  r3\n  r4\n  r5\n}\n\nfragment HeaderDescription_teacher on Teacher {\n  id\n  firstName\n  lastName\n  department\n  school {\n    legacyId\n    name\n    city\n    state\n    id\n  }\n  ...TeacherTitles_teacher\n  ...TeacherBookmark_teacher\n}\n\nfragment HeaderRateButton_teacher on Teacher {\n  ...RateTeacherLink_teacher\n}\n\nfragment TeacherTitles_teacher on Teacher {\n  department\n  school {\n    legacyId\n    name\n    id\n  }\n}\n',
        'variables': {
            'id': id,
        },
    }

    async with s.post('https://www.ratemyprofessors.com/graphql', headers=headers, json=json_data) as r:
        if r.status != 200:
            r.raise_for_status()

        return await r.json()

async def getRequest(s, teacher, school_id):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Basic dGVzdDp0ZXN0',
        'Content-Type': 'application/json',
    }

    json_data = {
            'query': 'query TeacherSearchResultsPageQuery(\n  $query: TeacherSearchQuery!\n  $schoolID: ID\n) {\n  search: newSearch {\n    ...TeacherSearchPagination_search_1ZLmLD\n  }\n  school: node(id: $schoolID) {\n    __typename\n    ... on School {\n      name\n    }\n    id\n  }\n}\n\nfragment TeacherSearchPagination_search_1ZLmLD on newSearch {\n  teachers(query: $query, first: 8, after: "") {\n    didFallback\n    edges {\n      cursor\n      node {\n        ...TeacherCard_teacher\n        id\n        __typename\n      }\n    }\n    pageInfo {\n      hasNextPage\n      endCursor\n    }\n    resultCount\n    filters {\n      field\n      options {\n        value\n        id\n      }\n    }\n  }\n}\n\nfragment TeacherCard_teacher on Teacher {\n  id\n  legacyId\n  avgRating\n  numRatings\n  ...CardFeedback_teacher\n  ...CardSchool_teacher\n  ...CardName_teacher\n  ...TeacherBookmark_teacher\n}\n\nfragment CardFeedback_teacher on Teacher {\n  wouldTakeAgainPercent\n  avgDifficulty\n}\n\nfragment CardSchool_teacher on Teacher {\n  department\n  school {\n    name\n    id\n  }\n}\n\nfragment CardName_teacher on Teacher {\n  firstName\n  lastName\n}\n\nfragment TeacherBookmark_teacher on Teacher {\n  id\n  isSaved\n}\n',
            'variables': {
                'query': {
                    'text': teacher,
                    'schoolID': school_id,
                    'fallback': True,
                    'departmentID': None,
                },
                'schoolID': school_id,
            },
    }

    async with s.post('https://www.ratemyprofessors.com/graphql', headers=headers, json=json_data) as r:
        if r.status != 200:
            r.raise_for_status()
        return await r.json()

def teacherMatch(first_name, last_name, school_id, node):
    num = 0
    if node["firstName"].__contains__(first_name):
        num+=1
    
    if node["lastName"].__contains__(last_name):
        num+=2
    
    if node["school"]["id"] == school_id:
        num+=2

    if num >= 4:
        return True

    return False


async def getTasks(session, school_id):
    tasks = []
    teacherList = ['Katherine Pagnucco', 'Christian Levesque', 'Patricia Foam', 'Jean-Paul Parkhill', 'Ruth Gordon', 'Simon Daoust', 'Christopher Roretz', 'Maryse Dagenais', 'Marie-Claire Rioux', 'Roxane Millette', 'Edward Hudson', 'Suzanne Black', 'Murray Bronet', 'Tian-Yun Wang', 'Jean-Michel Régimbal', 'Michael Lautman', 'Andrew Brown', 'Nicole Babich-Morin', 'Michal Goren', 'David Fenwick', 'Tania Peres', 'Sean Hughes', 'Rekha Iyer', 'Amélie Bérubé', 'Antonio Nicodemo', 'Sarah Worndle', 'Richard Léveillé', 'Rhoda Sollazzo', 'Antoine Herlin', 'Abdulrahman Karouma', 'Cameron Connor', 'Daniel Gatien', 'Ethan Mombourquette', 'Frank Vasco', 'Ivo Pendev', 'Jason Lucier', 'Kevin Flood', 'Kenneth Gerber', 'Mohammad Bardestani', 'Moushira Guindi', 'William Boshuck', 'Yuliya Klochko', 'Yu Zhao', 'Christophe Morris', 'Jordan Hill', 'Richard Masters', 'Richard Squire', 'Faranak Mokhtarian', 'Luiz Takei', 'Philippe Chaput', 'Philippe Delage', 'Kieran Hackett', 'Cynthia Giroux', 'Maria Mastorakos', 'Hubert Camirand', 'Christopher Tromp', 'Chris Larnder', 'Nanouk Pare', 'Etienne Portelance', 'Omar Melhem', 'Brian Larade', 'Paul Bazelais', 'Caroline Viger', 'Mandana Asl', 'Michael Richard', 'Bruce Tracy', 'Gregory Mulcair', 'Michael Dugdale', 'Cindy Hunzinger', 'Karim Jaffer', 'Robbyn Seller', 'Sarah Bean', 'Dario Guiducci', 'Sabrina Gloux', 'Laura Ricotta', 'James Kane', 'Sonia Savvidis', 'Gordon Spicer', 'Herman Tumurcuoglu', 'Tara Walker', 'Edward Lyon', 'Sorin Voinea', 'Magdy Meimari', 'David Koos', 'Kevin Williams', 'Steven Landry', 'Eugenia Bouras', 'John Serrati', 'Bertram Somers', 'Kenneth Matziorinis', 'Medoune Seck', 'David Desjardins', 'Mathieu Provencher', 'Avinash Samboo', 'Stephen Bryce', 'John Buskard', 'Jessica Burpee', 'Julie Podmore', 'Jessica Vandervort', 'Julien Charest', 'Catherine Humes', 'Andre Leblanc', 'Nicholas Tosaj', 'William Russell', 'Emmanuelle Carle', 'Felix Racine', 'Fiona Tomaszewski', 'Alexandre Panassenko', 'Audrey Baker', 'Andrea Spencer', 'Giulia Chiappetta', 'Gabriel Herta', 'Olivier Dubois', 'Sergio Fratarcangeli', 'Shery Mikhail', 'Karen Solsten', 'Derrick Chung', 'Alice McLeod', 'Caroline Lefebvre', 'Ibrahim Balushi', 'Vicki Beaupré-Odorico', 'Ryan Martin', 'Julien Laflamme', 'Nicola Hope', 'Jenny Cockburn', 'Onur Kapdan', 'Benedetto Angeloni', 'Elise Boer', 'Laura Shillington', 'Maude Riverin', 'Jessica Légère', 'Jean Sotiron', 'Charbel Nassif', 'Luba Serge', 'Stephanie Claude', 'Roger MacLean', 'Christophe Chowanietz', 'Kristin Anderson', 'Afroditi Panagopoulos', 'Vanessa Harrar', 'Brandon Daniel-Hughes', 'Luigi Pasto', 'Michelle Kwas', 'Steven Strudensky', 'Michael Foy', 'Jennifer Rocchi', 'Julie Caouette', 'Jacqueline Aubie', 'James Katz', 'Linda Knight', 'Julie Hanck', 'Peter Bender', 'Grace Lin', 'Wendi Hadd', 'Lisa Allen', 'Richard Element', 'Roksana Nazneen', 'Glenn Howlett', 'Jamie Macaulay', 'Monika Napier', 'Jamie Goodyear', 'Jennifer Lupien', 'Meghan Price', 'Sheila Nadimi', 'Gordana Mijovic', 'Avery Larose', 'Christina Oltmann', 'Jennifer McDermott', 'David Austin', 'Eric Laferriere', 'Maria Mamfredis', 'Denise Fidia', 'Nazareth Arabaghian', 'Brian Peters', 'Stephanie Myers', 'Tania Zampini', 'Jennifer Fisher', 'Pierre Dussol', 'Anne Golden', 'Frédérick Belzile', 'Yudi Sewraj', 'Nicole Forrest', 'Bettina Hoffmann', 'Daniel Schorr', 'Merdad Hage', 'Sarah Venart', 'Sara Villa', 'Thomas Abray', 'Daniel Rondeau', 'Clea Notar', 'Spaska Siderova', 'Angela Vella', 'Xiaoyang Zhu', 'Julie Gagnon', 'Paula Briones', 'Ryan Young', 'Edouard Fontaine', 'Elisha Conway', 'Ferenc Balogh', 'Derek Maisonville', 'Nicole Hoop', 'Elaine Pare', 'Wendy Eberle', 'Geoffrey Cook', 'Gediminas Lerner', 'Fiona Stewart', "Adil D'Sousa", 'Andrew Brock', 'Claire Russell', 'Finn Purcell', 'Mark Beers', 'Mathieu Bouchard', 'Brock Pennington', 'Robin Durnford', 'Lisa Szabo-Jones', 'Bruce Gilchrist', 'Ryan Maydan', 'Raymond Filipavicius', 'Kirsty Campbell', 'Rebecca Sultana', 'William McClelland', 'Valerie Bherer', 'Yann Geoffroy', 'Carousel Calvo', 'Jesse Bouvier', 'Kathleen MacNamara', 'Anna Sigg', 'Karen Lee', 'Lawrence Szigeti', 'Yael Margalit', 'Neil Briffett', 'Anna Lepine', 'Michele Trepanier', 'Jennifer Beauvais', 'Patrick Burger', 'David Bourgeois', 'Darren Millar', 'Ragne Raceviciute', 'Abraham Sosnowicz', 'Patricia Gordon', 'Marianne Campeau-Devlin', 'Proshat Hemmati', 'Christine Tellier', 'Claude Nicou', 'Louiza Aissani', 'Xiao Xu', 'Jean Beausoleil', 'Shahrouz Pezeshki', 'Isabelle Ste-Marie', 'Ariane Bessette', 'David Boutin', 'Frederic Laganiere', 'Alexandre Limoges', 'Sophie Prince', 'Marie-Claude Barrette', 'Michelle Legare', 'Catherine Greffard', 'Robert Inch', 'Maria Popica', 'Sylvie Mariage', 'Anna Woodrow', 'Paolo Stefano', 'Mario Bellemare', 'Kelly McKinney', 'Violaine Ares', 'Albert Sanchez', 'Johanna Okker', 'Mark McGuire', 'Alan Weiss', 'Hicham Tiflati', 'Deborah Lunny', 'Sujata Ghosh', 'Azra Rashid', 'Meredith Browne', 'Kathleen Sherwood', 'John Hamer', 'Roy Fu', 'Ful Massimi', 'Candis Steenbergen', 'Steven Sych', 'Eileen Kerwin', 'Sarwat Viqar', 'Thomas Young', 'Scott Armstrong', 'Joel Fitleberg', 'Sasan Ghinani', 'Monica Healey', 'Celine Homsy', 'Bronwen Lloyd-Hughes', 'Noémie Marin', 'Valerie Matthew', 'Brianna Miller', 'Laura Morrison', 'Andrew Plimer', 'Chelsea Privée', 'Geneviève Raymond-Parent', 'John Roberts', 'Jane Shaw', 'Robert Wall', 'Mikhail Zimerman', 'David Hill', 'Laura Pfeiffer', 'Jana Simandl', 'Giorgio Bartolucci', 'Manijeh Ali', 'Phoebe Jackson', 'Belinda Gare', 'Veronika Horlik']
    teacherData = {}
    goodTeacher = []

    for teacher in teacherList:
        task = asyncio.create_task(getRequest(session, teacher, school_id))
        tasks.append(task)
    response = await asyncio.gather(*tasks)
    num = 0
    for data in response:
        teacher = teacherList[num]
        if len(data["data"]["search"]["teachers"]["edges"]) != 0:
            teacher_node = data["data"]["search"]["teachers"]["edges"][0]["node"]
            teacherName = teacher.split(" ")
            first_name = teacherName[0]
            last_name = teacherName[1]

            if teacherMatch(first_name, last_name, school_id, teacher_node):

                teacherDict = ratingClass().__dict__
                teacherDict["link"] = "https://www.ratemyprofessors.com/professor/" + str(teacher_node["legacyId"])

                id = teacher_node["id"]
                goodTeacher.append([teacher, id])

                teacherData[teacher] = teacherDict
            else:
                teacherData[teacher] = "DNE"

        else:
            teacherData[teacher] = "DNE"

        num +=1
    
    tasks = []
    for data in goodTeacher:
        id = data[1]
        task = asyncio.create_task(getRating(session, id)) 
        tasks.append(task)
    
    response = await asyncio.gather(*tasks)

    num = 0
    for data in goodTeacher:
        teacher = data[0]
        r = response[num]
        rating = r["data"]["node"]["avgRating"]
        reviews = r["data"]["node"]["numRatings"]
        teacherData[teacher]["rating"] = rating
        teacherData[teacher]["reviews"] = reviews
        num +=1

    return teacherData

async def main(school_id):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        response = await getTasks(session, school_id)
    return response

if __name__ == '__main__':
    response = asyncio.run(main(school_id = "U2Nob29sLTEyMDUw"))
    with open("./dataCollector/results/asyncio.json", "w") as jsonFile:
        jsonFile.write(json.dumps(response, indent = 4))