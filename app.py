import streamlit as st  
import pandas as pd  
from datetime import datetime  
from modules.database import Database  
from modules.visualization import Visualization  
  
# Initialize database  
db = Database()  
viz = Visualization()  
  
# Page configuration  
st.set_page_config(  
    page_title="Employee Overtime Management",  
    page_icon="⏰",  
    layout="wide"  
)  
  
# Custom CSS  
st.markdown("""  
    <style>  
    .main {  
        padding: 20px;  
    }  
    .stButton>button {  
        width: 100%;  
    }  
    .reportview-container {  
        margin: 0;  
    }  
    </style>  
""", unsafe_allow_html=True)  
  
def overtime_form(dept):  
    st.subheader(f"{dept} Overtime Entry")  
      
    with st.form(key=f"{dept}_form"):  
        col1, col2 = st.columns(2)  
          
        with col1:  
            date = st.date_input("Date", value=datetime.today())  
            emp_id = st.text_input("Employee ID")  
            name = st.text_input("Employee Name")  
              
        with col2:  
            designation = st.text_input("Designation")  
            status = st.selectbox("Status", ["Active", "On Leave", "Training"])  
            ot_hours = st.number_input("Overtime Hours", min_value=0.0, step=0.5)  
              
        approved_by = st.text_input("Approved By")  
          
        submit = st.form_submit_button("Submit Entry")  
          
        if submit:  
            if not all([emp_id, name, designation, approved_by]):  
                st.error("Please fill all required fields")  
                return  
                  
            entry_data = {  
                "Date": date,  
                "ID": emp_id,  
                "Name": name,  
                "Designation": designation,  
                "Status": status,  
                "Scheduling_OT": ot_hours if dept == "Scheduling" else 0,  
                "OCC_OT": ot_hours if dept == "OCC" else 0,  
                "Training_OT": ot_hours if dept == "Training" else 0,  
                "OPS_OT": ot_hours if dept == "Operations" else 0,  
                "Approved_By": approved_by,  
                "Total_OT": ot_hours  
            }  
              
            if db.add_entry(entry_data):  
                st.success(f"Overtime entry added for {name}")  
            else:  
                st.error("Error adding entry")  
  
def show_report():  
    st.subheader("Overtime Analysis Dashboard")  
      
    df = db.load_data()  
    if df.empty:  
        st.info("No data available yet.")  
        return  
          
    # Summary metrics  
    col1, col2, col3, col4 = st.columns(4)  
    with col1:  
        st.metric("Total Employees", len(df["ID"].unique()))  
    with col2:  
        st.metric("Total OT Hours", f"{df['Total_OT'].sum():.1f}")  
    with col3:  
        st.metric("Avg. OT/Employee", f"{df.groupby('ID')['Total_OT'].sum().mean():.1f}")  
    with col4:  
        st.metric("Active Departments", len([col for col in df.columns if col.endswith("_OT")]))  
      
    # Charts  
    st.plotly_chart(viz.create_department_chart(df), use_container_width=True)  
    st.plotly_chart(viz.create_trend_chart(df), use_container_width=True)  
      
    # Detailed table  
    st.subheader("Detailed Overtime Records")  
    st.dataframe(  
        df.sort_values("Date", ascending=False),  
        use_container_width=True  
    )  
  
# Main App  
st.title("Employee Overtime Management System")  
  
# Sidebar navigation  
menu = st.sidebar.radio(  
    "Navigation",  
    ["Scheduling Overtime", "OCC Overtime",   
     "Training Overtime", "Operations Overtime",   
     "Overtime Dashboard"]  
)  
  
# Route to appropriate page  
if menu == "Scheduling Overtime":  
    overtime_form("Scheduling")  
elif menu == "OCC Overtime":  
    overtime_form("OCC")  
elif menu == "Training Overtime":  
    overtime_form("Training")  
elif menu == "Operations Overtime":  
    overtime_form("Operations")  
elif menu == "Overtime Dashboard":  
    show_report()  
  
