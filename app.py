import json

import streamlit as st
from agent import process_natural_language_request

# =====================================================================
# UI CONFIGURATION & STYLING
# =====================================================================
st.set_page_config(
    page_title="Agentic CIAM PoC Engine",
    page_icon="🛡️",
    layout="wide"
)

# Custom helper to match your UI component definitions
class FancyUI:
    def success(self, message):
        st.success(message, icon="🔓")
        
    def error(self, message):
        st.error(message, icon="🔒")
        
    def info(self, title, content):
        with st.expander(title, expanded=True):
            st.code(content, language="json")

fancy_ui = FancyUI()

# =====================================================================
# SESSION STATE INITIALIZATION
# =====================================================================
# Ensures clean state tracking across app reloads in the cloud environment
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True
if "user_role" not in st.session_state:
    st.session_state["user_role"] = "admin"

# =====================================================================
# MAIN USER INTERFACE RENDER
# =====================================================================
st.title("🛡️ Agentic ABAC Workspace")
st.subheader("Dynamic Policy & Governance Evaluation Engine")
st.markdown("---")

# Wrap the instructions and the line break in a tight container
with st.container(gap="small"):
    st.markdown(
    "**How to use this PoC Engine:** \n"
    "* Enter a natural language request detailing the action you want to take. \n"
    "* Include relevant contextual attributes such as your **role**, **location**, **network zone**, or **time of day**.\n"
    "* The agent will dynamically evaluate these attributes against corporate policy thresholds."
            )
    #st.markdown("---")
user_query = st.text_input(
   
    
    label="Enter context (e.g., 'Requesting access to production database from internal subnet to run diagnostic script')",
    max_chars=500,  # <--- Keeps the prompt short and input token costs predictably microscopic
    placeholder="Type access request context here..."
               
)

# Execution Trigger
if st.button("Evaluate Request", type="primary"):
    if user_query.strip() == "":
        
        st.warning("Please provide a valid text input to evaluate.")
    else:
        with st.spinner("Extracting request context and evaluating ABAC policy..."):
            try:
                # Execution handoff to core agent.py engine
                evaluation = process_natural_language_request(user_query)
                policy_decision = evaluation["policy_decision"]
                policy_status = policy_decision["status"]
                
                # Core Engine Log Output
                fancy_ui.info(
                    "Orchestrator Logs & Policy Evaluation Schema",
                    json.dumps(evaluation, indent=2)
                )
                
                # Security Gate Evaluation Conditional Check
                if policy_status == "APPROVED":
                    fancy_ui.success("ACCESS GRANTED: Policy conditions fully satisfied.")
                elif policy_status == "STEP_UP_REQUIRED":
                    st.warning("STEP-UP REQUIRED: Additional verification is required before access can be granted.")
                else:
                    fancy_ui.error("ACCESS DENIED: Security architecture constraints breached.")
                    
            except Exception as e:
                st.error(f"Execution Error encountered during agent dispatch: {str(e)}")
                st.info("Debugging context:", f"Type: {type(e).__name__}")
