# Resume-Synthesizer: AI-Powered Resume and Cover Letter Builder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Streamlit](https://img.shields.io/badge/Streamlit-v1.30.0+-orange)](https://streamlit.io/)

## Overview

Resume-Builder is an AI-driven application designed to help job seekers craft compelling, tailored resumes and cover letters. By leveraging the power of the Google Gemini API, this tool analyzes job descriptions and your existing resume to generate optimized documents that highlight your most relevant skills and experiences. It's built with Streamlit, providing an intuitive and interactive user interface.

## Key Features

*   **Resume Tailoring:**
    *   Paste your existing resume text into the application.
    *   Input the job description for the position you're targeting.
    *   The AI analyzes the job description and identifies the top 10 most critical skills.
    *   Select 3-6 skills to emphasize in your tailored resume.
    *   The AI generates a customized resume that highlights the selected skills, optimizes for Applicant Tracking Systems (ATS), and includes relevant keywords.
    *   Download your tailored resume as a PDF file.
*   **Cover Letter Generation:**
    *   Paste your existing resume text.
    *   Input the job description.
    *   Enter the company name and recipient's name (if known).
    *   The AI analyzes the job description and identifies the top 10 most critical skills.
    *   Select 3-6 skills to emphasize in your tailored cover letter.
    *   The AI generates a customized cover letter that highlights the selected skills, is tailored to the company and recipient, and includes relevant keywords.
    *   Download your tailored cover letter as a PDF file.
*   **AI-Powered Content Generation:**
    *   Utilizes the Google Gemini API to generate high-quality, contextually relevant content.
    *   Employs advanced natural language processing to understand job requirements and match them to your skills.
*   **Skill Extraction:**
    *   Automatically extracts key skills from job descriptions.
    *   Ranks skills by importance to help you prioritize.
*   **ATS Optimization:**
    *   The AI-generated resumes are designed to be compatible with Applicant Tracking Systems (ATS).
    *   Includes keyword optimization, standardized formatting, and bullet point normalization.
*   **User-Friendly Interface:**
    *   Built with Streamlit for an intuitive and interactive experience.
    *   Clear step-by-step guidance throughout the process.
*   **Error Handling:**
    *   Robust error handling to gracefully manage issues like API failures and invalid inputs.
*   **Logging:**
    *   Comprehensive logging for debugging and monitoring.
* **Pro Tips:**
    *   Provides helpful tips for reviewing and finalizing your resume and cover letter.

## Technologies Used

*   **Python:** The core programming language.
*   **Streamlit:** For building the interactive web application.
*   **Google Gemini API:** For AI-powered content generation and analysis.
*   **python-dotenv:** For managing environment variables.
*   **fpdf:** For generating PDF files.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**

    *   Create a `.env` file in the root directory of the project.
    *   Add your Google Gemini API key to the `.env` file:

        ```
        GOOGLE_API_KEY=YOUR_API_KEY_HERE
        ```

## Usage

1.  **Run the Streamlit application:**

    ```bash
    streamlit run main.py
    ```

2.  **Open the application in your browser:**

    *   The application will typically be available at `http://localhost:8501`.

3.  **Follow the on-screen instructions:**

    *   **Resume Builder Tab:**
        *   Paste your existing resume text.
        *   Paste the job description.
        *   Click "Analyze Job Requirements."
        *   Select 3-6 skills to emphasize.
        *   Click "Generate Tailored Resume."
        *   Review and download your tailored resume.
    *   **Cover Letter Builder Tab:**
        *   Paste your existing resume text.
        *   Paste the job description.
        *   Enter the company name and recipient's name.
        *   Click "Analyze Job Requirements for Cover Letter."
        *   Select 3-6 skills to emphasize.
        *   Click "Generate Tailored Cover Letter."
        *   Review and download your tailored cover letter.

## Contributing

Contributions are welcome! Please feel free to submit pull requests, open issues, or suggest new features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application uses AI to generate resume and cover letter content. While the AI is trained to provide helpful suggestions, it's essential to review and edit the generated content to ensure accuracy and relevance to your specific situation.
