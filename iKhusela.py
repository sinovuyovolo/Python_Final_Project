import streamlit as st
import json
import time
import random
from datetime import datetime
import requests
import google.generativeai as genai

# Configure the page
st.set_page_config(
    page_title="iKhuselo",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configure Gemini API
genai.configure(api_key="AIzaSyBizEFQuk2ZBsOk4WmNM60D2vbgjLolNwc")

# Custom CSS for styling
def local_css():
    st.markdown("""
    <style>
    /* Main styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Calculator styling */
    .calculator {
        background-color: #2c3e50;
        border-radius: 10px;
        padding: 20px;
        width: 300px;
        margin: 0 auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .calculator-display {
        background-color: #1a252f;
        color: white;
        font-size: 24px;
        text-align: right;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }
    
    .calculator-button {
        width: 60px;
        height: 60px;
        font-size: 18px;
        margin: 5px;
        border: none;
        border-radius: 5px;
        background-color: #34495e;
        color: white;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .calculator-button:hover {
        background-color: #4a6572;
    }
    
    .calculator-button.operator {
        background-color: #e74c3c;
    }
    
    .calculator-button.operator:hover {
        background-color: #c0392b;
    }
    
    .calculator-button.equals {
        background-color: #2ecc71;
        width: 130px;
    }
    
    .calculator-button.equals:hover {
        background-color: #27ae60;
    }
    
    /* SOS Button */
    .sos-button {
        background-color: #e74c3c;
        color: white;
        border: none;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        font-size: 24px;
        font-weight: bold;
        margin: 20px auto;
        display: block;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .sos-button:hover {
        background-color: #c0392b;
        transform: scale(1.05);
    }
    
    /* Dashboard cards */
    .dashboard-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Chat messages */
    .user-message {
        background-color: #3498db;
        color: white;
        border-radius: 18px 18px 0 18px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 80%;
        margin-left: auto;
    }
    
    .bot-message {
        background-color: #ecf0f1;
        color: #2c3e50;
        border-radius: 18px 18px 18px 0;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 80%;
    }
    
    /* Emergency contacts */
    .contact-card {
        background-color: #f8f9fa;
        border-left: 4px solid #3498db;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 5px 5px 0;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .calculator {
            width: 90%;
            max-width: 300px;
        }
        
        .sos-button {
            width: 100px;
            height: 100px;
            font-size: 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'pin' not in st.session_state:
        st.session_state.pin = ""
    if 'calculator_display' not in st.session_state:
        st.session_state.calculator_display = "0"
    if 'user_name' not in st.session_state:
        st.session_state.user_name = "User"
    if 'language' not in st.session_state:
        st.session_state.language = "English"
    if 'theme' not in st.session_state:
        st.session_state.theme = "light"
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'wellness_check' not in st.session_state:
        st.session_state.wellness_check = ""
    if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = []
    if 'date_safety_timer' not in st.session_state:
        st.session_state.date_safety_timer = None
    if 'personal_info' not in st.session_state:
        st.session_state.personal_info = {
            "full_name": "",
            "age": "",
            "address": "",
            "allergies": "",
            "blood_type": "",
            "emergency_contacts": ""
        }
    if 'sos_triggered' not in st.session_state:
        st.session_state.sos_triggered = False
    if 'anonymous_reports' not in st.session_state:
        st.session_state.anonymous_reports = []

# Language translations
def get_translations(language):
    translations = {
        "English": {
            "app_name": "iKhuselo",
            "welcome": "Welcome to iKhuselo",
            "subtitle": "Your Digital Shield Against GBV",
            "wellness_check": "How are you feeling today?",
            "safe": "Safe",
            "uneasy": "Uneasy",
            "in_danger": "In Danger",
            "sos_button": "SOS",
            "sos_confirm": "Are you sure? This will contact emergency services.",
            "yes": "Yes",
            "no": "No",
            "emergency_contacts": "Emergency Contacts",
            "date_safety": "Date Safety",
            "journal": "Private Journal",
            "sign_language": "Sign Language Support",
            "personal_info": "Personal Information",
            "anonymous_reporting": "Anonymous Reporting",
            "chat_with_ai": "Chat with our AI Assistant",
            "type_message": "Type your message...",
            "send": "Send",
            "name": "Name",
            "age": "Age",
            "address": "Address",
            "allergies": "Allergies",
            "blood_type": "Blood Type",
            "emergency_contacts_field": "Emergency Contacts",
            "save": "Save",
            "date_name": "Person's Name",
            "date_contact": "Contact Number",
            "date_location": "Meeting Location",
            "date_timer": "Set Timer (hours)",
            "start_timer": "Start Safety Timer",
            "cancel_timer": "Cancel Timer",
            "new_journal_entry": "New Journal Entry",
            "add_entry": "Add Entry",
            "report_incident": "Report Incident Anonymously",
            "incident_details": "Incident Details",
            "submit_report": "Submit Report",
            "sign_language_help": "Help",
            "sign_language_danger": "Danger",
            "sign_language_police": "Police",
            "sign_language_medical": "Medical Help",
            "logout": "Logout"
        },
        "isiZulu": {
            "app_name": "iKhuselo",
            "welcome": "Siyakwamukela ku-iKhuselo",
            "subtitle": "Isihlangu Sakho Sedijithali Sokulwa Ne-GBV",
            "wellness_check": "Uzizwa kanjani namuhla?",
            "safe": "Uvikelekile",
            "uneasy": "Ungakhululeki",
            "in_danger": "Usengozini",
            "sos_button": "SOS",
            "sos_confirm": "Uqinisekile? Lokhu kuzoxhumana nezinsizakubhekele ezingozi.",
            "yes": "Yebo",
            "no": "Cha",
            "emergency_contacts": "Izindlela Zokuxhumana Ezingozi",
            "date_safety": "Ukuphepha Kosuku",
            "journal": "Ijinali Yangasese",
            "sign_language": "Ukusekelwa Kolimi Lwezandla",
            "personal_info": "Ulwazi Lomuntu Siqu",
            "anonymous_reporting": "Ukubika Ngokungaziwa",
            "chat_with_ai": "Xoxa Ne-AI Assistant Yethu",
            "type_message": "Faka umlayezo wakho...",
            "send": "Thumela",
            "name": "Igama",
            "age": "Iminyaka",
            "address": "Ikheli",
            "allergies": "Izinto Ozizwayo",
            "blood_type": "Uhlobo Lwegazi",
            "emergency_contacts_field": "Izindlela Zokuxhumana Ezingozi",
            "save": "Londoloza",
            "date_name": "Igama Lomuntu",
            "date_contact": "Inombolo Yocingo",
            "date_location": "Indawo Yokuhlangana",
            "date_timer": "Setha Isikhathi (amahora)",
            "start_timer": "Qala Isikhathi Sokuphepha",
            "cancel_timer": "Khansela Isikhathi",
            "new_journal_entry": "Okungeniselwe Okusha Kwijinali",
            "add_entry": "Faka Okungeniselwe",
            "report_incident": "Bika Isigameko Ngokungaziwa",
            "incident_details": "Imininingwane Yesigameko",
            "submit_report": "Thumela Umbiko",
            "sign_language_help": "Usizo",
            "sign_language_danger": "Ingozi",
            "sign_language_police": "Amaphoyisa",
            "sign_language_medical": "Usizo Lwezokwelapha",
            "logout": "Phuma"
        },
        "isiXhosa": {
            "app_name": "iKhuselo",
            "welcome": "Wamkelekile kwi-iKhuselo",
            "subtitle": "Isihlangu Sakho SeDigital Sokulwa Ne-GBV",
            "wellness_check": "Uziva njani namhlanje?",
            "safe": "Ukhuselekile",
            "uneasy": "Akukho nto ikukhululekileyo",
            "in_danger": "Usesichengeni",
            "sos_button": "SOS",
            "sos_confirm": "Uqinisekile? Oku kuya kudibana neenkonzo ezingozi.",
            "yes": "Ewe",
            "no": "Hayi",
            "emergency_contacts": "Iindidi Zonxibelelwano Ezingozi",
            "date_safety": "Ukhuselo Lwexesha Lokudibana",
            "journal": "Iincwadi Zangasese",
            "sign_language": "Inkxaso Yolwimi Lwezandla",
            "personal_info": "Inkcazelo Yomntu",
            "anonymous_reporting": "Ukuxela Ngaphandle Kokwaziswa",
            "chat_with_ai": "Thetha Ne-AI Assistant Yethu",
            "type_message": "Chwetheza umyalezo wakho...",
            "send": "Thumela",
            "name": "Igama",
            "age": "Iminyaka",
            "address": "Idilesi",
            "allergies": "Izinto Ozithandayo",
            "blood_type": "Uhlobo Lwegazi",
            "emergency_contacts_field": "Iindidi Zonxibelelwano Ezingozi",
            "save": "Gcina",
            "date_name": "Igama Lomntu",
            "date_contact": "Inombolo Yomnxeba",
            "date_location": "Indawo Yokudibana",
            "date_timer": "Cwangcisa Ixesha (iiyure)",
            "start_timer": "Qala Ixesha Lokhuseleko",
            "cancel_timer": "Rhoxisa Ixesha",
            "new_journal_entry": "Ingeniso Entsha Kwiincwadi",
            "add_entry": "Yongeza Ingeniso",
            "report_incident": "Xela Isiganeko Ngaphandle Kokwaziswa",
            "incident_details": "Iinkcukacha Zesiganeko",
            "submit_report": "Thumela Ingxelo",
            "sign_language_help": "Uncedo",
            "sign_language_danger": "Ingozi",
            "sign_language_police": "Amapolisa",
            "sign_language_medical": "Uncedo Lwezempilo",
            "logout": "Phuma"
        }
    }
    
    return translations.get(language, translations["English"])

# Calculator component for discreet entry
def calculator_component():
    st.markdown("<h2 style='text-align: center;'>Calculator</h2>", unsafe_allow_html=True)
    
    # Calculator display
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<div class='calculator-display'>{st.session_state.calculator_display}</div>", unsafe_allow_html=True)
        
        # Calculator buttons
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', 'C', '=', '+']
        ]
        
        for row in buttons:
            cols = st.columns(4)
            for i, button in enumerate(row):
                with cols[i]:
                    if st.button(button, key=f"calc_{button}", use_container_width=True):
                        handle_calculator_input(button)

# Handle calculator input
def handle_calculator_input(button):
    if button == 'C':
        st.session_state.calculator_display = "0"
    elif button == '=':
        # Check if the display contains the secret PIN (1234*) followed by =
        if "1234*=" in st.session_state.calculator_display:
            st.session_state.authenticated = True
            st.session_state.calculator_display = "0"
            st.rerun()
        else:
            # For demo purposes, just show a random result
            try:
                # Remove the = for evaluation
                expression = st.session_state.calculator_display.replace('=', '')
                result = eval(expression)
                st.session_state.calculator_display = str(result)
            except:
                st.session_state.calculator_display = "Error"
    else:
        if st.session_state.calculator_display == "0" or st.session_state.calculator_display == "Error":
            st.session_state.calculator_display = button
        else:
            st.session_state.calculator_display += button

# Generate AI response using Gemini API
def generate_ai_response(user_input, language="English"):
    try:
        # Set up the model
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 512,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        # Create context-aware prompt
        prompt_parts = [
            f"You are iKhuselo AI, a compassionate, calm, and reassuring AI assistant for a gender-based violence support app in South Africa. The user is communicating in {language}.",
            "Your role is to be a 'first responder' - empathetic, practical, and safety-focused.",
            "Key guidelines:",
            "1. Always prioritize user safety",
            "2. Be calm and reassuring",
            "3. Ask triage questions if needed: 'Are you in a safe place to talk?', 'Are you in immediate danger?'",
            "4. Provide actionable advice",
            "5. If critical emergency is indicated, state you will alert authorities",
            "6. Keep responses clear and concise",
            "7. Be culturally sensitive to South African context",
            f"User message: {user_input}",
            "Response:"
        ]

        response = model.generate_content(prompt_parts)
        return response.text
        
    except Exception as e:
        return f"I'm here to help, but I'm experiencing technical difficulties. Please try again or use the emergency contacts if you need immediate assistance. Error: {str(e)}"

# Main dashboard
def main_dashboard():
    # Top navigation
    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
    
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/a/af/Flag_of_South_Africa.svg", width=50)
    
    with col2:
        st.markdown(f"<h1 style='text-align: center;'>{get_translations(st.session_state.language)['app_name']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>{get_translations(st.session_state.language)['subtitle']}</p>", unsafe_allow_html=True)
    
    with col3:
        # Language selector
        language = st.selectbox(
            "Language",
            ["English", "isiZulu", "isiXhosa"],
            index=["English", "isiZulu", "isiXhosa"].index(st.session_state.language),
            key="language_selector",
            label_visibility="collapsed"
        )
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()
    
    with col4:
        # Theme toggle and logout
        theme_col, logout_col = st.columns(2)
        with theme_col:
            if st.button("🌙" if st.session_state.theme == "light" else "☀️"):
                st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
                st.rerun()
        with logout_col:
            if st.button("🚪"):
                st.session_state.authenticated = False
                st.session_state.calculator_display = "0"
                st.rerun()
    
    # Personalized greeting
    st.markdown(f"<h2>Hello {st.session_state.user_name}!</h2>", unsafe_allow_html=True)
    
    # Wellness check-in
    st.markdown(f"<h3>{get_translations(st.session_state.language)['wellness_check']}</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(f"😊 {get_translations(st.session_state.language)['safe']}", use_container_width=True):
            st.session_state.wellness_check = "safe"
            st.success("Thank you for checking in. Stay safe!")
    with col2:
        if st.button(f"😟 {get_translations(st.session_state.language)['uneasy']}", use_container_width=True):
            st.session_state.wellness_check = "uneasy"
            st.info("We're here for you. Would you like to chat with our AI assistant?")
    with col3:
        if st.button(f"🚨 {get_translations(st.session_state.language)['in_danger']}", use_container_width=True):
            st.session_state.wellness_check = "in_danger"
            st.error("You've indicated you're in danger. Please use the SOS button if you need immediate help.")
    
    # SOS Button
    st.markdown(f"<div style='text-align: center;'><button class='sos-button'>{get_translations(st.session_state.language)['sos_button']}</button></div>", unsafe_allow_html=True)
    
    # SOS confirmation
    if st.button(get_translations(st.session_state.language)['sos_button'], key="sos_confirm", use_container_width=True):
        st.session_state.sos_triggered = True
    
    if st.session_state.sos_triggered:
        st.error("🚨 EMERGENCY ALERT TRIGGERED!")
        st.info("Police & Ambulance Dispatched to [Your Saved Address]. ETA: 8 Minutes.")
        st.warning("Please stay on the line if possible. Help is on the way.")
        
        if st.button("Cancel Alert (Test Only)"):
            st.session_state.sos_triggered = False
            st.success("Alert cancelled. This is only for testing purposes.")
    
    # Dashboard sections
    st.markdown("---")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"## {get_translations(st.session_state.language)['app_name']}")
        selected = st.radio(
            "Navigate to:",
            [
                "AI Assistant", 
                get_translations(st.session_state.language)['emergency_contacts'],
                get_translations(st.session_state.language)['date_safety'],
                get_translations(st.session_state.language)['journal'],
                get_translations(st.session_state.language)['sign_language'],
                get_translations(st.session_state.language)['personal_info'],
                get_translations(st.session_state.language)['anonymous_reporting']
            ]
        )
    
    # Display selected section
    if selected == "AI Assistant":
        ai_chatbot()
    elif selected == get_translations(st.session_state.language)['emergency_contacts']:
        emergency_contacts()
    elif selected == get_translations(st.session_state.language)['date_safety']:
        date_safety()
    elif selected == get_translations(st.session_state.language)['journal']:
        private_journal()
    elif selected == get_translations(st.session_state.language)['sign_language']:
        sign_language_support()
    elif selected == get_translations(st.session_state.language)['personal_info']:
        personal_information()
    elif selected == get_translations(st.session_state.language)['anonymous_reporting']:
        anonymous_reporting()

# AI Chatbot
def ai_chatbot():
    st.markdown(f"<h2>{get_translations(st.session_state.language)['chat_with_ai']}</h2>", unsafe_allow_html=True)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-message'>{message['content']}</div>", unsafe_allow_html=True)
    
    # Input area
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(get_translations(st.session_state.language)['type_message'], key="chat_input", label_visibility="collapsed")
    with col2:
        send_button = st.button(get_translations(st.session_state.language)['send'], use_container_width=True)
    
    if send_button and user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generate AI response using Gemini API
        with st.spinner("Thinking..."):
            ai_response = generate_ai_response(user_input, st.session_state.language)
        
        # Add AI response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
        # Check if this is a critical situation
        if any(keyword in user_input.lower() for keyword in ["emergency", "help now", "danger", "hurt me", "attack"]):
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": "I've detected this may be an emergency. I am now alerting the authorities with your information. Please stay on the line."
            })
            st.session_state.sos_triggered = True
        
        # Rerun to update the chat display
        st.rerun()
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Emergency contacts
def emergency_contacts():
    st.markdown(f"<h2>{get_translations(st.session_state.language)['emergency_contacts']}</h2>", unsafe_allow_html=True)
    
    contacts = [
        {"name": "SAPS (South African Police Service)", "number": "10111"},
        {"name": "GBV Command Centre", "number": "0800 150 150"},
        {"name": "National Ambulance Service", "number": "10177"},
        {"name": "Childline SA", "number": "116"},
        {"name": "Lifeline", "number": "0861 322 322"},
        {"name": "Suicide Crisis Line", "number": "0800 567 567"}
    ]
    
    for contact in contacts:
        with st.container():
            st.markdown(f"<div class='contact-card'><h3>{contact['name']}</h3><p>{contact['number']}</p></div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button(f"📞 Call", key=f"call_{contact['name']}"):
                    st.info(f"Calling {contact['name']} at {contact['number']}... (This is a simulation)")

# Date safety feature
def date_safety():
    st.markdown(f"<h2>{get_translations(st.session_state.language)['date_safety']}</h2>", unsafe_allow_html=True)
    
    with st.form("date_safety_form"):
        date_name = st.text_input(get_translations(st.session_state.language)['date_name'])
        date_contact = st.text_input(get_translations(st.session_state.language)['date_contact'])
        date_location = st.text_input(get_translations(st.session_state.language)['date_location'])
        date_timer = st.number_input(get_translations(st.session_state.language)['date_timer'], min_value=1, max_value=24, value=2)
        
        submitted = st.form_submit_button(get_translations(st.session_state.language)['start_timer'])
        
        if submitted:
            if date_name and date_contact and date_location:
                # Set the timer
                timer_end = datetime.now().timestamp() + (date_timer * 3600)
                st.session_state.date_safety_timer = {
                    "end_time": timer_end,
                    "name": date_name,
                    "contact": date_contact,
                    "location": date_location
                }
                st.success(f"Safety timer set for {date_timer} hours. Remember to cancel it when you're safe!")
            else:
                st.error("Please fill in all fields to set the safety timer.")
    
    # Display active timer
    if st.session_state.date_safety_timer:
        remaining_time = st.session_state.date_safety_timer["end_time"] - datetime.now().timestamp()
        if remaining_time > 0:
            hours = int(remaining_time // 3600)
            minutes = int((remaining_time % 3600) // 60)
            st.info(f"Active safety timer: {hours}h {minutes}m remaining")
            
            if st.button(get_translations(st.session_state.language)['cancel_timer']):
                st.session_state.date_safety_timer = None
                st.success("Safety timer cancelled. We're glad you're safe!")
        else:
            # Timer has expired
            st.error("Safety timer expired! Alert with your location and date details has been sent to your emergency contacts.")
            st.session_state.date_safety_timer = None

# Private journal
def private_journal():
    st.markdown(f"<h2>{get_translations(st.session_state.language)['journal']}</h2>", unsafe_allow_html=True)
    
    # New journal entry
    st.markdown(f"<h3>{get_translations(st.session_state.language)['new_journal_entry']}</h3>", unsafe_allow_html=True)
    new_entry = st.text_area("Write your thoughts here...", height=150, key="new_journal", label_visibility="collapsed")
    
    if st.button(get_translations(st.session_state.language)['add_entry']):
        if new_entry:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.journal_entries.append({
                "timestamp": timestamp,
                "content": new_entry
            })
            st.success("Journal entry added successfully!")
            st.rerun()
        else:
            st.error("Please write something before adding an entry.")
    
    # Display previous entries
    st.markdown("<h3>Previous Entries</h3>", unsafe_allow_html=True)
    for i, entry in enumerate(reversed(st.session_state.journal_entries)):
        with st.expander(f"Entry {len(st.session_state.journal_entries)-i} - {entry['timestamp']}"):
            st.write(entry['content'])
            
            # Simple sentiment analysis (demo)
            if any(word in entry['content'].lower() for word in ['scared', 'afraid', 'hurt', 'danger', 'emergency']):
                st.warning("This entry contains concerning language. Would you like to speak with our AI assistant?")

# Sign language support
def sign_language_support():
    st.markdown(f"<h2>{get_translations(st.session_state.language)['sign_language']}</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <p>These are basic South African Sign Language (SASL) signs that can help you communicate in difficult situations:</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"<h3>{get_translations(st.session_state.language)['sign_language_help']}</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; padding: 20px; background-color: #3498db; color: white; border-radius: 10px;'>
            <h1>🖐️</h1>
            <p>Raise your hand with palm facing out, then move it toward your body.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<h3>{get_translations(st.session_state.language)['sign_language_danger']}</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; padding: 20px; background-color: #e74c3c; color: white; border-radius: 10px;'>
            <h1>✊❌</h1>
            <p>Cross your arms in front of your chest with fists closed.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<h3>{get_translations(st.session_state.language)['sign_language_police']}</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; padding: 20px; background-color: #2ecc71; color: white; border-radius: 10px;'>
            <h1>👮</h1>
            <p>Tap your shoulder where a badge would be.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"<h3>{get_translations(st.session_state.language)['sign_language_medical']}</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; padding: 20px; background-color: #f39c12; color: white; border-radius: 10px;'>
            <h1>❤️</h1>
            <p>Place your hand on your chest over your heart.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Emoji key
    st.markdown("<h3>Emoji Key for Non-Verbal Communication</h3>", unsafe_allow_html=True)
    st.markdown("""
    - 🚨 = "I need the police"
    - 🏥 = "I need medical help"
    - 🏠 = "I need to go home"
    - 📍 = "This is my location"
    - ❤️ = "I'm okay"
    - 😢 = "I'm not okay"
    - 👮 = "Police"
    - 🚑 = "Ambulance"
    - 🔒 = "I feel trapped"
    """)

# Personal information
def personal_information():
    st.markdown(f"<h2>{get_translations(st.session_state.language)['personal_info']}</h2>", unsafe_allow_html=True)
    
    with st.form("personal_info_form"):
        full_name = st.text_input(get_translations(st.session_state.language)['name'], value=st.session_state.personal_info["full_name"])
        age = st.text_input(get_translations(st.session_state.language)['age'], value=st.session_state.personal_info["age"])
        address = st.text_input(get_translations(st.session_state.language)['address'], value=st.session_state.personal_info["address"])
        allergies = st.text_input(get_translations(st.session_state.language)['allergies'], value=st.session_state.personal_info["allergies"])
        blood_type = st.text_input(get_translations(st.session_state.language)['blood_type'], value=st.session_state.personal_info["blood_type"])
        emergency_contacts = st.text_area(get_translations(st.session_state.language)['emergency_contacts_field'], value=st.session_state.personal_info["emergency_contacts"])
        
        submitted = st.form_submit_button(get_translations(st.session_state.language)['save'])
        
        if submitted:
            st.session_state.personal_info = {
                "full_name": full_name,
                "age": age,
                "address": address,
                "allergies": allergies,
                "blood_type": blood_type,
                "emergency_contacts": emergency_contacts
            }
            st
