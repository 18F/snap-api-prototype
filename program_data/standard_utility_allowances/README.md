## Parsing Standard Utility Allowances data

FNS provides a spreadsheet of information about standard utility allowances by state and utility:

https://www.fns.usda.gov/snap/eligibility/deduction/standard-utility-allowances

There are too many data points to make hard-coding sensible, but enough complexity that simply transforming the CSV to YAML and using the raw output YAML directly isn't feasible.

I use a script to transform the raw CSV into raw YAML, and will then pull that YAML out into the main `standard_utility_allowances.yaml` file in the folder above on a state-by-state basis.

This sub-folder contains:

1. `Copy-of-SNAP-SUA-Table-FY2019.csv`: Raw CSV data.
2. `sua_csv_to_yaml.py`: Python script to transform the CSV to YAML.
3. `standard_utility_allowances_draft.yaml`: Raw YAML data; will pull this into the main program data file state by state, handling complexities like multiple regions in one state and different values for different household sizes as they arise.

Run the script:

```
python sua_csv_to_yaml.py
```
