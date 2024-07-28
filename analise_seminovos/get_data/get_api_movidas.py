import requests
import json
from datetime import datetime

url = "https://be-seminovos.movidacloud.com.br/elasticsearch/veiculos"

payload = json.dumps({
  "from": None,
  "localizacao": {
    "latitude": None,
    "longitude": None,
    "uf": None
  }
})
headers = {
  'authority': 'be-seminovos.movidacloud.com.br',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
  'content-type': 'application/json',
  'origin': 'https://www.seminovosmovida.com.br',
  'referer': 'https://www.seminovosmovida.com.br/',
  'sec-ch-ua': '"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'cross-site',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
}

def get_max(response):
  return response.json()['total']['value']

def get_cars(response):
  return response.json()['data']

all_cars = []
data_atual = datetime.now().strftime("%d%m%Y")

total_cars = get_max(requests.request("POST", url, headers=headers, data=payload))

for i in range(0,(total_cars + 1),20):
  payload_dict = json.loads(payload)
  payload_dict['from'] = i
  payload = json.dumps(payload_dict)

  response = requests.request("POST", url, headers=headers, data=payload)

  if response.status_code == 200:

    new_cars = get_cars(response)
    for car in new_cars:
      if car in all_cars:
        pass
      else:
        all_cars.append(car)

with open (f'E:\\Workspace\\analise_seminovos\\data\\all_cars{data_atual}.json', 'w', encoding='utf-8') as json_file:
  json.dump(all_cars, json_file, ensure_ascii=False, indent=2)