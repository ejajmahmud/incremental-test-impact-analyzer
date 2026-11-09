"""Unit tests for incremental-test-impact-analyzer."""
import unittest
from incremental_test_impact_analyzer.analyzer import TestImpactAnalyzer


class TestImpactAnalyzerTest(unittest.TestCase):
    def setUp(self):
        self.analyzer = TestImpactAnalyzer()
        test_code = """
class TestCalc(unittest.TestCase):
    def test_add(self):
        res = compute_sum(1, 2)
    def test_sub(self):
        res = compute_diff(5, 2)
"""
        self.analyzer.index_test_file("test_calc.py", test_code)

    def test_impact_mapping(self):
        impacted = self.analyzer.identify_impacted_tests(["compute_sum"])
        self.assertEqual(impacted, ["TestCalc.test_add"])

    def test_unrelated_symbol(self):
        impacted = self.analyzer.identify_impacted_tests(["unknown_function"])
        self.assertEqual(len(impacted), 0)
