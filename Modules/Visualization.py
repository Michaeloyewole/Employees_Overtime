import plotly.express as px  
import plotly.graph_objects as go  
import pandas as pd  
  
class Visualization:  
    @staticmethod  
    def create_overtime_summary(df):  
        if df.empty:  
            return None  
          
        summary = df.groupby(["Name", "Designation"]).agg({  
            "Scheduling_OT": "sum",  
            "OCC_OT": "sum",  
            "Training_OT": "sum",  
            "OPS_OT": "sum",  
            "Total_OT": "sum"  
        }).reset_index()  
          
        return summary  
      
    @staticmethod  
    def create_department_chart(df):  
        if df.empty:  
            return None  
              
        fig = px.bar(  
            df,  
            x="Name",  
            y=["Scheduling_OT", "OCC_OT", "Training_OT", "OPS_OT"],  
            title="Overtime by Department",  
            labels={"value": "Hours", "variable": "Department"},  
            barmode="group"  
        )  
        return fig  
      
    @staticmethod  
    def create_trend_chart(df):  
        if df.empty:  
            return None  
              
        daily_total = df.groupby("Date")["Total_OT"].sum().reset_index()  
        fig = px.line(  
            daily_total,  
            x="Date",  
            y="Total_OT",  
            title="Daily Overtime Trend",  
            labels={"Total_OT": "Total Hours", "Date": "Date"}  
        )  
        return fig  
