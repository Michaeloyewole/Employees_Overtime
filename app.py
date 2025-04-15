import streamlit as st  
import pandas as pd  
import plotly.express as px  
from datetime import datetime  
import os  
  
# Page config  
st.set_page_config(  
    page_title="Employee Overtime Management",  
    layout="wide",  
    initial_sidebar_state="expanded"  
)  
  
# Initialize session state  
if 'data' not in st.session_state:  
    st.session_state.data = pd.DataFrame(  
        columns=[  
            "Date", "ID", "Name", "Designation", "Status",  
            "Scheduling_OT", "OCC_OT", "Training_OT", "OPS_OT",  
            "Approved_By", "Total_OT"  
        ]  
    )  
  
# Data management functions  
def save_data():  
    st.session_state.data.to_csv('overtime_data.csv', index=False)  
  
def load_data():  
    if os.path.exists('overtime_data.csv'):  
        st.session_state.data = pd.read_csv('overtime_data.csv')  
        st.session_state.data['Date'] = pd.to_datetime(st.session_state.data['Date'])  
  
# Load existing data  
load_data()  
  
def overtime_entry_form(department):  
    st.header(f"{department} Overtime Entry")  
      
    with st.form(f"{department}_form"):  
        col1, col2 = st.columns(2)  
          
        with col1:  
            date = st.date_input("Date", value=datetime.today())  
            emp_id = st.text_input("Employee ID")  
            name = st.text_input("Employee Name")  
              
        with col2:  
            designation = st.text_input("Designation")  
            status = st.selectbox("Status", ["Active", "Inactive"])  
            ot_hours = st.number_input("Overtime Hours", min_value=0.0, step=0.5)  
              
        approved_by = st.text_input("Approved By")  
          
        if st.form_submit_button("Submit"):  
            new_entry = {  
                "Date": date,  
                "ID": emp_id,  
                "Name": name,  
                "Designation": designation,  
                "Status": status,  
                "Scheduling_OT": ot_hours if department == "Scheduling" else 0,  
                "OCC_OT": ot_hours if department == "OCC" else 0,  
                "Training_OT": ot_hours if department == "Training" else 0,  
                "OPS_OT": ot_hours if department == "Operations" else 0,  
                "Approved_By": approved_by,  
                "Total_OT": ot_hours  
            }  
              
            st.session_state.data = pd.concat([  
                st.session_state.data,  
                pd.DataFrame([new_entry])  
            ], ignore_index=True)  
              
            save_data()  
            st.success("Overtime entry added successfully!")  
  
def show_dashboard():  
    st.header("Overtime Dashboard")  
      
    if st.session_state.data.empty:  
        st.info("No overtime data available yet.")  
        return  
      
    # Summary metrics  
    col1, col2, col3, col4 = st.columns(4)  
      
    with col1:  
        st.metric("Total Scheduling OT",   
                 f"{st.session_state.data['Scheduling_OT'].sum():.2f} hrs")  
    with col2:  
        st.metric("Total OCC OT",   
                 f"{st.session_state.data['OCC_OT'].sum():.2f} hrs")  
    with col3:  
        st.metric("Total Training OT",   
                 f"{st.session_state.data['Training_OT'].sum():.2f} hrs")  
    with col4:  
        st.metric("Total OPS OT",   
                 f"{st.session_state.data['OPS_OT'].sum():.2f} hrs")  
  
    # Visualization  
    st.subheader("Overtime Distribution by Department")  
    df_melt = st.session_state.data.melt(  
        id_vars=['Name'],  
        value_vars=['Scheduling_OT', 'OCC_OT', 'Training_OT', 'OPS_OT'],  
        var_name='Department',  
        value_name='Hours'  
    )  
      
    fig = px.bar(  
        df_melt,  
        x='Name',  
        y='Hours',  
        color='Department',  
        title='Overtime Hours by Employee and Department',  
        barmode='group'  
    )  
    st.plotly_chart(fig, use_container_width=True)  
  
    # Detailed data view  
    st.subheader("Detailed Records")  
    st.dataframe(  
        st.session_state.data.sort_values('Date', ascending=False),  
        use_container_width=True  
    )  
  
# Sidebar navigation  
st.sidebar.title("Navigation")  
page = st.sidebar.radio(  
    "Select Module",  
    ["Scheduling Overtime", "OCC Overtime", "Training Overtime",   
     "Operations Overtime", "Dashboard"]  
)  
  
# Main content  
if page == "Dashboard":  
    show_dashboard()  
elif page == "Scheduling Overtime":  
    overtime_entry_form("Scheduling")  
elif page == "OCC Overtime":  
    overtime_entry_form("OCC")  
elif page == "Training Overtime":  
    overtime_entry_form("Training")  
elif page == "Operations Overtime":  
    overtime_entry_form("Operations")  
  
# Footer  
st.sidebar.markdown("---")  
st.sidebar.markdown("© 2023 Employee Overtime Management")  
