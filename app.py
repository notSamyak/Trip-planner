import streamlit as st
import google.generativeai as genai

# Configure the API securely using the secrets file
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash') # We use flash for speed

# 1. Page Setup
st.set_page_config(page_title="Trip Optimizer", layout="centered")
st.title("🗺️ Trip Optimizer Pro Max")
st.write("Get a highly actionable, logical, and fluff-free itinerary based on your exact travel style.")

st.markdown("---")

# 2. The 5 Input Parameters
destination = st.text_input("1. Where are you going?", placeholder="e.g., Diu, Lucknow, Surat")

col1, col2 = st.columns(2)

with col1:
    days = st.number_input("2. Number of days?", min_value=1, max_value=30, value=2)
    diet = st.selectbox("3. Food Preference?", ["Strictly Veg", "Non-Veg", "Anything"])

with col2:
    people = st.selectbox("4. Who is traveling?", ["Solo", "Couple", "3-5 Friends", "Large Group/Family"])
    pace = st.select_slider(
        "5. Travel Pace?", 
        options=["Slow & Relaxed", "Balanced", "Optimized Pro Max"], 
        value="Optimized Pro Max"
    )

st.markdown("---")

# 3. The Generate Button
if st.button("Draft My Itinerary 🚀"):
    if destination:
        with st.spinner(f"Cooking up a {pace} trip to {destination}..."):
            
            # This is the "System Prompt" we talked about!
            # The "Master System Prompt"
            prompt = f"""
            You are an elite, highly opinionated local travel expert. Your goal is to create a hyper-optimized, fluff-free itinerary for {destination}.
            
            PARAMETERS:
            - Duration: {days} days
            - Group: {people}
            - Diet: {diet} (If strictly veg, NEVER suggest meat spots. Suggest iconic local vegetarian street food or specific dishes).
            - Pacing: {pace} (If 'Slow & Relaxed', max 2 spots per day with heavy chill time. If 'Optimized Pro Max', pack the day logically from 8 AM to 10 PM, factoring in travel time).

            YOUR CORE RULES (THE "PRO MAX" PHILOSOPHY):
            1. No Boring Sightseeing: Skip standard museums or generic forts unless they offer a unique vibe (e.g., acoustic mazes, high cliffs, blue flag beaches).
            2. Logistics Matter: Group locations geographically. Account for travel time between spots. Factor in group size for transport (e.g., 3 people means auto over scooty).
            3. Food is a Priority: Suggest specific local legendary spots and exactly what to order (e.g., "Basket Chaat at Royal Cafe" or "Cold Cocoa at A-One").

            OUTPUT FORMAT:
            You MUST output the itinerary strictly as a vertical timeline using Markdown formatting. Use exact times. 
            For every single stop, you must include a bullet point titled "Why:" explaining the logic of why it is A1.

            EXAMPLE FORMAT TO FOLLOW:
            ### **DAY 1: SATURDAY (History & Vibes)**
            **10:30 AM • [Location Name]**
            * **Action:** [What to do/What to order]
            * **Why:** [Provide the sharp, logical reason this is on the list]
            
            Now, generate the final itinerary for {destination} following these strict rules.
            """
            
            # Call the API
            response = model.generate_content(prompt)
            
            # Display the result
            st.markdown(response.text)
    else:
        st.error("Please enter a destination first!")