import streamlit as st
import datetime
import json

st.set_page_config(
    page_title="SECURO - St. Kitts & Nevis Crime Intel Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ALL BLACK theme
st.markdown("""
<style>
    /* Import Times New Roman font */
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');
    
    /* EVERYTHING BLACK */
    .main, .main .block-container, .stApp, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Times New Roman', serif !important;
    }
    
    /* Sidebar BLACK */
    .css-1d391kg, [data-testid="stSidebar"], .css-1lcbmhc {
        background-color: #000000 !important;
    }
    
    /* Headers WHITE text */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-family: 'Times New Roman', serif !important;
    }
    
    /* Chat messages BLACK */
    .stChatMessage {
        background-color: #000000 !important;
        border: 1px solid #333333 !important;
        font-family: 'Times New Roman', serif !important;
        color: #FFFFFF !important;
    }
    
    /* User messages */
    .stChatMessage[data-testid="user-message"] {
        background-color: #000000 !important;
    }
    
    /* Assistant messages */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #000000 !important;
    }
    
    /* Buttons BLACK with WHITE text */
    .stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
        font-family: 'Times New Roman', serif !important;
        font-weight: bold !important;
    }
    
    .stButton > button:hover {
        background-color: #333333 !important;
        color: #FFFFFF !important;
    }
    
    /* Chat input BLACK */
    .stChatInput > div {
        background-color: #000000 !important;
        border: 1px solid #FFFFFF !important;
    }
    
    .stChatInput input {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Times New Roman', serif !important;
    }
    
    /* Selectbox BLACK */
    .stSelectbox > div > div {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Times New Roman', serif !important;
        border: 1px solid #FFFFFF !important;
    }
    
    /* All text WHITE */
    .stMarkdown, .stText, p, span, div {
        color: #FFFFFF !important;
        font-family: 'Times New Roman', serif !important;
    }
    
    /* Divider WHITE */
    hr {
        border-color: #FFFFFF !important;
    }
    
    /* Footer BLACK */
    .footer {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

class SecuroChatbot:
    def __init__(self):
        self.crime_categories = {
            "violent_crimes": ["homicide", "assault", "robbery", "domestic violence"],
            "property_crimes": ["burglary", "theft", "vandalism", "fraud"],
            "drug_crimes": ["drug possession", "drug trafficking", "drug manufacturing"],
            "traffic_crimes": ["speeding", "drunk driving", "reckless driving"],
            "cyber_crimes": ["online fraud", "identity theft", "cyberbullying"]
        }

        self.safety_tips = {
            "home_security": [
                "Install proper lighting around your property",
                "Use deadbolt locks on all exterior doors",
                "Keep valuable items out of sight from windows",
                "Consider a security system or cameras",
                "Secure all windows with proper locks",
                "Don't advertise expensive purchases on social media"
            ],
            "personal_safety": [
                "Stay aware of your surroundings at all times",
                "Travel in groups when possible, especially at night",
                "Keep emergency contacts readily available",
                "Trust your instincts if something feels wrong",
                "Avoid displaying expensive jewelry or electronics",
                "Stay in well-lit, populated areas when walking alone"
            ],
            "online_safety": [
                "Use strong, unique passwords for all accounts",
                "Enable two-factor authentication where possible",
                "Be cautious about sharing personal information online",
                "Verify the identity of people you meet online",
                "Report suspicious online activity immediately",
                "Keep software and antivirus programs updated"
            ]
        }

        self.crime_trends = {
            "2023": {
                "total_crimes": 1250,
                "violent_crimes": 180,
                "property_crimes": 620,
                "drug_crimes": 280,
                "traffic_crimes": 170,
                "areas_most_affected": ["Basseterre", "Frigate Bay", "Sandy Point"],
                "crime_rate_change": "+5.2%"
            },
            "2024": {
                "total_crimes": 1180,
                "violent_crimes": 165,
                "property_crimes": 590,
                "drug_crimes": 260,
                "traffic_crimes": 165,
                "areas_most_affected": ["Basseterre", "Charlestown", "Dieppe Bay"],
                "crime_rate_change": "-5.6%"
            }
        }

    def get_crime_reporting_info(self):
        return """**How to Report a Crime**

**Emergency:** Call 911 immediately for crimes in progress

**Non-Emergency:** 
• Police Station: (869) 465-2241
• Online: Royal St. Christopher and Nevis Police Force website

**What to Include:**
• Date, time, and location
• Description of incident
• Suspect details (if safe to observe)
• Witness information
• Evidence (photos if safe)

**Anonymous Tips:** Crime Stoppers (869) 465-8474

Remember: Your safety comes first."""

    def get_safety_tips(self, category=None):
        if category and category in self.safety_tips:
            tips = self.safety_tips[category]
            category_name = category.replace('_', ' ').title()
            tip_list = "\n".join([f"• {tip}" for tip in tips])
            return f"**{category_name} Tips**\n\n{tip_list}"
        else:
            all_tips = "**Safety Guide**\n\n"
            for cat, tips in self.safety_tips.items():
                category_name = cat.replace('_', ' ').title()
                all_tips += f"**{category_name}:**\n"
                all_tips += "\n".join([f"• {tip}" for tip in tips]) + "\n\n"
            return all_tips

    def get_crime_trends(self, year="2024"):
        if year in self.crime_trends:
            data = self.crime_trends[year]
            return f"""**Crime Statistics {year}**

**Total Crimes:** {data['total_crimes']:,} ({data.get('crime_rate_change', 'N/A')})

**Breakdown:**
• Violent: {data['violent_crimes']} ({data['violent_crimes']/data['total_crimes']*100:.1f}%)
• Property: {data['property_crimes']} ({data['property_crimes']/data['total_crimes']*100:.1f}%)
• Drug-Related: {data['drug_crimes']} ({data['drug_crimes']/data['total_crimes']*100:.1f}%)
• Traffic: {data.get('traffic_crimes', 'N/A')}

**Most Affected Areas:** {', '.join(data['areas_most_affected'])}

*Source: Royal St. Christopher and Nevis Police Force*"""
        return "Crime data not available for that year. Available: 2023, 2024"

    def get_emergency_info(self):
        return """**Emergency Contacts**

**Immediate Emergency:** 911 (Police, Medical, Fire)

**Non-Emergency Services:**
• Police: (869) 465-2241
• Hospital: (869) 465-2551
• Alexandra Hospital (Nevis): (869) 469-5473

**Specialized:**
• Coast Guard: (869) 465-8482
• Crime Stoppers: (869) 465-8474
• Disaster Management: (869) 466-5100

Save these numbers in your phone."""

    def get_tourist_specific_info(self):
        return """**Tourist Safety**

**General Safety:**
• Stay in established tourist zones
• Use reputable tour operators
• Keep hotel contact information handy

**Transportation:**
• Use licensed taxi services
• Avoid hitchhiking
• Be cautious with vehicle rentals

**Beach Safety:**
• Swim in designated areas only
• Don't leave valuables unattended
• Check weather conditions

**Emergency Contacts:**
• Tourist Police: (869) 465-2241
• Hotel/Resort Security
• Your Embassy/Consulate"""

    def process_user_input(self, user_input):
        user_input_lower = user_input.lower()

        if any(keyword in user_input_lower for keyword in ["report", "reporting", "file report", "how to report"]):
            return self.get_crime_reporting_info()
        
        elif any(keyword in user_input_lower for keyword in ["safety", "tips", "prevention", "protect", "secure"]):
            if "home" in user_input_lower or "house" in user_input_lower:
                return self.get_safety_tips("home_security")
            elif "personal" in user_input_lower or "walking" in user_input_lower:
                return self.get_safety_tips("personal_safety")
            elif any(word in user_input_lower for word in ["online", "cyber", "internet", "digital"]):
                return self.get_safety_tips("online_safety")
            else:
                return self.get_safety_tips()
        
        elif any(keyword in user_input_lower for keyword in ["trends", "statistics", "crime rates", "data", "stats"]):
            if "2023" in user_input_lower:
                return self.get_crime_trends("2023")
            else:
                return self.get_crime_trends("2024")
        
        elif any(keyword in user_input_lower for keyword in ["emergency", "911", "help", "contact", "phone"]):
            return self.get_emergency_info()
        
        elif any(keyword in user_input_lower for keyword in ["tourist", "visitor", "vacation", "travel"]):
            return self.get_tourist_specific_info()
        
        elif any(keyword in user_input_lower for keyword in ["hello", "hi", "hey", "start", "begin"]):
            return """**Welcome to SECURO**

I can help you with:
• Crime reporting procedures
• Safety tips and prevention
• Crime statistics and trends
• Emergency contact information
• Tourist-specific safety advice

What would you like to know?"""
        
        else:
            return """I can help you with:

• Crime reporting procedures
• Safety tips and prevention strategies  
• Crime trends and statistics
• Emergency contact information
• Tourist-specific safety advice

Try asking:
- "How do I report a crime?"
- "What are some safety tips?"
- "Show me crime statistics"
- "What are the emergency numbers?" """


def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to SECURO. I'm your St. Kitts & Nevis Crime Intelligence Assistant. How can I help you stay safe today?"}
        ]
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = SecuroChatbot()
    if "user_type" not in st.session_state:
        st.session_state.user_type = "General Public"


def display_chat_message(message):
    """Display a chat message with proper formatting"""
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def add_message_and_rerun(role, content):
    """Add a message to the session state and rerun the app"""
    st.session_state.messages.append({"role": role, "content": content})
    st.rerun()


def main():
    init_session_state()

    # Header
    st.title("SECURO")
    st.subheader("St. Kitts & Nevis Crime Intelligence Assistant")
    st.markdown("Your connection to crime data, safety strategies, and reporting mechanisms.")
    st.divider()

    chatbot = st.session_state.chatbot

    # Sidebar
    with st.sidebar:
        st.header("User Profile")
        user_type = st.selectbox(
            "I am a:", 
            ["General Public", "Criminologist/Law Enforcement", "Tourist/Visitor"],
            index=["General Public", "Criminologist/Law Enforcement", "Tourist/Visitor"].index(st.session_state.user_type)
        )
        st.session_state.user_type = user_type

        st.divider()
        st.header("Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Emergency", use_container_width=True):
                add_message_and_rerun("assistant", chatbot.get_emergency_info())

            if st.button("Statistics", use_container_width=True):
                add_message_and_rerun("assistant", chatbot.get_crime_trends())

        with col2:
            if st.button("Safety Tips", use_container_width=True):
                add_message_and_rerun("assistant", chatbot.get_safety_tips())

            if st.button("Report Crime", use_container_width=True):
                add_message_and_rerun("assistant", chatbot.get_crime_reporting_info())

        # Tourist-specific button
        if st.session_state.user_type == "Tourist/Visitor":
            if st.button("Tourist Safety", use_container_width=True):
                add_message_and_rerun("assistant", chatbot.get_tourist_specific_info())

        st.divider()
        st.markdown(f"**Current User:** {st.session_state.user_type}")
        
        # Clear chat button
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "Chat cleared. How can I help you stay safe today?"}
            ]
            st.rerun()

    # Main chat interface
    st.header("Chat with SECURO")
    
    # Display chat messages
    for message in st.session_state.messages:
        display_chat_message(message)

    # Chat input
    if prompt := st.chat_input("Ask me about crime reporting, safety tips, statistics, or emergencies..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get bot response
        with st.spinner("SECURO is analyzing..."):
            response = chatbot.process_user_input(prompt)
        
        # Add bot response
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Footer
    st.divider()
    st.markdown("""
    <div class="footer">
    <p style="text-align: center; margin: 0;"><strong>IMPORTANT:</strong> SECURO provides information and guidance only.</p>
    <p style="text-align: center; margin: 5px 0 0 0;"><strong>For real emergencies, always call 911 immediately.</strong></p>
    <p style="text-align: center; margin: 10px 0 0 0; font-size: 12px; opacity: 0.7;">Data sources: Royal St. Christopher and Nevis Police Force | Last updated: 2024</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
