import csv
import yaml

data = {}

reader = csv.DictReader(
    open('Copy-of-SNAP-SUA-Table-FY2019.csv', newline=''),
    fieldnames=[
        'STATE_WITH_REGION',
        'HEATING_AND_COOLING_UTILITY_ALLOWANCE',
        'BASIC_LIMITED_UTILITY_ALLOWANCE',
        'ELECTRICITY',
        'GAS_AND_FUEL',
        'WATER',
        'SEWAGE',
        'TRASH',
        'PHONE',
    ])

for index, row in enumerate(reader):
    if index > 0:
        state_with_region = row['STATE_WITH_REGION']
        row.pop('STATE_WITH_REGION')
        data[state_with_region] = row

yaml_data = yaml.dump(data)

output_file = open('standard_utility_allowances_draft.yaml', 'r+')
output_file.write(yaml_data)
