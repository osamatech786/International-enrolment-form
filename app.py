import streamlit as st
from datetime import datetime, date
from streamlit_drawable_canvas import st_canvas
import json
import pandas as pd
from docx import Document
from docx.shared import Inches
import io
from PIL import Image
import numpy as np
import smtplib
from email.message import EmailMessage

files=list()

# Load country names from a JSON file
with open("world-countries.json") as file:
    data = json.load(file)
    countries = [entry['name'] for entry in data]
countries = ["Select"] + sorted(countries)

# Load and process the Excel file
df = pd.read_excel('courses.xlsx', sheet_name=0)
df = df.drop_duplicates(subset=['Category', 'Course Title'])
category_courses = df.groupby('Category')['Course Title'].apply(list).to_dict()
category_courses = df.groupby('Category')['Course Title'].apply(lambda x: sorted(set(x))).to_dict()

def is_signature_drawn(signature):
    # Check if signature is None or an empty numpy array
    if signature is None:
        return False
    # Ensure it is a numpy array and has content
    if isinstance(signature, np.ndarray) and signature.size > 0:
        # Additional check: if the array is not just empty white pixels
        # Assuming white background is [255, 255, 255] in RGB
        if np.all(signature == 255):
            return False
        return True
    return False

# Function to send email with attachments (Handle Local + Uploaded)
def send_email_with_attachments(sender_email, sender_password, receiver_email, subject, body, files, local_file_path=None):
    msg = EmailMessage()
    msg['From'] = sender_email
    msg["To"] = ", ".join(receiver_email)
    msg['Subject'] = subject
    msg.set_content(body)

    # Attach uploaded files
    for uploaded_file in files:
        uploaded_file.seek(0)  # Move to the beginning of the UploadedFile
        msg.add_attachment(uploaded_file.read(), maintype='application', subtype='octet-stream', filename=uploaded_file.name)

    # Attach local file if specified
    if local_file_path:
        with open(local_file_path, 'rb') as f:
            file_data = f.read()
            file_name = local_file_path.split('/')[-1]
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Use the SMTP server for sending the email
    with smtplib.SMTP('smtp.office365.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

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
    st.session_state.front_id_document = None
    st.session_state.back_id_document = None
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
    st.session_state.current_institution = st.text_input("Please enter the name of your current educational institution (if applicable, else put 'none').")
    if st.button("Next"):
        if st.session_state.previous_qualifications and st.session_state.current_institution:
            st.session_state.step = 8
            st.experimental_rerun()
        else:
            st.warning("Please list your previous qualifications and current institution before proceeding.")

elif st.session_state.step == 8:
    st.title("> 7: Course Information")
        
    # Category selection
    categories = ["Select"] + list(category_courses.keys())
    st.session_state.category = st.selectbox("Please select the course category.", categories)
    
    # Dynamically update course options based on the selected category
    if st.session_state.category != "Select":
        courses = category_courses.get(st.session_state.category, [])
    else:
        courses = []
    
    # Store selected courses
    st.session_state.courses = st.multiselect("Please select the courses you are interested in.", courses)
    
    # Date and learning mode input
    st.session_state.start_date = st.date_input("Please select your preferred start date for the course.", value=st.session_state.start_date or date.today(), format='DD/MM/YYYY')
    st.session_state.learning_mode = st.selectbox("Please select your preferred mode of learning.", ["Select", "Online", "In-Person", "Hybrid"])
    
    if st.button("Next"):
        if st.session_state.courses and st.session_state.start_date and st.session_state.learning_mode != "Select":
            st.session_state.step = 9
            st.experimental_rerun()
        else:
            st.warning("Please select your courses, preferred start date, and learning mode before proceeding.")

elif st.session_state.step == 9:
    st.title("> 8: Identification Documents")
    st.text("(*Upload of any 1 document is mandatory)")
    # Upload front and back of the document
    st.session_state.front_id_document = st.file_uploader("Please upload a scan or photo of the front of your passport or ID.", type=["jpg", "png", "pdf", "docx"], key="front")
    if st.session_state.front_id_document is not None:
        files.append(st.session_state.front_id_document)

    st.session_state.back_id_document = st.file_uploader("Please upload a scan or photo of the back of your passport or ID.", type=["jpg", "png", "pdf", "docx"], key="back")
    if st.session_state.back_id_document is not None:
        files.append(st.session_state.back_id_document)
    
    if st.button("Next"):
        if st.session_state.front_id_document or st.session_state.back_id_document:
            st.session_state.step = 10
            st.experimental_rerun()
        else:
            st.warning("Please upload both the front and back of your identification document before proceeding.")

elif st.session_state.step == 10:
    st.title("> 9: Proof of Address")
    st.session_state.address_proof = st.file_uploader("*Please upload a scan or photo of your proof of address.", type=["jpg", "png", "pdf", "docx"])
    if st.session_state.address_proof is not None:
        files.append(st.session_state.address_proof)


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
    
    st.write("[Privacy Policy](https://www.prevista.co.uk/policies)")  # Replace '#' with actual link to privacy policy

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
        if is_signature_drawn(st.session_state.signature):
        # if st.session_state.signature is not None:
            st.session_state.step = 13
            st.experimental_rerun()
        else:
            st.warning("Please provide your signature before proceeding.")

elif st.session_state.step == 13:
    st.title("Final Review")
    st.write("Thank you for providing your details. Please review your information and click 'Submit' to complete your enrolment.")

    st.write(f"**Full Name:** {st.session_state.personal_info}")
    dob = st.session_state.dob.strftime('%d-%m-%Y')
    st.write(f"**Date of Birth:** {dob}")
    st.write(f"**Gender:** {st.session_state.gender}")
    st.write(f"**Nationality:** {st.session_state.nationality}")
    st.write(f"**Email:** {st.session_state.email}")
    st.write(f"**Phone:** {st.session_state.phone}")
    st.write(f"**Address:** {st.session_state.address}")
    st.write(f"**Previous Qualifications:** {st.session_state.previous_qualifications}")
    st.write(f"**Current Institution:** {st.session_state.current_institution}")
    st.write(f"**Course Interested In:** {st.session_state.course}")
    start_date= st.session_state.start_date.strftime('%d-%m-%Y')
    st.write(f"**Preferred Start Date:** {start_date}")
    st.write(f"**Learning Mode:** {st.session_state.learning_mode}")
    st.write(f"**Learning Preferences:** {st.session_state.learning_preferences}")
    st.write(f"**Special Requirements:** {st.session_state.special_requirements}")
    st.write(f"**Emergency Contact:** {st.session_state.emergency_contact}")

    if st.session_state.signature is not None:
        st.image(st.session_state.signature, caption="Your Signature")

    if st.button("Submit"):
        # Create a new Document
        doc = Document()
        doc.add_heading('Enrolment Form Submission', 0)

        # Add form details
        doc.add_paragraph(f'Full Name: {st.session_state.personal_info}')

        dob = st.session_state.dob.strftime('%d-%m-%Y')
        doc.add_paragraph(f'Date of Birth: {dob}')

        doc.add_paragraph(f'Gender: {st.session_state.gender}')
        doc.add_paragraph(f'Nationality: {st.session_state.nationality}')
        doc.add_paragraph(f'Email: {st.session_state.email}')
        doc.add_paragraph(f'Phone: {st.session_state.phone}')
        doc.add_paragraph(f'Address: {st.session_state.address}')
        doc.add_paragraph(f'Previous Qualifications: {st.session_state.previous_qualifications}')
        doc.add_paragraph(f'Current Institution: {st.session_state.current_institution}')
        
        # Add selected courses
        if st.session_state.courses:
            courses_text = ", ".join(st.session_state.courses)
            doc.add_paragraph(f'Course Interested In: {courses_text}')
        else:
            doc.add_paragraph(f'Course Interested In: None')

        start_date= st.session_state.start_date.strftime('%d-%m-%Y')
        doc.add_paragraph(f'Preferred Start Date: {start_date}')

        doc.add_paragraph(f'Learning Mode: {st.session_state.learning_mode}')
        doc.add_paragraph(f'Learning Preferences: {st.session_state.learning_preferences}')
        doc.add_paragraph(f'Special Requirements: {st.session_state.special_requirements}')
        doc.add_paragraph(f'Emergency Contact: {st.session_state.emergency_contact}')
        
        # Save the signature image if available
        if st.session_state.signature is not None:
            # Convert numpy array to PIL image
            image_data = st.session_state.signature
            image = Image.fromarray(image_data.astype(np.uint8))  # Ensure correct data type
            
            # Save the image to an in-memory file
            image_stream = io.BytesIO()
            image.save(image_stream, format='PNG')
            image_stream.seek(0)
            
            # Add image to docx
            doc.add_picture(image_stream, width=Inches(2))
        
        # Save the document
        doc_path = f"Int_Form_Submission_{st.session_state.personal_info}.docx"
        doc.save(doc_path)


        # Email
        # Sender email credentials
        # Credentials: Streamlit host st.secrets
        sender_email = st.secrets["sender_email"]
        sender_password = st.secrets["sender_password"]

        # Credentials: Local env
        # load_dotenv()                                     # uncomment import of this library!
        # sender_email = os.getenv('EMAIL')
        # sender_password = os.getenv('PASSWORD')

        receiver_email = [sender_email, 'mohamedr@prevista.co.uk']
        subject = f"Int_Form_Submission_{st.session_state.personal_info} {date.today()}"
        body = "International Form submitted. Please find attached files."

        # Local file path
        local_file_path = doc_path

        # Send email with attachments
        if files or local_file_path:
            send_email_with_attachments(sender_email, sender_password, receiver_email, subject, body, files, local_file_path)
            st.success("Response sent successfully!")
        else:
            st.warning("Please upload at least one file or specify a local file.")


        # Inform the user
        st.success("Response sent successfully!")



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
        st.session_state.courses = []  # Reset courses
        st.session_state.start_date = None
        st.session_state.learning_mode = ""
        st.session_state.front_id_document = None
        st.session_state.back_id_document = None
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
