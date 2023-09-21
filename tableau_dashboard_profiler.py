from tableaudocumentapi import Workbook
from os import listdir
from os.path import isfile, join, splitext, basename
import os
import pandas as pd

class TableauWorkbookAnalyzer:
    """
    This class represents a Tableau Workbook Analyzer which analyzes a single Tableau workbook.
    """
    def __init__(self, workbook_path):
        """
        Initialize the analyzer with the path to the Tableau workbook.
        """
        self.workbook = Workbook(workbook_path)

    def analyze(self, fields_to_append=None):
        """
        Analyze the workbook and return a DataFrame with the results.
        :param fields_to_append: List of field attributes to append to the output.
        :return: DataFrame with analysis results.
        """
        print(f"Analyzing workbook: {self.workbook.filename}")

        data = []
        for worksheet in self.workbook.worksheets:
            for datasource in self.workbook.datasources:
                for field in datasource.fields.values():
                    if worksheet in field.worksheets:
                        row = {
                            'Dashboard Name': splitext(basename(self.workbook.filename))[0],
                            'Worksheet Name': worksheet,
                            'Field Name': field.name,
                            'Field Calculation': field.calculation,
                            'Field Type': field.datatype,
                            'Field Role': field.role,
                            'Field Aggregation': field._aggregation
                        }
                        if fields_to_append:
                            for custom_field in fields_to_append:
                                row[custom_field] = getattr(field, custom_field, None)
                        data.append(row)

        return pd.DataFrame(data)

class DashboardAnalyzer:
    """
    This class represents a Dashboard Analyzer which analyzes one or more Tableau workbooks.
    """
    def __init__(self, input_path, output_path=None, create_dir=False):
        """
        Initialize the analyzer with the path to the directory or file containing the workbooks.
        """
        self.input_path = input_path
        self.output_path = output_path if output_path else input_path
        if isfile(input_path):
            self.files = [input_path]
        else:
            self.files = [join(input_path, f) for f in listdir(input_path) if isfile(join(input_path, f)) and f.endswith('.twbx')]
        
        if create_dir and not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        else:
            self.output_path=input_path

    def analyze(self, fields_to_append=None, return_concat=False):
        """
        Analyze the workbooks and optionally return a DataFrame with the results.
        :param fields_to_append: List of field attributes to append to the output.
        :param return_concat: If True, return a concatenated DataFrame of all results.
        :return: If return_concat is True, return a DataFrame with analysis results.
        """
        data = []
        for file in self.files:  
            try:
                analyzer = TableauWorkbookAnalyzer(file)
                df = analyzer.analyze(fields_to_append)
                data.append(df)

                csv_filename = splitext(basename(file))[0] + '_docs.csv'
                csv_path = join(self.output_path, csv_filename)
                df.to_csv(csv_path, index=False)
                print(f"Saved data to {csv_path}")
            except Exception as e:
                print(f"Failed to analyze {file}: {str(e)}")

        if return_concat:
            return pd.concat(data, ignore_index=True)

# Usage
# input_path = 'your_folder_with_tdwbx_files'
# output_path = 'where_to_save_csv_files'
# analyzer = DashboardAnalyzer(input_path, output_path, create_dir=False)
# df = analyzer.analyze(return_concat=True)
# if df is not None:
#     print(df)
