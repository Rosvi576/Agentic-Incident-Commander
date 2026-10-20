import streamlit as st
from openai import OpenAI

# Page Setup
st.set_page_config(
    page_title="Agentic Incident Commander", 
    page_icon="🚨", 
    layout="wide"
)

# Title Header
st.title("🚨 Agentic Incident Commander")
st.caption("Automated SRE Copilot • Root Cause Analysis & Code Remediation Platform")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ System Status")
    st.success("🟢 Local Engine Active")
    st.info("Model: **Llama 3.2 (Ollama)**")
    st.markdown("---")
    st.markdown("### 🏆 Hackathon Details")
    st.markdown("- **Track**: Best Apps & Agents")
    st.markdown("- **Deployment**: Local / Self-Hosted Engine")

# Connect to local Ollama instance
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# Quick Preset Options
st.subheader("1. Incident Context")

preset = st.selectbox(
    "Load Example Preset:",
    ["Custom", "Redis Connection Refused", "PostgreSQL Pool Exhaustion", "HTTP 504 Gateway Timeout"]
)

# Set defaults based on selection
if preset == "Redis Connection Refused":
    default_service = "Payment Gateway Microservice"
    default_stack = "Python 3.11, FastAPI, Redis, Docker"
    default_error = "redis.exceptions.ConnectionError: Error 111 connecting to 127.0.0.1:6379."
    default_log = "redis.exceptions.ConnectionError: Error 111 connecting to 127.0.0.1:6379. Connection refused.\ncelery.worker.consumer.consumer: ERROR: Consumer: Connection to broker lost."
elif preset == "PostgreSQL Pool Exhaustion":
    default_service = "User Authentication Service"
    default_stack = "Node.js, Express, PostgreSQL, Prisma"
    default_error = "PrismaClientInitializationError: Timed out fetching a new connection from the pool."
    default_log = "Error: ConnectionPoolTimeoutError: Connection pool is full. Max pool size: 10. Active connections: 10."
else:
    default_service = "Payment Service"
    default_stack = "Python 3.11, FastAPI, Docker"
    default_error = "Connection Failure"
    default_log = "Insert log trace here..."

col1, col2 = st.columns(2)
with col1:
    service_name = st.text_input("Service Name", value=default_service)
    error_type = st.text_input("Error Exception", value=default_error)

with col2:
    tech_stack = st.text_input("Tech Stack", value=default_stack)

raw_log = st.text_area("Stack Trace / Application Logs:", height=150, value=default_log)

# Execution Trigger
if st.button("🚀 Run Incident Analysis & Resolution", type="primary", use_container_width=True):
    try:
        with st.spinner("🤖 SRE Agent analyzing logs and engineering code patch..."):
            prompt = f"""
            System/Service: {service_name}
            Tech Stack: {tech_stack}
            Exception Type: {error_type}

            Raw Trace Logs:
            ```
            {raw_log}
            ```

            Provide a comprehensive SRE Resolution Report in structured Markdown with these exact section headers:
            ### 1. Root Cause Analysis
            ### 2. Immediate Fix & Step-by-Step Remediation
            ### 3. Executable Code / Configuration Patch
            ### 4. Prevention & Monitoring Guidelines
            """

            response = client.chat.completions.create(
                model="llama3.2",
                messages=[
                    {"role": "system", "content": "You are a Senior Site Reliability Engineer (SRE). Provide concise, technical, and actionable incident analysis."},
                    {"role": "user", "content": prompt}
                ]
            )
            report = response.choices[0].message.content

        st.markdown("---")
        st.subheader("2. AI Incident Resolution Report")
        
        # Display output in tabs for clean layout
        tab1, tab2 = st.tabs(["📄 Full Incident Report", "📥 Export & Download"])
        
        with tab1:
            st.markdown(report)
            
        with tab2:
            st.markdown("#### Download Analysis")
            st.download_button(
                label="📥 Download Report (.md)",
                data=report,
                file_name=f"incident_report_{service_name.lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )

    except Exception as e:
        st.error(f"Error connecting to local engine: {str(e)}")