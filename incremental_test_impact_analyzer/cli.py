"""CLI for incremental-test-impact-analyzer."""
import sys
import argparse
from .analyzer import TestImpactAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Incremental Test Impact Analyzer CLI")
    parser.add_argument("--demo", action="store_true", help="Run test impact analysis demo")
    args = parser.parse_args()

    if args.demo:
        analyzer = TestImpactAnalyzer()
        test_code = """
class TestAuth(unittest.TestCase):
    def test_verify_token(self):
        verify_token("sample")

    def test_login(self):
        login_user("bob", "secret")
"""
        analyzer.index_test_file("tests/test_auth.py", test_code)
        print("Indexed Test Suite.")

        impacted = analyzer.identify_impacted_tests(["verify_token"])
        print(f"Modifying symbol 'verify_token' impacts tests:")
        for t in impacted:
            print(f"  -> {t}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
