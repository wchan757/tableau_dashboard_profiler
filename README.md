# 🧐 Tableau Dashboard Profiler 🕵️‍♀️

Tableau Dashboard Profiler is your secret agent for analyzing Tableau workbook files. It dives into your `.twbx` files and retrieves field-level details, helping you understand the structure and content of your dashboards.

## 💼 Requirements

Before you start, make sure you've installed the necessary Python packages. You can do this by running the following command in your terminal:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

Follow these steps to analyze your Tableau workbooks:

1. Import the `DashboardAnalyzer` class from `tableau_dashboard_profiler.py`.
2. Initialize a `DashboardAnalyzer` instance with the path to the directory or file containing your `.twbx` Tableau workbooks.
3. Call the `analyze` method on the `DashboardAnalyzer` instance.
4. Optionally, provide an output path and a `create_dir` flag. The script will save the output CSV files in this directory. If the directory doesn't exist, setting `create_dir` to `True` will create it.
5. If you set `return_concat` to `True` when calling `analyze`, the method will return a DataFrame with the analysis results.

Here's an example:

```python
from tableau_dashboard_profiler import DashboardAnalyzer

input_path = r'/path/to/your/workbooks'
output_path = r'/path/to/output/directory'

# Initialize the analyzer
analyzer = DashboardAnalyzer(input_path, output_path, create_dir=True)

# Analyze the workbooks and get a DataFrame of the results
df = analyzer.analyze(return_concat=True)

# See what the analyzer found
if df is not None:
    print(df)
```

## 🎁 Output

The `analyze` method saves a CSV file for each analyzed `.twbx` workbook in the specified output directory. Each CSV file contains the following columns:

- 'Dashboard Name'
- 'Worksheet Name'
- 'Field Name'
- 'Field Calculation'
- 'Field Type'
- 'Field Role'
- 'Field Aggregation'

If `return_concat` is set to `True`, the `analyze` method also returns a DataFrame that contains all the results combined.

Happy Profiling! 🕵️‍♀️🔍📊

---
