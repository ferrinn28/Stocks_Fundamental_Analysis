import pandas as pd

class ExcelWriter():
    def __init__(self, path, fundamental_data):
        self.path = path
        self.fundamental_data = fundamental_data

    def create_report(self):
        file_name = f"{self.fundamental_data['Date']}-{self.fundamental_data['Code']}-{self.fundamental_data['Type Report']}.xlsx"
        pd.options.display.float_format = '{:.2f}'.format
        df_fundamental = pd.DataFrame(self.fundamental_data)

        # Create a Excel File
        df_fundamental.to_excel(excel_writer=f"{self.path}\\{file_name}", 
                                sheet_name='Fundamental Data')
        
        print(f"Report is Created in {self.path}\\{file_name}")