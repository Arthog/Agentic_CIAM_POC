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
st.title("🛡️ Agentic CIAM Demonstration Workspace")
st.subheader("Dynamic Policy & Governance Evaluation Engine")
st.markdown("---")

st.markdown("### Input Natural Language Access Request")
user_query = st.text_input(
   
    
    label="Enter context (e.g., 'Requesting access to production database from internal subnet to run diagnostic script')",
    #max_chars=500,  # <--- Keeps the prompt short and input token costs predictably microscopic
    placeholder="Type access request context here..."
               
)

# Execution Trigger
if st.button("Evaluate Request", type="primary"):
    if user_query.strip() == "":
        
        st.warning("Please provide a valid text input to evaluate.")
    else:
        with st.spinner("Orchestrating agentic policy evaluation via Gemini..."):
            try:
                # Execution handoff to core agent.py engine
                agent_logs = process_natural_language_request(user_query)
                
                # =====================================================
                # FIXED DEFENSIVE STRING HANDLING
                # =====================================================
                # Converts the response payload cleanly to a string and forces uppercase
                # This guarantees character-case mismatches or JSON-wrapping won't trigger false negatives.
                agent_logs_clean = str(agent_logs).upper()
                
                # Core Engine Log Output
                fancy_ui.info("Orchestrator Logs & Token Evaluation Schema", str(agent_logs))
                
                # Security Gate Evaluation Conditional Check
                if "APPROVED" in agent_logs_clean:
                    fancy_ui.success("ACCESS GRANTED: Policy conditions fully satisfied.")
                else:
                    fancy_ui.error("ACCESS DENIED: Security architecture constraints breached.")
                    
            except Exception as e:
                st.error(f"Execution Error encountered during agent dispatch: {str(e)}")
                st.info("Debugging context:", f"Type: {type(e).__name__}")
