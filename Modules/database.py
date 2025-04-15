import pandas as pd  
import os  
from datetime import datetime  
  
class Database:  
    def __init__(self, data_file="data/overtime_data.csv"):  
        self.data_file = data_file  
        self.initialize_db()  
      
    def initialize_db(self):  
        if not os.path.exists("data"):  
            os.makedirs("data")  
              
        if not os.path.exists(self.data_file):  
            df_init = pd.DataFrame(columns=[  
                "Date", "ID", "Name", "Designation", "Status",  
                "Scheduling_OT", "OCC_OT", "Training_OT", "OPS_OT",   
                "Approved_By", "Total_OT", "Entry_Timestamp"  
            ])  
            df_init.to_csv(self.data_file, index=False)  
      
    def load_data(self):  
        return pd.read_csv(self.data_file, parse_dates=["Date"])  
      
    def save_data(self, df):  
        df.to_csv(self.data_file, index=False)  
      
    def add_entry(self, entry_data):  
        df = self.load_data()  
        entry_data["Entry_Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        df = pd.concat([df, pd.DataFrame([entry_data])], ignore_index=True)  
        self.save_data(df)  
        return True  
