import csv
import json


def make_json(csv_file_path, json_file_path):

    data = []
    with open(csv_file_path, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)

        for rows in csv_reader:

            data.append(rows)

    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        print('started writing file')
        jsonf.write(json.dumps(data, indent=4))
        print('finished writing')


csv_file_path = r'./CoinRep.csv'
json_file_path = r'./ngc-coins.json'

make_json(csv_file_path, json_file_path)
