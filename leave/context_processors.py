import datetime

def my_date_today(request):
    return {'my_date_today' : datetime.datetime.now() }
