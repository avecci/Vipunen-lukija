import requests
import json
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

url = 'http://api.vipunen.fi/api/resources/'
server = 'fill from AWS'
user = 'admin'
passw = 'YourPwdShouldBeLongAndSecure!'
database = 'insert existing db name'

def return_all_values_by_item(url, item):
    """
    Return API results as json dump without filtering
    Input: URL, item
    - Example::
        url = 'http://api.vipunen.fi/api/resources/'
        return_all_values_by_item(url, 'avoin_yliopisto')
    """
    response = requests.get(url+'/'+item+'/data')
    if response.status_code != 200:
        raise Exception('Error code {}'.format(response.status_code))
    else:
        response.encoding = 'ISO-8859-1'
        response = response.json()
        response = json.dumps(response, indent=4, sort_keys=True, ensure_ascii=True)
        return response

def return_values_by_item(url, item, filter):
    """
    Return API results as json dump, filter result set by variable
    Input: URL, item, filter
    - Example::
        url = 'http://api.vipunen.fi/api/resources/'
        return_values_by_item(url, 'avoin_yliopisto', 'tilastovuosi==2018')
        curl http://api.vipunen.fi/api/resources/avoin_yliopisto/data?filter=tilastovuosi==2018
    """
    response = requests.get(url+value+'/data'+'?'+'filter='+filter)
    if response.status_code != 200:
        raise Exception('Error code {}'.format(response.status_code))
    else:
        response.encoding = 'ISO-8859-1'
        response = response.json()
        response = json.dumps(response, indent=4, sort_keys=True, ensure_ascii=True)
        return response


def main():
    """
    Create sql connection using SQL Alchemy, connect to database instance.
    Load data in variable 'data' and transform it into pandas dataframe.
    Populate table in SQL server database using pandas functionality.
    """
    engine = create_engine('mssql+pyodbc://'+user+':'+passw+'@'+server+'/'+database+"?driver=SQL+Server", pool_recycle=360)
    connection = engine.connect()
    for value in resources:
        print("Data to be inserted:", value)
        data = return_all_values_by_item(url, value)
        data = json.loads(data)
        data = pd.DataFrame(data)
        print("Amount of data:", data.shape)
        data.to_sql(value, con=connection, if_exists='replace')
    connection.close()


if __name__ == "__main__":
    resources = requests.get(url)
    resources = resources.json()
    main()
