import streamlit as st
import google.generativeai as genai
import time
import urllib.parse

# 1. Page Setup
st.set_page_config(page_title="MaiRuknaNahiChahta", layout="centered")
st.title("🗺️ Main Rukna Nahi Chahta")
st.write("*Main udna chahta hoon, daudna chahta hoon... bus rukna nahi chahta.* Get your hyper-optimized, fluff-free itinerary.")

# Configure AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

st.markdown("---")

# 2. The Core Parameters (Low Cognitive Load)
destination = st.text_input("📍 Where are you going?", placeholder="e.g., Diu, Lucknow, Surat")

col1, col2 = st.columns(2)
with col1:
    days = st.number_input("🗓️ Number of days?", min_value=1, max_value=30, value=2)
    pace = st.select_slider(
        "⚡ Travel Pace?", 
        options=["Slow & Relaxed", "Balanced", "Optimized Pro Max"], 
        value="Balanced"
    )

with col2:
    people = st.selectbox("👥 Who is traveling?", ["Solo", "Couple", "3-5 Friends", "Large Group/Family"])

# 3. Progressive Disclosure (The Advanced Dropdown)
with st.expander("✨ Advanced Preferences (Optional)"):
    theme = st.selectbox("Trip Theme?", ["Mix of Everything", "Adventure & Outdoors", "Sightseeing & Monuments", "Art, Culture & Museums", "Nomadic / Fast-Paced"])
    diet = st.selectbox("Food Preference?", ["Anything", "Strictly Veg", "Non-Veg"])
    elements = st.multiselect(
        "Must-Have Elements:", 
        ["Temples & Spiritual", "Local Shopping/Markets", "Cafes & Chill", "Historical Ruins", "Street Food Hopping", "Beaches/Nature"],
        help="Leave blank to let the AI decide the best mix."
    )

st.markdown("---")

# 4. Dynamic Button Microcopy
button_text = f"Draft My {destination.title()} Itinerary 🚀" if destination else "Draft My Itinerary 🚀"

if st.button(button_text, use_container_width=True):
    if destination:
        with st.spinner(f"Cooking up a {theme} trip to {destination}..."):
            
            elements_str = ", ".join(elements) if elements else "A balanced mix of the city's best offerings."
            
            # The V2 System Prompt
            prompt = f"""
            You are an elite, highly opinionated local travel expert. 
            Create a hyper-optimized itinerary for {destination}.
            
            PARAMETERS:
            - Duration: {days} days
            - Group: {people}
            - Diet: {diet} (If strictly veg, NEVER suggest meat spots).
            - Pacing: {pace}
            - Theme: {theme}
            - Must-Include Elements: {elements_str}

            YOUR CORE RULES:
            1. THE GRID FORMAT: You MUST output the daily itinerary strictly as a Markdown Table. The columns MUST be: | Time | Location | Action | Why it's A1 |. Do NOT use linear bullet points for the timeline.
            2. LOGISTICS FIRST: Group locations geographically. Account for travel time.
            3. NO FLUFF: Name specific dishes, specific cafes, and specific transport methods.
            
            THE "FOMO" EXCEPTION RULE:
            If the user did NOT select "Museums" or "Temples", but {destination} has a globally or nationally recognized 'Must Visit' landmark that defines the city (e.g., Bharat Bhavan in Bhopal, Laxmi Vilas Palace in Vadodara), you MUST include it anyway. Add a small note in the 'Why' column explaining that this is a "Must-Do Exception".

            THE CLOSURE WARNINGS (DAY-CHECKS):
            Because you do not know the exact dates the user is traveling, you MUST include a section at the very bottom titled "⚠️ **Crucial Day-Checks**". List the known closed days for ANY location you suggested in the table (e.g., "Note: The Tribal Museum is closed on Mondays"). If everything suggested is open 7 days a week, state that clearly.

            Now, generate the final itinerary.
            """
            
            try:
                response = model.generate_content(prompt)
                itinerary_text = response.text
                
                st.markdown(itinerary_text)
                
                st.markdown("---")
                st.subheader("📲 Save & Share")
                
                safe_markdown = itinerary_text.replace('`', '\\`').replace('\n', '\\n')
                html_file = f"""<!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>{destination} Itinerary</title>
                    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
                    <style>
                        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; line-height: 1.6; color: #333; }}
                        table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; font-size: 14px; }}
                        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                        th {{ background-color: #f8f9fa; font-weight: bold; }}
                        h1, h2, h3 {{ border-bottom: 2px solid #eee; padding-bottom: 5px; }}
                        .print-btn {{ display: block; margin: 20px 0; padding: 10px 20px; background: #000; color: #fff; text-align: center; text-decoration: none; border-radius: 5px; font-weight: bold; cursor: pointer; }}
                        @media print {{ .print-btn {{ display: none; }} }}
                    </style>
                </head>
                <body>
                    <button class="print-btn" onclick="window.print()">🖨️ Save as PDF / Print</button>
                    <div id="content"></div>
                    <script>
                        document.getElementById('content').innerHTML = marked.parse(`{safe_markdown}`);
                    </script>
                </body>
                </html>
                """
                
                colA, colB = st.columns(2)
                
                with colA:
                    st.download_button(
                        label="📥 Download Itinerary",
                        data=html_file,
                        file_name=f"{destination}_Pro_Max_Itinerary.html",
                        mime="text/html",
                        use_container_width=True
                    )
                
                with colB:
                    app_url = "https://trip-planner-s5cpbw5whcactta7xgdtxd.streamlit.app/"
                    whatsapp_msg = urllib.parse.quote(f"Check out this AI Trip Planner that built my {destination} itinerary! 🚀 {app_url}")
                    st.markdown(f"[![Share on WhatsApp](https://img.shields.io/badge/Share_App_on-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)]({f'https://wa.me/?text={whatsapp_msg}'})", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.error("Please enter a destination first!")