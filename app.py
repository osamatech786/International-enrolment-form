import streamlit as st
from datetime import datetime, date
from streamlit_drawable_canvas import st_canvas
import json
import pandas as pd

# Load country names from a JSON file
with open("world-countries.json") as file:
    data = json.load(file)
    countries = [entry['name'] for entry in data]
countries = ["Select"] + sorted(countries)


# Initialize session state variables if they do not exist
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.personal_info = ""
    st.session_state.dob = None
    st.session_state.gender = ""
    st.session_state.nationality = ""
    st.session_state.email = ""
    st.session_state.phone = ""
    st.session_state.address = ""
    st.session_state.previous_qualifications = ""
    st.session_state.current_institution = ""
    st.session_state.course = ""
    st.session_state.start_date = None
    st.session_state.learning_mode = ""
    st.session_state.id_document = None
    st.session_state.address_proof = None
    st.session_state.additional_document = None
    st.session_state.learning_preferences = ""
    st.session_state.special_requirements = ""
    st.session_state.emergency_contact = ""
    st.session_state.consent = False
    st.session_state.signature = None  # stoer signature

# Define a function to calculate progress and percentage
def get_progress(step, total_steps=17):
    return int((step / total_steps) * 100)

# Define the total number of steps
total_steps = 17

# Calculate the current progress
progress = get_progress(st.session_state.step, total_steps)

# Display the progress bar and percentage
st.write(f"Progress: {progress}%")
st.progress(progress)

# Define the different steps
if st.session_state.step == 1:
    st.title("WORK IN PROGRESS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    st.title("Caution! Under Development.")
    st.image('danger.png')
    st.title("==============================")

    st.title("WELCOME TO PREVISTA!")
    st.write("""
    At Prevista, we believe in unlocking potential and creating opportunities for lifelong learning.
    Our international CPD and accredited qualifications are designed to empower you with the skills and knowledge needed to excel in your chosen field.
    
    We are excited to have you on board and look forward to supporting your journey towards achieving UK accreditation.
    
    Let's get started with your enrolment process. It's simple and straightforward. Please proceed by filling out the following fields one at a time.
    Click 'Next' to begin your journey with Prevista!
    """)
    if st.button("Next"):
        st.session_state.step = 2
        st.experimental_rerun()

elif st.session_state.step == 2:
    st.title("> 1: Personal Information")
    st.session_state.personal_info = st.text_input("Please enter your full name as it appears on your official documents.")
    if st.button("Next"):
        if st.session_state.personal_info:
            st.session_state.step = 3
            st.experimental_rerun()
        else:
            st.warning("Please enter your full name before proceeding.")

elif st.session_state.step == 3:
    st.title("> 2: Date of Birth")
    st.session_state.dob = st.date_input("Please select your date of birth.", 
                                        min_value=date(1900, 1, 1),  # Minimum selectable date
                                        max_value=date(2025, 12, 31),  # Maximum selectable date
                                        key="date_of_borth",  # Unique key for the widget
                                        help="Choose a date",  # Tooltip text
                                        value=st.session_state.dob or datetime(2000, 1, 1), 
                                        format='DD/MM/YYYY')
    
    if st.button("Next"):
        if st.session_state.dob:
            st.session_state.step = 4
            st.experimental_rerun()
        else:
            st.warning("Please select your date of birth before proceeding.")

elif st.session_state.step == 4:
    st.title("> 3: Gender")
    st.session_state.gender = st.selectbox("Please select your gender.", ["Select", "Male", "Female", "Other"])
    if st.button("Next"):
        if st.session_state.gender != "Select":
            st.session_state.step = 5
            st.experimental_rerun()
        else:
            st.warning("Please select your gender before proceeding.")

elif st.session_state.step == 5:
    st.title("> 4: Nationality")
    
    st.session_state.nationality = st.selectbox("Please select your nationality.", countries)
    if st.button("Next"):
        if st.session_state.nationality != "Select":
            st.session_state.step = 6
            st.experimental_rerun()
        else:
            st.warning("Please select your nationality before proceeding.")

elif st.session_state.step == 6:
    st.title("> 5: Contact Information")
    st.session_state.email = st.text_input("Please enter your email address where we can reach you.")
    st.session_state.phone = st.text_input("Please enter your phone number.")
    st.session_state.address = st.text_area("Please enter your complete mailing address.")
    if st.button("Next"):
        if st.session_state.email and st.session_state.phone and st.session_state.address:
            st.session_state.step = 7
            st.experimental_rerun()
        else:
            st.warning("Please enter all contact information fields before proceeding.")

elif st.session_state.step == 7:
    st.title("> 6: Educational Background")
    st.session_state.previous_qualifications = st.text_area("Please list your previous qualifications.")
    st.session_state.current_institution = st.text_input("Please enter the name of your current educational institution (if applicable).")
    if st.button("Next"):
        if st.session_state.previous_qualifications and st.session_state.current_institution:
            st.session_state.step = 8
            st.experimental_rerun()
        else:
            st.warning("Please list your previous qualifications and current institution before proceeding.")

elif st.session_state.step == 8:
    st.title("> 7: Course Information")
    st.session_state.course = st.selectbox("Please select the course you are interested in.", ["Select", "Course 1", "Course 2", "Course 3"])
    st.session_state.start_date = st.date_input("Please select your preferred start date for the course.", value=st.session_state.start_date or date.today(), format='DD/MM/YYYY')
    st.session_state.learning_mode = st.selectbox("Please select your preferred mode of learning.", ["Select", "Online", "In-Person", "Hybrid"])
    if st.button("Next"):
        if st.session_state.course != "Select" and st.session_state.start_date and st.session_state.learning_mode != "Select":
            st.session_state.step = 9
            st.experimental_rerun()
        else:
            st.warning("Please select your course, preferred start date, and learning mode before proceeding.")

elif st.session_state.step == 9:
    st.title("> 8: Identification Documents")
    st.session_state.id_document = st.file_uploader("Please upload a scan or photo of your passport or ID.", type=["jpg", "png", "pdf", "docx"])
    if st.button("Next"):
        if st.session_state.id_document:
            st.session_state.step = 10
            st.experimental_rerun()
        else:
            st.warning("Please upload your identification document before proceeding.")

elif st.session_state.step == 10:
    st.title("> 9: Proof of Address")
    st.session_state.address_proof = st.file_uploader("Please upload a scan or photo of your proof of address.", type=["jpg", "png", "pdf", "docx"])
    if st.button("Next"):
        if st.session_state.address_proof:
            st.session_state.step = 11
            st.experimental_rerun()
        else:
            st.warning("Please upload your proof of address before proceeding.")

elif st.session_state.step == 11:
    st.title("> 10: Additional Information")
    st.session_state.learning_preferences = st.text_area("Please describe any learning preferences you have.")
    st.session_state.special_requirements = st.text_area("Please let us know if you have any special requirements.")
    st.session_state.emergency_contact = st.text_input("Please provide emergency contact details.")
    st.session_state.consent = st.checkbox("I consent to the collection and processing of my personal data according to Prevista’s privacy policy.")
    
    st.write("[Privacy Policy](#)")  # Replace '#' with actual link to privacy policy

    if st.button("Next"):
        if all([st.session_state.learning_preferences, st.session_state.special_requirements, st.session_state.emergency_contact, st.session_state.consent]):
            st.session_state.step = 12
            st.experimental_rerun()
        else:
            st.warning("Please complete all fields and consent before proceeding.")

elif st.session_state.step == 12:
    st.title("> 11: Signature")
    st.write("Please provide your signature below:")
    canvas_result = st_canvas(
        stroke_width=2,
        stroke_color="black",
        background_color="white",
        update_streamlit=True,
        height=150,
        width=600,
        drawing_mode="freedraw",
        key="signature_canvas"
    )
    st.session_state.signature = canvas_result.image_data
    if st.button("Next"):
        if st.session_state.signature is not None:
            st.session_state.step = 13
            st.experimental_rerun()
        else:
            st.warning("Please provide your signature before proceeding.")

elif st.session_state.step == 13:
    st.title("Final Review")
    st.write("Thank you for providing your details. Please review your information and click 'Submit' to complete your enrolment.")

    st.write(f"**Full Name:** {st.session_state.personal_info}")
    st.write(f"**Date of Birth:** {st.session_state.dob}")
    st.write(f"**Gender:** {st.session_state.gender}")
    st.write(f"**Nationality:** {st.session_state.nationality}")
    st.write(f"**Email:** {st.session_state.email}")
    st.write(f"**Phone:** {st.session_state.phone}")
    st.write(f"**Address:** {st.session_state.address}")
    st.write(f"**Previous Qualifications:** {st.session_state.previous_qualifications}")
    st.write(f"**Current Institution:** {st.session_state.current_institution}")
    st.write(f"**Course Interested In:** {st.session_state.course}")
    st.write(f"**Preferred Start Date:** {st.session_state.start_date}")
    st.write(f"**Learning Mode:** {st.session_state.learning_mode}")
    st.write(f"**Learning Preferences:** {st.session_state.learning_preferences}")
    st.write(f"**Special Requirements:** {st.session_state.special_requirements}")
    st.write(f"**Emergency Contact:** {st.session_state.emergency_contact}")

    if st.session_state.signature is not None:
        st.image(st.session_state.signature, caption="Your Signature")

    if st.button("Submit"):
        st.write("Form submitted successfully!")
        # Reset the form for the next use
        st.session_state.step = 1
        st.session_state.personal_info = ""
        st.session_state.dob = None
        st.session_state.gender = ""
        st.session_state.nationality = ""
        st.session_state.email = ""
        st.session_state.phone = ""
        st.session_state.address = ""
        st.session_state.previous_qualifications = ""
        st.session_state.current_institution = ""
        st.session_state.course = ""
        st.session_state.start_date = None
        st.session_state.learning_mode = ""
        st.session_state.id_document = None
        st.session_state.address_proof = None
        st.session_state.additional_document = None
        st.session_state.learning_preferences = ""
        st.session_state.special_requirements = ""
        st.session_state.emergency_contact = ""
        st.session_state.consent = False
        st.session_state.signature = None  # Clear the signature
else:
    st.write("Form completed. Thank you!")

# streamlit run app.py --server.port 8503
# Dev : https://linkedin.com/in/osamatech786
