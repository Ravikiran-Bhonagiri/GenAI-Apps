import streamlit as st
import os
from dotenv import load_dotenv
from google import generativeai as genai
from fpdf import FPDF
import base64

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Get the API key from environment variables
if not GOOGLE_API_KEY:
    st.error("Please set the GOOGLE_API_KEY in the .env file.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

def generate_meal_plan(prompt):
    """
    Sends the prompt to the Gemini API and returns the generated meal plan.

    Args:
        prompt (str): The prompt to send to the Gemini API.

    Returns:
        str: The generated meal plan.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def create_download_link(pdf_data, filename):
    """Generates a download link for the PDF."""
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def main():
    """
    Main function to run the Streamlit app for the Personalized Nutrition Agent.
    """
    # --- Custom CSS ---
    st.markdown(
        """
        <style>
        .st-emotion-cache-1v0mbdj {
            background-color: #f0f8ff; /* Light blue background */
        }
        .st-emotion-cache-10oheav {
            color: #000080; /* Dark blue text */
        }
        .st-emotion-cache-1y4p8pa {
            color: #000080; /* Dark blue text */
        }
        .st-emotion-cache-16txtl3 {
            color: #000080; /* Dark blue text */
        }
        .st-emotion-cache-10trblm {
            color: #000080; /* Dark blue text */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- Title and Introduction ---
    st.title("🌟 Your Personalized Nutrition Adventure! 🌟")
    st.write(
        "👋 Welcome to your journey towards a healthier, happier you! "
        "Let's team up to craft a meal plan that's perfectly tailored to your unique needs and goals. "
        "Ready to take the first step? Just share a bit about yourself below!"
    )

    # --- Sidebar for User Input ---
    st.sidebar.header("Tell Us About You!")

    # --- Basic Demographics and Goals ---
    st.sidebar.subheader("Let's Start with the Basics")
    age = st.sidebar.number_input("Your Age (years young!)", min_value=1, max_value=120, value=30)
    gender = st.sidebar.selectbox("Your Gender", ["Male", "Female", "Other"])
    height_cm = st.sidebar.number_input("Your Height (cm)", min_value=50, max_value=250, value=170)
    weight_kg = st.sidebar.number_input("Your Weight (kg)", min_value=30, max_value=200, value=70)
    activity_level = st.sidebar.selectbox(
        "Your Typical Activity Level",
        [
            "Sedentary (mostly sitting, little to no exercise)",
            "Lightly Active (light movement/sports 1-3 days/week)",
            "Moderately Active (moderate exercise/sports 3-5 days/week)",
            "Very Active (hard exercise/sports 6-7 days a week)",
            "Extra Active (intense exercise/sports & physical job)",
        ],
    )
    primary_goal = st.sidebar.selectbox(
        "Your Main Nutrition Goal",
        [
            "Weight Loss (shed some pounds)",
            "Weight Gain (bulk up)",
            "Maintain Weight (stay steady)",
            "Improve General Health (feel better overall)",
            "Build Muscle (get stronger)",
            "Muscle Definition (tone up)",
        ],
    )

    # --- Dietary Preferences and Restrictions ---
    st.sidebar.subheader("Your Food Preferences")
    dietary_restrictions = st.sidebar.multiselect(
        "Any Dietary Restrictions?",
        [
            "Vegetarian",
            "Vegan",
            "Pescatarian",
            "Gluten-Free",
            "Dairy-Free",
            "Nut-Free",
            "Soy-Free",
            "Other",
        ],
    )
    food_preferences = st.sidebar.text_input("Any Favorite Foods or Foods You Dislike?")
    meal_frequency = st.sidebar.selectbox(
        "How Often Do You Like to Eat?", ["3 meals a day", "4-5 smaller meals", "Other"]
    )
    snacking_habits = st.sidebar.selectbox(
        "Do You Enjoy Snacking?", ["I love to snack between meals", "I don't usually snack"]
    )
    time_constraints = st.sidebar.multiselect(
        "Any Time Constraints?",
        [
            "Limited time for breakfast",
            "Need quick lunch options",
            "Love cooking elaborate dinners",
        ],
    )

    # --- Health Conditions and Considerations ---
    st.sidebar.subheader("Your Health in Mind")
    known_allergies = st.sidebar.text_input("Any Known Allergies?")
    medical_conditions = st.sidebar.multiselect(
        "Any Existing Medical Conditions?",
        [
            "Diabetes",
            "High Blood Pressure",
            "High Cholesterol",
            "Pregnancy",
            "Breastfeeding",
            "Other",
        ],
    )

    # --- Diabetes Specifics ---
    diabetes_type = None
    taking_insulin = None
    if "Diabetes" in medical_conditions:
        diabetes_type = st.sidebar.selectbox("Type of Diabetes", ["Type 1", "Type 2", "Gestational", "Other"])
        taking_insulin = st.sidebar.selectbox("Are you taking insulin?", ["Yes", "No"])
        st.sidebar.write("💡 Remember: Please consult with your doctor or a registered dietitian for specific guidance on managing your diabetes.")

    # --- High Blood Pressure Specifics ---
    taking_medication_bp = None
    if "High Blood Pressure" in medical_conditions:
        taking_medication_bp = st.sidebar.selectbox("Are you taking medication for high blood pressure?", ["Yes", "No"])
        st.sidebar.write("💡 Remember: Please consult with your doctor or a registered dietitian for specific guidance on managing your high blood pressure.")

    # --- High Cholesterol Specifics ---
    taking_medication_cholesterol = None
    if "High Cholesterol" in medical_conditions:
        taking_medication_cholesterol = st.sidebar.selectbox("Are you taking medication for high cholesterol?", ["Yes", "No"])
        st.sidebar.write("💡 Remember: Please consult with your doctor or a registered dietitian for specific guidance on managing your high cholesterol.")

    # --- Pregnancy Specifics ---
    pregnancy_trimester = None
    if "Pregnancy" in medical_conditions:
        pregnancy_trimester = st.sidebar.selectbox("Pregnancy Trimester", ["First", "Second", "Third"])
        st.sidebar.write("💡 Remember: Please consult with your doctor or a registered dietitian for specific guidance on managing your diet during pregnancy.")

    # --- Breastfeeding Specifics ---
    breastfeeding_duration = None
    if "Breastfeeding" in medical_conditions:
        breastfeeding_duration = st.sidebar.selectbox("How long have you been breastfeeding?", ["Less than 6 months", "6-12 months", "More than 12 months"])
        st.sidebar.write("💡 Remember: Please consult with your doctor or a registered dietitian for specific guidance on managing your diet while breastfeeding.")

    current_medications = st.sidebar.text_input("Any Current Medications? (optional)")

    # --- Time Availability and Resources ---
    st.sidebar.subheader("Your Time and Resources")
    meal_prep_time = st.sidebar.selectbox(
        "How Much Time Can You Dedicate to Meal Prep?", ["Minimal", "Moderate", "Significant"]
    )
    cooking_skill = st.sidebar.selectbox(
        "Your Cooking Skills Level", ["Beginner", "Intermediate", "Advanced"]
    )
    kitchen_equipment = st.sidebar.multiselect(
        "What Kitchen Equipment Do You Have Access To?", ["Oven", "Microwave", "Blender", "Other"]
    )
    pantry_staples = st.sidebar.selectbox(
        "How's Your Pantry Stocked?", ["I have a well-stocked pantry", "I usually buy fresh ingredients"]
    )

    # --- Submit Button ---
    if st.sidebar.button("✨ Generate My Personalized Plan! ✨"):
        st.write("🚀 Crafting your personalized nutrition plan... just a moment! 🚀")

        # --- Extract Data from Streamlit ---
        user_data = {
            "age": age,
            "gender": gender,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "activity_level": activity_level,
            "primary_goal": primary_goal,
            "dietary_restrictions": dietary_restrictions,
            "food_preferences": food_preferences,
            "meal_frequency": meal_frequency,
            "snacking_habits": snacking_habits,
            "time_constraints": time_constraints,
            "known_allergies": known_allergies,
            "medical_conditions": medical_conditions,
            "diabetes_type": diabetes_type if "Diabetes" in medical_conditions else "N/A",
            "taking_insulin": taking_insulin if "Diabetes" in medical_conditions else "N/A",
            "taking_medication_bp": taking_medication_bp if "High Blood Pressure" in medical_conditions else "N/A",
            "taking_medication_cholesterol": taking_medication_cholesterol if "High Cholesterol" in medical_conditions else "N/A",
            "pregnancy_trimester": pregnancy_trimester if "Pregnancy" in medical_conditions else "N/A",
            "breastfeeding_duration": breastfeeding_duration if "Breastfeeding" in medical_conditions else "N/A",
            "current_medications": current_medications,
            "meal_prep_time": meal_prep_time,
            "cooking_skill": cooking_skill,
            "kitchen_equipment": kitchen_equipment,
            "pantry_staples": pantry_staples,
        }

        # --- Create the Prompt ---
        prompt = f"""
You are a world-class nutritionist, and your task is to create a personalized one-week meal plan for a client.

Client Information:
- Age: {user_data["age"]}
- Gender: {user_data["gender"]}
- Height: {user_data["height_cm"]} cm
- Weight: {user_data["weight_kg"]} kg
- Activity Level: {user_data["activity_level"]}
- Primary Goal: {user_data["primary_goal"]}
- Dietary Restrictions: {user_data["dietary_restrictions"]}
- Food Preferences/Dislikes: {user_data["food_preferences"]}
- Meal Frequency: {user_data["meal_frequency"]}
- Snacking Habits: {user_data["snacking_habits"]}
- Time Constraints: {user_data["time_constraints"]}
- Known Allergies: {user_data["known_allergies"]}
- Medical Conditions: {user_data["medical_conditions"]}
- Diabetes Type: {user_data["diabetes_type"]}
- Taking Insulin: {user_data["taking_insulin"]}
- Taking Medication for High Blood Pressure: {user_data["taking_medication_bp"]}
- Taking Medication for High Cholesterol: {user_data["taking_medication_cholesterol"]}
- Pregnancy Trimester: {user_data["pregnancy_trimester"]}
- Breastfeeding Duration: {user_data["breastfeeding_duration"]}
- Current Medications: {user_data["current_medications"]}
- Meal Prep Time: {user_data["meal_prep_time"]}
- Cooking Skill Level: {user_data["cooking_skill"]}
- Kitchen Equipment: {user_data["kitchen_equipment"]}
- Pantry Staples: {user_data["pantry_staples"]}

Instructions:
1. Create a detailed one-week meal plan that is tailored to the client's specific needs and preferences.
2. Ensure the meal plan is nutritionally balanced and appropriate for the client's medical conditions (if any).
3. Consider the client's dietary restrictions, food preferences/dislikes, and meal frequency.
4. Take into account the client's time constraints, meal prep time, cooking skill level, and available kitchen equipment.
5. If the client has diabetes, ensure the meal plan is appropriate for their diabetes type and insulin use (if applicable).
6. If the client has high blood pressure, ensure the meal plan is appropriate for managing their condition and medication use (if applicable).
7. If the client has high cholesterol, ensure the meal plan is appropriate for managing their condition and medication use (if applicable).
8. If the client is pregnant, ensure the meal plan is appropriate for their trimester.
9. If the client is breastfeeding, ensure the meal plan is appropriate for their breastfeeding duration.
10. Provide a variety of meals and snacks throughout the week.
11. Provide a list of ingredients for each meal.
12. Provide instructions for each meal.

Output Format:
Present the meal plan in a clear, day-by-day format. For each day, list the meals (breakfast, lunch, dinner, snacks) with their corresponding ingredients and instructions.

Example:
Day 1:
Breakfast: Oatmeal with Berries and Nuts
Ingredients: 1/2 cup rolled oats, 1 cup water, 1/4 cup mixed berries, 1 tbsp chopped nuts
Instructions: Cook oatmeal with water. Top with berries and nuts.
Lunch: ...
...
"""

        #st.text_area("Generated Prompt:", value=prompt, height=400)

        # --- Generate Meal Plan using Gemini API ---
        with st.spinner("Generating your personalized meal plan..."):
            meal_plan_text = generate_meal_plan(prompt)

        if meal_plan_text:
            st.write("🎉 Ta-da! Here's your personalized meal plan: 🎉")
            st.markdown(meal_plan_text)

            # --- Create PDF ---
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, meal_plan_text)
            pdf_data = pdf.output(dest="S").encode("latin-1")

            # --- Download Button ---
            st.markdown(create_download_link(pdf_data, "meal_plan.pdf"), unsafe_allow_html=True)
        else:
            st.error("Failed to generate meal plan. Please try again.")

    # --- Disclaimer ---
    st.markdown(
        """
        <div style="text-align: justify;">
        <b>Disclaimer:</b> The information provided by this nutrition agent is intended for general knowledge and informational purposes only, and does not constitute medical advice. It is essential to consult with a qualified healthcare professional or registered dietitian for any health concerns or before making any decisions related to your health or treatment. The generated meal plans are not a substitute for professional medical or dietary advice. If you have specific health conditions, allergies, or are taking medications, please consult with your doctor or a registered dietitian to ensure the meal plan is appropriate for you. <b>If you have diabetes, high blood pressure, high cholesterol, are pregnant, or are breastfeeding, it is especially important to consult with your doctor or a registered dietitian before making any dietary changes.</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
