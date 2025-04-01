import streamlit as st
import os
from dotenv import load_dotenv
from google import generativeai as genai
from fpdf import FPDF
import base64
import re
import logging
from typing import Optional, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Constants
MAX_SKILLS = 10
VALID_FILE_TYPES = ["pdf", "docx", "txt"]
DEFAULT_TEMPERATURE = 0.7

class ResumeBuilder:
    def __init__(self):
        self._configure_gemini()
        
    def _configure_gemini(self) -> None:
        """Configure the Gemini API with settings from environment variables."""
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if not self.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.GOOGLE_API_KEY)
        
        self.generation_config = {
            "temperature": float(os.getenv("MODEL_TEMPERATURE", DEFAULT_TEMPERATURE)),
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 4096,
        }

        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )

    @staticmethod
    def _sanitize_input(text: str) -> str:
        """Basic sanitization of user input."""
        if not text:
            return ""
        return text.strip()

    def _generate_content(self, prompt: str) -> Optional[str]:
        """Handle content generation with error management."""
        try:
            response = self.model.generate_content(prompt)
            if not response.text:
                logger.error("Empty response from Gemini API")
                return None
            return response.text
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            st.error(f"An error occurred while generating content. Please try again.")
            return None

    def extract_skills(self, job_description: str) -> Optional[List[str]]:
        """
        Extract exactly 10 key skills from job description with ranking.
        Returns a list of skills or None if failed.
        """
        sanitized_jd = self._sanitize_input(job_description)
        if not sanitized_jd:
            return None

        prompt = f"""
        Analyze the following job description and extract exactly the top {MAX_SKILLS} most critical skills 
        that candidates must possess, ordered by importance. Focus on:
        
        1. Technical/hard skills specific to the role
        2. Industry-specific knowledge
        3. Key soft skills mentioned
        4. Tools/technologies required
        
        Present ONLY as a numbered list (1-{MAX_SKILLS}) without additional commentary.
        
        Job Description:
        {sanitized_jd}
        """

        result = self._generate_content(prompt)
        if not result:
            return None

        # Parse numbered list into skills
        skills = []
        for line in result.split('\n'):
            match = re.match(r'^\d+\.\s*(.+)$', line.strip())
            if match and len(skills) < MAX_SKILLS:
                skills.append(match.group(1))
        
        return skills if skills else None

    def generate_custom_resume(self, resume: str, job_description: str, selected_skills: List[str]) -> Optional[str]:
        """
        Generate a tailored resume emphasizing selected skills.
        Returns formatted resume text or None if failed.
        """
        if not all([resume, job_description, selected_skills]):
            return None

        prompt = f"""
        Role: Expert Resume Writer specializing in ATS-optimized resumes
        
        Task: Transform this resume to perfectly match the target job by emphasizing these {len(selected_skills)} key skills:
        {", ".join(selected_skills)}
        
        Guidelines:
        1. STRUCTURE: Use standard resume sections (Summary, Skills, Experience, Education)
        2. RELEVANCE: Prioritize experiences demonstrating selected skills
        3. QUANTIFICATION: Add metrics to achievements where possible
        4. KEYWORDS: Mirror language from the job description
        5. CONCISENESS: Keep to 1-2 pages worth of content
        6. FORMATTING: Use clean, professional formatting with bullet points
        
        Original Resume:
        {self._sanitize_input(resume)}
        
        Target Job Description:
        {self._sanitize_input(job_description)}
        
        Generate the optimized resume following these exact sections:
        
        [Professional Summary]
        - 3-4 sentence career overview highlighting top qualifications
        
        [Key Skills]
        - 6-8 bullet points mixing selected skills and job keywords
        
        [Professional Experience]
        - For each role:
          - Company, Job Title, Dates
          - 3-5 bullet points emphasizing relevant achievements
          - Start bullets with strong action verbs
          - Include metrics (%, $, numbers) where possible
        
        [Education]
        - Degree, Institution, Year
        - Relevant coursework if entry-level
        
        [Optional Sections]
        - Certifications, Projects, or Technical Skills if space allows
        """

        return self._generate_content(prompt)
    
    def generate_cover_letter(self, resume: str, job_description: str, selected_skills: List[str], company_name: str, recipient_name: str) -> Optional[str]:
        """
        Generate a tailored cover letter emphasizing selected skills.
        Returns formatted cover letter text or None if failed.
        """
        if not all([resume, job_description, selected_skills, company_name, recipient_name]):
            return None

        prompt = f"""
        Role: Expert Cover Letter Writer specializing in ATS-optimized cover letters
        
        Task: Craft a compelling cover letter to perfectly match the target job by emphasizing these {len(selected_skills)} key skills:
        {", ".join(selected_skills)}
        
        Guidelines:
        1. STRUCTURE: Use standard cover letter format (Introduction, Body, Conclusion)
        2. RELEVANCE: Prioritize experiences demonstrating selected skills
        3. QUANTIFICATION: Add metrics to achievements where possible
        4. KEYWORDS: Mirror language from the job description
        5. CONCISENESS: Keep to 1 page worth of content
        6. FORMATTING: Use clean, professional formatting with paragraphs
        7. PERSONALIZATION: Address the recipient by name and mention the company name
        
        Original Resume:
        {self._sanitize_input(resume)}
        
        Target Job Description:
        {self._sanitize_input(job_description)}
        
        Company Name:
        {self._sanitize_input(company_name)}
        
        Recipient Name:
        {self._sanitize_input(recipient_name)}
        
        Generate the optimized cover letter following these exact sections:
        
        [Introduction]
        - Express enthusiasm for the role and company
        - Briefly introduce yourself and highlight your key qualifications
        
        [Body]
        - 2-3 paragraphs detailing relevant experiences and achievements
        - Emphasize how your skills align with the job requirements
        - Use specific examples and metrics to showcase your impact
        
        [Conclusion]
        - Reiterate your interest and enthusiasm
        - Thank the recipient for their time and consideration
        - Express your eagerness to discuss your application further
        
        """

        return self._generate_content(prompt)

    @staticmethod
    def create_pdf(resume_text: str) -> bytes:
        """Generate PDF from resume text with error handling."""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=11)
            
            # Handle encoding and line breaks
            text = resume_text.encode('latin-1', 'replace').decode('latin-1')
            for line in text.split('\n'):
                pdf.multi_cell(0, 5, line)
                
            return pdf.output(dest="S").encode("latin-1")
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            return None

def create_download_link(file_data: bytes, filename: str) -> str:
    """Create a download link for generated files."""
    b64 = base64.b64encode(file_data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'

def main_ui():
    """Main Streamlit UI implementation."""
    st.set_page_config(
        page_title="AI Resume & Cover Letter Builder", 
        page_icon="📄",
        layout="centered"
    )
    
    # Initialize session state
    if 'skills' not in st.session_state:
        st.session_state.skills = []
    if 'resume_generated' not in st.session_state:
        st.session_state.resume_generated = False
    if 'cover_letter_generated' not in st.session_state:
        st.session_state.cover_letter_generated = False
    
    # Initialize resume builder
    try:
        builder = ResumeBuilder()
    except ValueError as e:
        st.error(str(e))
        st.stop()
    
    # UI Header
    st.title("🚀 AI-Powered Resume & Cover Letter Tailoring Tool")
    st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .stButton>button {width: 100%;}
    .skill-box {border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 5px 0;}
    </style>
    """, unsafe_allow_html=True)
    
    # Tabs for Resume and Cover Letter
    tab1, tab2 = st.tabs(["Resume Builder", "Cover Letter Builder"])
    
    # Resume Builder Tab
    with tab1:
        # Step 1: Inputs
        with st.expander("📝 Step 1: Provide Your Information", expanded=True):
            resume_text = st.text_area(
                "Your Current Resume (paste text)",
                height=200,
                help="Copy-paste your existing resume content",
                key="resume_text"  # Unique key
            )
            
            job_description = st.text_area(
                "Target Job Description",
                height=200,
                help="Paste the full job description you're applying for",
                key="job_description"  # Unique key
            )
            
            if st.button("Analyze Job Requirements", type="primary"):
                if not all([resume_text, job_description]):
                    st.warning("Please provide both resume and job description")
                else:
                    with st.spinner(f"Identifying top {MAX_SKILLS} required skills..."):
                        st.session_state.skills = builder.extract_skills(job_description)
                    
                    if not st.session_state.skills:
                        st.error("Failed to extract skills. Please try again.")
                    else:
                        st.session_state.resume_generated = False
        
        # Step 2: Skill Selection
        if st.session_state.skills:
            with st.expander("🎯 Step 2: Customize Skill Emphasis", expanded=True):
                st.markdown("**Top Skills Identified:** (Select 3-6 to emphasize)")
                
                # Create two columns for better skill display
                col1, col2 = st.columns(2)
                selected_skills = []
                
                for i, skill in enumerate(st.session_state.skills):
                    col = col1 if i % 2 == 0 else col2
                    if col.checkbox(skill, key=f"skill_{i}", value=(i < 5)):
                        selected_skills.append(skill)
                
                if st.button("Generate Tailored Resume", type="primary"):
                    if len(selected_skills) < 3:
                        st.warning("Please select at least 3 skills for best results")
                    else:
                        with st.spinner("Crafting your perfect resume..."):
                            custom_resume = builder.generate_custom_resume(
                                resume_text,
                                job_description,
                                selected_skills
                            )
                        
                        if custom_resume:
                            st.session_state.custom_resume = custom_resume
                            st.session_state.resume_generated = True
                            st.session_state.selected_skills = selected_skills
        
        # Step 3: Results
        if st.session_state.get('resume_generated', False):
            with st.expander("✨ Step 3: Your Tailored Resume", expanded=True):
                st.markdown("**Customized Resume Preview**")
                st.markdown(st.session_state.custom_resume)
                
                # PDF Generation
                pdf_data = builder.create_pdf(st.session_state.custom_resume)
                if pdf_data:
                    st.markdown(create_download_link(pdf_data, "tailored_resume.pdf"), 
                               unsafe_allow_html=True)
                
                # Improvement Tips
                st.markdown("---")
                st.markdown("**Pro Tips:**")
                st.markdown("""
                - Review for accuracy of all facts and figures
                - Ensure your LinkedIn matches this resume
                - Save with a clear filename like "FirstName_LastName_[JobTitle]_Resume.pdf"
                """)
    
    # Cover Letter Builder Tab
    with tab2:
        st.header("Cover Letter Builder")
        
        # Step 1: Inputs
        with st.expander("📝 Step 1: Provide Your Information", expanded=True):
            cover_letter_resume_text = st.text_area(
                "Your Current Resume (paste text)",
                height=200,
                help="Copy-paste your existing resume content",
                key="cover_letter_resume_text"  # Unique key
            )
            
            cover_letter_job_description = st.text_area(
                "Target Job Description",
                height=200,
                help="Paste the full job description you're applying for",
                key="cover_letter_job_description"  # Unique key
            )
            
            company_name = st.text_input(
                "Company Name",
                help="Enter the name of the company you're applying to"
            )
            
            recipient_name = st.text_input(
                "Recipient Name",
                help="Enter the name of the hiring manager or recruiter"
            )
            
            if st.button("Analyze Job Requirements for Cover Letter", type="primary"):
                if not all([cover_letter_resume_text, cover_letter_job_description, company_name, recipient_name]):
                    st.warning("Please provide all required information")
                else:
                    with st.spinner(f"Identifying top {MAX_SKILLS} required skills..."):
                        st.session_state.skills = builder.extract_skills(cover_letter_job_description)
                    
                    if not st.session_state.skills:
                        st.error("Failed to extract skills. Please try again.")
                    else:
                        st.session_state.cover_letter_generated = False
        
        # Step 2: Skill Selection
        if st.session_state.skills:
            with st.expander("🎯 Step 2: Customize Skill Emphasis", expanded=True):
                st.markdown("**Top Skills Identified:** (Select 3-6 to emphasize)")
                
                # Create two columns for better skill display
                col1, col2 = st.columns(2)
                selected_skills = []
                
                for i, skill in enumerate(st.session_state.skills):
                    col = col1 if i % 2 == 0 else col2
                    if col.checkbox(skill, key=f"cover_letter_skill_{i}", value=(i < 5)):
                        selected_skills.append(skill)
                
                if st.button("Generate Tailored Cover Letter", type="primary"):
                    if len(selected_skills) < 3:
                        st.warning("Please select at least 3 skills for best results")
                    else:
                        with st.spinner("Crafting your perfect cover letter..."):
                            custom_cover_letter = builder.generate_cover_letter(
                                cover_letter_resume_text,
                                cover_letter_job_description,
                                selected_skills,
                                company_name,
                                recipient_name
                            )
                        
                        if custom_cover_letter:
                            st.session_state.custom_cover_letter = custom_cover_letter
                            st.session_state.cover_letter_generated = True
                            st.session_state.selected_skills = selected_skills
        
        # Step 3: Results
        if st.session_state.get('cover_letter_generated', False):
            with st.expander("✨ Step 3: Your Tailored Cover Letter", expanded=True):
                st.markdown("**Customized Cover Letter Preview**")
                st.markdown(st.session_state.custom_cover_letter)
                
                # PDF Generation
                pdf_data = builder.create_pdf(st.session_state.custom_cover_letter)
                if pdf_data:
                    st.markdown(create_download_link(pdf_data, "tailored_cover_letter.pdf"), 
                               unsafe_allow_html=True)
                
                # Improvement Tips
                st.markdown("---")
                st.markdown("**Pro Tips:**")
                st.markdown("""
                - Review for accuracy of all facts and figures
                - Ensure your LinkedIn matches this cover letter
                - Save with a clear filename like "FirstName_LastName_[JobTitle]_CoverLetter.pdf"
                """)

if __name__ == "__main__":
    main_ui()
