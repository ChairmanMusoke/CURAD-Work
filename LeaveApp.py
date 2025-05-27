import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('your_credentials.json', scope)
client = gspread.authorize(credentials)

# Open your Google Sheet
sheet = client.open("Leave_Applications").worksheet("Sheet1")  # Adjust the name

# Streamlit form
st.title("Leave Application Form")

with st.form("leave_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    department = st.text_input("Department")
    leave_type = st.selectbox("Type of Leave", ["Annual", "Sick", "Maternity", "Paternity", "Other"])
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    reason = st.text_area("Reason for Leave")
    submit = st.form_submit_button("Submit Application")

    if submit:
        application_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([application_date, name, department, leave_type, str(start_date), str(end_date), reason, "Pending Supervisor Approval", "Pending HR Confirmation"])
        st.success("Your leave application has been submitted!")

