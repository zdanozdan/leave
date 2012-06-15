from calendar import HTMLCalendar, LocaleHTMLCalendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

class MikranCalendar(LocaleHTMLCalendar):

    def __init__(self, freedays):
        super(MikranCalendar, self).__init__()
        self.freedays = self.group_by_day(freedays)

    def group_by_day(self, freedays):
        pass
#        field = lambda workout: workout.performed_at.day
#        return dict(
#            [(day, list(items)) for day, items in groupby(workouts, field)]
#            )
