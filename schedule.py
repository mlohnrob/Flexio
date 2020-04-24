from bs4 import BeautifulSoup as bs
from lxml import html
import re


def get(self, session, schoolId, studentId):
    scheduleUrl = f"https://www.lectio.dk/lectio/{schoolId}/SkemaNy.aspx?type=elev&elevid={studentId}"

    schedulePage = session.get(scheduleUrl)

    schedulePageHtml = bs(schedulePage.text, features="html.parser")

    scheduleContainer = schedulePageHtml.findAll('a', {"class": "s2bgbox"})

    fullSchedule = []
    Schedule = {}

    for schedule in scheduleContainer:
        rows = schedule['data-additionalinfo'].split("\n")
        timeStructure = re.compile(
            '\d{2}/\d+-\d{4} \d{2}:\d{2} til \d{2}:\d{2}')
        teamStructure = re.compile('Hold: ')
        teacherStructure = re.compile('Lærer.*: ')
        roomStructure = re.compile('Lokale: ')

        # Getting the lesson id
        lessonIdSplit1 = schedule['href'].split("absid=")
        lessonIdSplit2 = lessonIdSplit1[1].split("&prevurl=")
        lessonId = lessonIdSplit2[0]

        # Check if there is a status
        if rows[0] == "Aflyst!" or rows[0] == "Ændret!":
            # print("found a status: {}".format(rows[0]))

            status = rows[0]

            # Check if there is a title
            if timeStructure.match(rows[1]):
                # print("did not find a title")
                title = ""
            else:
                # print("found a title: {}".format(rows[1]))
                title = rows[1]

        else:
            # print("did not find any status")
            status = ""

            # Check if there is a title
            if timeStructure.match(rows[0]):
                # print("did not find a title")
                title = ""
            else:
                # print("found a title: {}".format(rows[0]))
                title = rows[0]

        time = list(filter(timeStructure.match, rows))
        team = list(filter(teamStructure.match, rows))
        teacher = list(filter(teacherStructure.match, rows))
        room = list(filter(roomStructure.match, rows))

        fullSchedule.append((status, time, team, teacher, room))
    return fullSchedule
