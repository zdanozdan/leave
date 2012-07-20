# This Python file uses the following encoding: utf-8

from calendar import HTMLCalendar, LocaleHTMLCalendar
from datetime import date
from itertools import groupby
from collections import defaultdict
import locale

from django.core.urlresolvers import reverse

import logging

#from django.utils.html import conditional_escape as esc

class MikranCalendar(LocaleHTMLCalendar):

    css_mikran = {"Zaplanowany":"planned", "Zaakceptowany":"accepted","Odrzucony":"rejected","Obecny":"present","Lekarskie":"sick"}
    free_days_2012 = {
        #1 stycznia 2012	niedziela	Nowy Rok
        "01-01-2012":"Nowy Rok",        
        #6 stycznia 2012	piątek	Święto Trzech Króli
        "06-01-2012":"Święto Trzech Króli",
        #8 kwietnia 2012	niedziela	Wielkanoc – 1 dzień świąt Wielkanocnych
        "08-04-2012":"Wielkanoc – 1 dzień świąt Wielkanocnych",
        #9 kwietnia 2012	poniedziałek	Lany Poniedziałek – 2 dzień świąt Wielkanocnych
        "09-04-2012":"Lany Poniedziałek – 2 dzień świąt Wielkanocnych",
        #1 maja 2012	wtorek	1 Maja – Święto Pracy
        "01-05-2012":"1 Maja – Święto Pracy",
        #3 maja 2012	czwartek	Święto Konstytucji 3 Maja
        "03-05-2012":"Święto Konstytucji 3 Maja",
        #27 maja 2012	niedziela	Zesłanie Ducha Świętego
        "27-05-2012":"Zesłanie Ducha Świętego",
        #7 czerwca 2012	czwartek	Boże Ciało
        "07-06-2012":"Boże Ciało",
        #15 sierpnia 2012	środa	Wniebowzięcie NMP
        "15-08-2012":"Wniebowzięcie NMP",
        #1 listopada 2012	czwartek	Dzień Wszystkich Świętych
        "01-11-2012":"Dzień Wszystkich Świętych",
        #11 listopada 2012	niedziela	Narodowe Święto Niepodległości
        "11-11-2012":"Narodowe Święto Niepodległości",
        #25 grudnia 2012	wtorek	Boże Narodzenie – pierwszy dzień świąt
        "25-12-2012":"Boże Narodzenie – pierwszy dzień świąt",
        #26 grudnia 2012	środa	Boże Narodzenie – drugi dzień świąt
        "26-12-2012":"Boże Narodzenie – drugi dzień świąt"
        }

    def __init__(self, user_days, selected_id = None):

        locale.setlocale(locale.LC_ALL, 'pl_PL.utf8')

        #main view do not show "Present"
        if selected_id:
            self.group_status_by_day = self.group_status_by_days(user_days)
        else:
            self.group_status_by_day = self.group_status_by_days(user_days,"Obecny")

        self.group_users_by_day = self.group_users_by_days(user_days)        
        self.selected_id = selected_id

        super(MikranCalendar, self).__init__(locale='pl_PL.utf8')

    def formatday(self, day, weekday):
        k = '%02d-%02d-%04d' % (day,self.month,self.year)
        
        #different url for main view and user view
        #
        url = reverse('leave.views.show_present',args=(self.year,self.month,day,))
        if self.selected_id:
            url = reverse('leave.views.single_present',args=(self.selected_id,self.year,self.month,day,))

        if(k in self.group_status_by_day):
            """
            Return a day as a table cell.
            """
            if day == 0:
                return '<td class="noday">&nbsp;</td>' # day outside month
            elif k in self.free_days_2012:
                return '<td title="%s" class="freeday">%d</td>' % (self.free_days_2012[k],day)
            else:
                css_multiple = "single"
                if len(self.group_users_by_day[k]) > 1: css_multiple = "multiple"

                names = ",".join(self.group_users_by_day[k])
                return '<td title="%s" class="%s %s %s"><a href="%s">%d</a></td>' % (names.encode('utf-8'), 
                                                                                     self.cssclasses[weekday],
                                                                                     self.css_mikran[self.group_status_by_day[k].status], 
                                                                                     css_multiple,
                                                                                     url,
                                                                                     day)

        else:  
            if day == 0:
                return '<td class="noday">&nbsp;</td>' # day outside month
            elif k in self.free_days_2012:
                return '<td title="%s" class="freeday">%d</td>' % (self.free_days_2012[k],day)
            else:                
                return '<td title="pokaż obecność" class="%s"><a href="%s">%d</a></td>' % (self.cssclasses[weekday],url,day)

    def formatmonth(self, year, month, withyear=True):
        self.year, self.month = year, month
        return super(MikranCalendar, self).formatmonth(year, month, withyear)

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

    def group_status_by_days(self, user_days, exclude=""):
        return dict([(day.leave_date.strftime('%d-%m-%Y'),day.status) for day in user_days if day.status.status != exclude])

    def group_users_by_days(self, user_days):
        users = ([(day.leave_date.strftime('%d-%m-%Y'),day.user.first_name) for day in user_days])
        fq= defaultdict(list)
        for n,v in users:
            fq[n].append(v)

        return fq

    def group_days_by_statuses(self, user_days):
        days = ([(day.status.status,day.user.first_name) for day in user_days])
        fq= defaultdict(list)
        for n,v in days:
            fq[n].append(v)

        return fq
