import requests
import pandas as pd

url = 'http://127.0.0.1:8000/all_functions'

def test_api():
    params = {
        'test':'can we plan a meeting for tomorrow ?'    
    }

    response = requests.get(url, params=params)
    return response.json()

if __name__ == '__main__':
    
    print(test_api())