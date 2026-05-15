
from agent import process_natural_language_request

print("\n=== STARTING AGENTIC CIAM/ABAC SYSTEM PROTOTYPE ===")

# Test case 1: The happy path using natural language
process_natural_language_request("Hey there, could you let Alex open up the Q4 financial budget spreadsheet?")

# Test case 2: The unauthorized path using natural language
process_natural_language_request("Sam here from marketing, I need to check the ledger to see if a client invoice cleared.")

print("====================================================")