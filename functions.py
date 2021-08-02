from datetime import datetime, timedelta, date
from collections import OrderedDict


def date_generator(format,start,end):
    if format == 'month':
        dates = [start, end]
        start, end = [datetime.strptime(_, "%Y-%m") for _ in dates]
        return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys())

    if format == 'week':
        if start.split('-')[0] != end.split('-')[0]:
            weeks = [f"{start.split('-')[0]}-{n}" for n in range(int(start.split('-')[1]),53)] 
            weeks += [f"{end.split('-')[0]}-{n}" for n in range(0,int(end.split('-')[1])+1)]
        else:
            weeks = [f"{start.split('-')[0]}-{n}" for n in range(int(start.split('-')[1]),int(end.split('-')[1]) + 1)] 
        return [x.replace('-','-0') if len(x) == 6 else x for x in weeks]

    if format == 'day':
        dates = [start, end]
        start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
        return list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m-%d"), None) for _ in range((end - start).days)).keys())
