import xml.etree.ElementTree as ET
from datetime import datetime
import requests


class WorkCalendar:
    def __init__(self):
        self.base_url = 'https://raw.githubusercontent.com/\
xmlcalendar/data/master/ru/'
        self.holidays = []
        self.workdays = []
        self._go()

    def _go(self):
        self.get_calendar()
        self.parse_calendar()

    def parse_calendar(self):
        tree = ET.fromstring(self.file.text)
        all_days = tree.find('days')
        for item in all_days:
            date = datetime.strptime(str(item.attrib['d']), '%m.%d')
            date = date.replace(year=datetime.today().year)
            if item.attrib['t'] == '1':
                self.holidays.append(date)
            if item.attrib['t'] == '2':
                self.workdays.append(date)

    def get_calendar(self):
        full_url = self.base_url +\
            str(datetime.today().year) +\
            '/calendar.xml'
        self.file = requests.get(full_url)
        if self.file.status_code == 200:
            return self.file.content
        else:
            self.file.raise_for_status()
