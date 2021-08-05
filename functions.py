from datetime import datetime, timedelta, date
from collections import OrderedDict
import base64


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

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download results (.csv)</a>'
    return href