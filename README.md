```
env FLASK_APP=app.py FLASK_ENV=development flask run
```

```sh
###################
# BBCE STATE (IL) #
###################

# Compare results with: https://www.dhs.state.il.us/page.aspx?item=33412

# IL, 1 person, no income or savings
curl -X POST -H "Content-Type: application/json" \
  -d @./sample_input_data/il-1-person-no-income-or-savings.json \
  http://127.0.0.1:5000/calculate

# IL, 2 people, no income or savings
curl -X POST -H "Content-Type: application/json" \
  -d @./sample_input_data/il-2-person-no-income-or-savings.json \
  http://127.0.0.1:5000/calculate

# IL, 3 people, no income or savings
curl -X POST -H "Content-Type: application/json" \
  -d @./sample_input_data/il-3-person-no-income-or-savings.json \
  http://127.0.0.1:5000/calculate

# IL, 4 people, no income or savings
curl -X POST -H "Content-Type: application/json" \
  -d @./sample_input_data/il-4-person-no-income-or-savings.json \
  http://127.0.0.1:5000/calculate

#######################
# NON-BBCE STATE (UT) #
#######################

# No income or savings
curl -X POST -H "Content-Type: application/json" \
  -d @./sample_input_data/ut-2-person-no-income-or-savings.json \
  http://127.0.0.1:5000/calculate

# Monthly income of $1,700 (fails net eligibility limit for household size and state)
curl -X POST -H "Content-Type: application/json" \
  -d @./sample_input_data/ut-2-person-above-net-income.json \
  http://127.0.0.1:5000/calculate

# Household includes elderly member, meets net but not gross limit
curl -X POST -H "Content-Type: application/json" \
  -d @./sample_input_data/ut-2-person-elderly-eligible-via-net-income.json \
  http://127.0.0.1:5000/calculate

# No income, but resources too high
curl -X POST -H "Content-Type: application/json" \
  -d @./sample_input_data/ut-2-person-no-income-but-resources-too-high.json \
  http://127.0.0.1:5000/calculate

# Household includes elderly member, meets resource limite for household w/ elderly member
curl -X POST -H "Content-Type: application/json" \
  -d @./sample_input_data/ut-2-person-no-income-meets-resource-limit-elderly.json \
  http://127.0.0.1:5000/calculate

# 3 person household -- Household includes elderly member, meets resource limite for household w/ elderly member
curl -X POST -H "Content-Type: application/json" \
  -d @./sample_input_data/ut-3-person-no-income-meets-resource-limit-elderly.json \
  http://127.0.0.1:5000/calculate
```