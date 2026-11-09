"""Core Incremental Test Impact Analyzer implementation."""
import ast
import os
from typing import Dict, List, Set, Optional, Any


class SymbolReference:
    def __init__(self, symbol_name: str, file_path: str):
        self.symbol_name = symbol_name
        self.file_path = file_path


class TestImpactAnalyzer:
    def __init__(self):
        self.symbol_to_tests: Dict[str, Set[str]] = {}  # symbol_name -> {test_name}
        self.file_symbols: Dict[str, Set[str]] = {}  # file_path -> {symbol_names}

    def index_test_file(self, test_filepath: str, test_content: str):
        try:
            tree = ast.parse(test_content)
        except SyntaxError:
            return

        for node in tree.body:
            if isinstance(node, ast.ClassDef) and "Test" in node.name:
                for sub in node.body:
                    if isinstance(sub, ast.FunctionDef) and sub.name.startswith("test_"):
                        test_id = f"{node.name}.{sub.name}"
                        # Walk test body to find referenced function calls
                        for child in ast.walk(sub):
                            if isinstance(child, ast.Call):
                                if isinstance(child.func, ast.Name):
                                    self._link_symbol(child.func.id, test_id)
                                elif isinstance(child.func, ast.Attribute):
                                    self._link_symbol(child.func.attr, test_id)

    def _link_symbol(self, symbol: str, test_id: str):
        if symbol not in self.symbol_to_tests:
            self.symbol_to_tests[symbol] = set()
        self.symbol_to_tests[symbol].add(test_id)

    def identify_impacted_tests(self, modified_symbols: List[str]) -> List[str]:
        impacted = set()
        for sym in modified_symbols:
            if sym in self.symbol_to_tests:
                impacted.update(self.symbol_to_tests[sym])
        return sorted(list(impacted))

    def extract_symbols_from_source(self, source_code: str) -> List[str]:
        symbols = []
        try:
            tree = ast.parse(source_code)
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    symbols.append(node.name)
        except SyntaxError:
            pass
        return symbols
