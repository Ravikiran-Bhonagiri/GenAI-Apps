# Personalized Nutrition Planner

## Overview

The Personalized Nutrition Planner is a web application designed to generate customized one-week meal plans based on user-specific information. It leverages the power of the Gemini API (a large language model) to create nutritionally balanced and tailored meal plans, taking into account factors like dietary restrictions, health conditions, activity levels, and personal preferences.

## Features

*   **Personalized Meal Plans:** Generates one-week meal plans tailored to individual needs and goals.
*   **Comprehensive User Input:** Collects detailed information about the user, including:
    *   Basic demographics (age, gender, height, weight).
    *   Activity level and primary nutrition goals.
    *   Dietary preferences and restrictions (vegetarian, vegan, gluten-free, etc.).
    *   Health conditions (diabetes, high blood pressure, high cholesterol, pregnancy, breastfeeding).
    *   Time availability and resources for meal preparation.
    *   Allergies and medications.
*   **Gemini API Integration:** Uses the Gemini API to generate meal plans based on the provided prompt.
*   **Formatted Output:** Displays the generated meal plan in a clear and readable format using Markdown.
*   **PDF Download:** Allows users to download their personalized meal plan as a PDF file.
*   **User-Friendly Interface:** Utilizes Streamlit to create an interactive and intuitive web application.
*   **Customizable:** The app's appearance can be customized using CSS.
* **Secure:** The API key is loaded from a `.env` file.
* **Error Handling:** The app has error handling for API requests.
* **Loading Message:** The app displays a loading message while the meal plan is being generated.

## Technologies Used

*   **Python:** The primary programming language.
*   **Streamlit:** For building the interactive web application.
*   **Google AI Gemini API:** For generating the meal plans.
*   **python-dotenv:** For managing environment variables (API key).
*   **fpdf:** For generating PDF files.
*   **base64:** For encoding PDF data.

## Setup

1.  **Clone the Repository:**
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd Nutrition-Planner
    ```
2.  **Install Dependencies:**
    ```bash
    pip install streamlit python-dotenv google-generativeai fpdf
    ```
3.  **Get a Gemini API Key:**
    *   Go to Google AI Studio and get an API key.
4.  **Create a `.env` File:**
    *   In the root directory of the project, create a file named `.env`.
    *   Add your API key to the `.env` file:
        ```
        GOOGLE_API_KEY=YOUR_API_KEY
        ```
    *   **Important:** Do not commit the `.env` file to version control. Add `.env` to your `.gitignore` file.

## Usage

1.  **Run the App:**
    ```bash
    streamlit run main.py
    ```
2.  **Interact with the App:**
    *   The app will open in your web browser.
    *   Fill out the form in the sidebar with your information.
    *   Click the "✨ Generate My Personalized Plan! ✨" button.
    *   The app will generate your meal plan and display it on the screen.
    *   You can download the plan as a PDF using the provided link.

## Code Structure

*   **`main.py`:** Contains the main Streamlit application code, including:
    *   API key configuration.
    *   Model setup.
    *   Input form.
    *   Prompt generation.
    *   API interaction.
    *   Output formatting.
    *   PDF generation.
    *   Custom CSS.

## Disclaimer

The information provided by this nutrition agent is intended for general knowledge and informational purposes only, and does not constitute medical advice. It is essential to consult with a qualified healthcare professional or registered dietitian for any health concerns or before making any decisions related to your health or treatment. The generated meal plans are not a substitute for professional medical or dietary advice. If you have specific health conditions, allergies, or are taking medications, please consult with your doctor or a registered dietitian to ensure the meal plan is appropriate for you. If you have diabetes, high blood pressure, high cholesterol, are pregnant, or are breastfeeding, it is especially important to consult with your doctor or a registered dietitian before making any dietary changes.

## Future Enhancements

*   **More Advanced Meal Planning:** Implement more sophisticated logic for generating meal plans, such as calorie and macronutrient tracking.
*   **Recipe Database:** Integrate a database of recipes to provide more detailed meal suggestions.
*   **User Accounts:** Add user accounts to save and manage multiple meal plans.
*   **Progress Tracking:** Allow users to track their progress and adjust their plans accordingly.
*   **Integration with Fitness Trackers:** Connect with fitness trackers to get more accurate activity data.
*   **More Detailed Dietary Analysis:** Provide more in-depth analysis of the generated meal plans.
* **More Models:** Add more models to the app.

## Contributing

Contributions are welcome! If you have any ideas for improvements or bug fixes, please feel free to open an issue or submit a pull request.

