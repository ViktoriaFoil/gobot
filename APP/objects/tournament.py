import datetime


class Tournament:

    def __init__(self):
        self.start = ""
        self.end = ""
        self.name = ""
        self.city = ""
        self.link = ""
        self.flag = ""

    def setStart(self, start):
        format_string = "%d.%m.%Y"
        self.start = datetime.datetime.strptime(start, format_string).strftime("%Y-%m-%d")

    def setEnd(self, end):
        format_string = "%d.%m.%Y"
        self.end = datetime.datetime.strptime(end, format_string).strftime("%Y-%m-%d")

    def setName(self, name):
        self.name = name

    def setCity(self, city):
        self.city = city

    def setLink(self, link):
        self.link = link

    def setFlag(self, flag):
        self.flag = flag


