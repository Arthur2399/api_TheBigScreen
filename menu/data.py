import pandas as pd
from djcines.settings import DIR

def datamenu():
    df = pd.read_csv(DIR+'menu/menu.csv')
    d=[]
    a = df.to_dict('records')
    for i in a:
        dat=[{
            'id':int(i['id']),
            'name':i['name'],
            'path':i['path'],
        }]
        for g in dat:
            d=d+[g]
    return d