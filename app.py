# app.py
import streamlit as fancy_ui
from agent import process_natural_language_request
from security_engine import USER_DIRECTORY

# Set up the webpage layout
fancy_ui.set_page_config(page_title="AI-Driven ABAC Orchestrator", layout="wide")

fancy_ui.title("🛡️ Agentic CIAM & Attribute-Based Access Control Engine")
fancy_ui.caption("Technical PM Showcase: Combining Natural Language Orchestration with Deterministic Guardrails")

# Layout the portfolio cleanly using columns
col1, col2 = fancy_ui.columns([1, 2])

with col1:
    fancy_ui.header("📋 System Identities (User Directory)")
    fancy_ui.write("These are the live attributes stored securely in the CIAM database:")
    fancy_ui.json(USER_DIRECTORY)
    
    fancy_ui.divider()
    fancy_ui.markdown("""
    **How it works under the hood:**
    1. The user inputs a messy, natural language request.
    2. **Gemini 2.5 Flash** parses the intent and enforces a strict structured data model (Pydantic).
    3. The extracted attributes are passed directly to a zero-trust **Deterministic Policy Engine**.
    4. Access is granted or denied strictly based on ABAC attributes—the AI cannot hallucinate a breach.
    """)

with col2:
    fancy_ui.header("💬 Interactive Access Portal")
    fancy_ui.write("Simulate a user or application asking for access to a protected system resource.")
    
    # Provide clickable portfolio examples
    example_prompts = [
        "Select an example...",
        "Hey there, could you let Alex open up the Q4 financial budget spreadsheet?",
        "Sam here from marketing, I need to check the ledger to see if a client invoice cleared."
    ]
    
    selected_example = fancy_ui.selectbox("Quick-test Scenarios:", example_prompts)
    
    # Text input field for custom prompt hacking
    user_query = fancy_ui.text_input("Or write a custom access request (Try to prompt-inject it!):", 
                                     value="" if selected_example == "Select an example..." else selected_example)
    
    if fancy_ui.button("Submit Request to Agent", type="primary"):
        if user_query:
            with fancy_ui.spinner("Agent evaluating request constraints..."):
                # Redirect our print logs cleanly to show the agent's thought process in the UI
                import sys
                from io import StringIO
                
                old_stdout = sys.stdout
                sys.stdout = buffer = StringIO()
                
                # Execute the agent block we wrote earlier
                process_natural_language_request(user_query)
                
                sys.stdout = old_stdout
                agent_logs = buffer.getvalue()
                
                # Display the visual results based on engine responses
                fancy_ui.subheader("🤖 Agent Evaluation & Audit Trail")
                fancy_ui.code(agent_logs, language="text")
                
                if "APPROVED" in agent_logs:
                    fancy_ui.success("🔓 ACCESS GRANTED: Policy conditions fully satisfied.")
                else:
                    fancy_ui.error("🔒 ACCESS DENIED: Security architecture constraints breached.")