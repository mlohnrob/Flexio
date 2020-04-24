import requests
from lxml import html
from bs4 import BeautifulSoup

import schedule


class Lectio:
    def __init__(self, username, password, schoolId):
        self.username = username
        self.password = password
        self.schoolId = str(schoolId)

        loginUrl = f"https://www.lectio.dk/lectio/{self.schoolId}/login.aspx"

        session = requests.Session()

        loginPage = session.get(loginUrl)

        tree = html.fromstring(loginPage.text)

        authenticity_token = list(
            set(tree.xpath("//input[@name='__EVENTVALIDATION']/@value")))[0]

        body = {
            "m$Content$username2": self.username,
            "m$Content$password2": self.password,
            "m$Content$passwordHidden": self.password,
            "__EVENTVALIDATION": authenticity_token,
            "__EVENTTARGET": "m$Content$submitbtn2",
            "__EVENTARGUMENT": "",
            "LectioPostbackId": ""
        }
        loginPost = session.post(loginUrl, data=body, headers={
                                 "referer": loginUrl})

        homePageUrl = f"https://www.lectio.dk/lectio/{self.schoolId}/forside.aspx"
        homePage = session.get(homePageUrl)

        homePageHtml = BeautifulSoup(homePage.text, features="html.parser")

        studentIdFind = homePageHtml.find(
            "a", {"id": "s_m_HeaderContent_subnavigator_ctl01"}, href=True)
        print(studentIdFind)

        self.studentId = (studentIdFind['href']).replace(
            f"/lectio/{self.schoolId}/forside.aspx?elevid=", '')

        self.session = session

    def getSchedule(self):
        result = schedule.get(self, self.session,
                              self.schoolId, self.studentId)
        return result


f = open("secret.txt", "r")
user = f.readlines()

username = user[0].split(" ")[0]
password = user[0].split(" ")[1]


hej = Lectio(username, password, 137)

skema = hej.getSchedule()


print(skema)
