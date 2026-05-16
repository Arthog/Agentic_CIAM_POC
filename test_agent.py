import unittest
from unittest.mock import patch

from agent import process_natural_language_request
from security_engine import evaluate_abac_policy


class PolicyEngineTests(unittest.TestCase):
    def test_finance_user_on_trusted_device_is_approved(self):
        decision = evaluate_abac_policy("alex", "financial_ledger")

        self.assertEqual(decision["status"], "APPROVED")
        self.assertEqual(decision["user_id"], "user_123")

    def test_marketing_contractor_is_denied_financial_ledger(self):
        decision = evaluate_abac_policy("sam", "financial_ledger")

        self.assertEqual(decision["status"], "DENIED")

    def test_compromised_finance_user_requires_step_up(self):
        decision = evaluate_abac_policy("alex compromised", "financial_ledger")

        self.assertEqual(decision["status"], "STEP_UP_REQUIRED")


class AgentOrchestrationTests(unittest.TestCase):
    @patch("agent._extract_request_with_gemini", side_effect=RuntimeError("no credentials"))
    def test_agent_falls_back_to_rules_and_uses_policy_engine(self, _mock_gemini):
        result = process_natural_language_request(
            "Sam here from marketing, I need to check the ledger."
        )

        self.assertEqual(result["extraction"]["source"], "rules_fallback")
        self.assertEqual(result["policy_decision"]["status"], "DENIED")

    @patch("agent._extract_request_with_gemini", side_effect=RuntimeError("no credentials"))
    def test_agent_approval_comes_from_exact_policy_status(self, _mock_gemini):
        result = process_natural_language_request(
            "Could Alex open the Q4 financial budget spreadsheet?"
        )

        self.assertEqual(result["policy_decision"]["status"], "APPROVED")


if __name__ == "__main__":
    unittest.main()
