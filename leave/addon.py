from calendar import HTMLCalendar, LocaleHTMLCalendar
from datetime import date
from itertools import groupby
import logging

#from django.utils.html import conditional_escape as esc

class MikranCalendar(LocaleHTMLCalendar):

    css_mikran = {"Zaplanowany":"planned", "Zaakceptowany":"accepted","Odrzucony":"rejected"}

    def __init__(self, user_days):
        self.group_by_day = self.group_by_days(user_days)
        super(MikranCalendar, self).__init__()

    def formatday(self, day, weekday):
        k = '%02d-%02d-%04d' % (day,self.month,self.year)
        if(k in self.group_by_day):
            """
            Return a day as a table cell.
            """
            if day == 0:
                return '<td class="noday">&nbsp;</td>' # day outside month
            else:
                return '<td class="%s %s">%d</td>' % (self.cssclasses[weekday],self.css_mikran[self.group_by_day[k].status], day)

        else:            
            return super(MikranCalendar,self).formatday(day,weekday)

    def formatmonth(self, year, month, withyear=True):
        self.year, self.month = year, month
        return super(MikranCalendar, self).formatmonth(year, month, withyear)

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

    def group_by_days(self, user_days):
        return dict([(day.leave_date.strftime('%d-%m-%Y'),day.status) for day in user_days])
