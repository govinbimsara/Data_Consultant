import streamlit as st
import sys
import os
import re
from datetime import datetime
from io import StringIO
import threading
import time

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.research_analyst.crew import ResearchAnalyst

def strip_ansi_codes(text):
    """Remove ANSI color codes from text"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def sanitize_filename(text):
    """Convert text to safe filename format"""
    # Replace spaces and special characters with underscores
    sanitized = re.sub(r'[^\w\s-]', '', text)
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    return sanitized.strip('_')

def generate_filename(company_name):
    """Generate filename with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_company = sanitize_filename(company_name)
    return f"research_analyst/Reports/{safe_company}_{timestamp}.md"

class StreamCapture:
    """Capture stdout/stderr for real-time display"""
    def __init__(self, placeholder):
        self.content = []
        self.placeholder = placeholder
        
    def write(self, text):
        if text.strip():
            clean_text = strip_ansi_codes(text)
            self.content.append(clean_text)
            # Update the display in real-time
            self.placeholder.text_area(
                "Live Output:", 
                '\n'.join(self.content[-50:]),  # Show last 50 lines
                height=300,
                key=f"log_{len(self.content)}"
            )
        
    def flush(self):
        pass
        
    def get_content(self):
        return '\n'.join(self.content)

def run_crew_analysis(company, website, output_file, progress_placeholder, log_placeholder, status_placeholder):
    """Run the crew analysis with progress tracking"""
    
    # Capture stdout/stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    captured_output = StreamCapture(log_placeholder)
    sys.stdout = captured_output
    sys.stderr = captured_output
    
    try:
        # Update status
        status_placeholder.info("🚀 Initializing crew...")
        
        inputs = {
            'company': company,
            'website': website,
            'current_year': str(datetime.now().year)
        }
        
        # Create crew instance with output file
        crew_instance = ResearchAnalyst(output_file=output_file)
        
        status_placeholder.info("🔍 Starting research analysis...")
        progress_placeholder.progress(0.2)
        
        # Run the crew
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        progress_placeholder.progress(1.0)
        status_placeholder.success("✅ Analysis completed successfully!")
        
        return True, None
        
    except Exception as e:
        status_placeholder.error("❌ Analysis failed!")
        return False, str(e)
        
    finally:
        # Restore stdout/stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr

def main():
    st.set_page_config(
        page_title="AI Research Analyst",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 AI Research Analyst")
    st.markdown("Generate comprehensive AI use case reports for any company")
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input(
            "Company Name",
            placeholder="e.g., Apple Inc",
            help="Enter the full company name"
        )
    
    with col2:
        website_url = st.text_input(
            "Website URL",
            placeholder="e.g., https://www.apple.com/",
            help="Enter the company's website URL"
        )
    
    # Validation
    if st.button("🚀 Generate Report", type="primary", disabled=not (company_name and website_url)):
        
        # Generate output filename
        output_file = generate_filename(company_name)
        
        # Create Reports directory if it doesn't exist
        os.makedirs("research_analyst/Reports", exist_ok=True)
        
        # Progress tracking
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        # Log output section
        st.subheader("📋 Analysis Progress")
        log_placeholder = st.empty()
        
        # Error section (initially hidden)
        error_placeholder = st.empty()
        
        # Run analysis
        with st.spinner("Running analysis..."):
            success, error = run_crew_analysis(
                company_name, 
                website_url, 
                output_file,
                progress_placeholder,
                log_placeholder,
                status_placeholder
            )
        
        if success:
            st.success("🎉 Report generated successfully!")
            
            # Download section
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    report_content = f.read()
                
                st.download_button(
                    label="📥 Download Report",
                    data=report_content,
                    file_name=os.path.basename(output_file),
                    mime="text/markdown",
                    type="secondary"
                )
                
                # Preview section
                with st.expander("📖 Preview Report"):
                    st.markdown(report_content[:2000] + "..." if len(report_content) > 2000 else report_content)
            
        else:
            error_placeholder.error(f"❌ **Error occurred:** {error}")
    
    # Instructions
    with st.sidebar:
        st.header("📖 Instructions")
        st.markdown("""
        1. **Enter Company Name**: Full company name for the report
        2. **Enter Website URL**: Company's official website
        3. **Click Generate**: Start the AI analysis
        4. **Monitor Progress**: Watch real-time progress and logs
        5. **Download Report**: Get your comprehensive AI use case report
        
        **Note**: Analysis may take 5-10 minutes depending on company complexity.
        """)
        
        st.header("🔧 Features")
        st.markdown("""
        - **Real-time Progress**: Live updates during analysis
        - **Comprehensive Reports**: 15+ AI use cases
        - **Instant Download**: Get reports in Markdown format
        - **Error Handling**: Clear error messages if issues occur
        """)

if __name__ == "__main__":
    main()