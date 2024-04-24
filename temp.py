import json
from typing import Any, Dict, List, Tuple


class Term:
    def _init_(self, op: str, args: List['Term'] = None, constant: float = None, sym: str = None):
        self.op = op
        self.args = args or []
        self.constant = constant
        self.sym = sym


class SymbolEntry:
    def _init(self, type: str, expression: Term):
        self.type = type_
        self.expression = expression


def unknown_symbols(term: Term, defs: Dict[str, SymbolEntry]) -> List[str]:
    unknown_syms = []

    if term.op == "sym":
        if term.sym not in defs:
            unknown_syms.append(term.sym)
    else:
        for arg in term.args:
            unknown = unknown_symbols(arg, defs)
            unknown_syms.extend(unknown)

    return unknown_syms


def type_violations(term: Term, defs: Dict[str, SymbolEntry]) -> List[Term]:
    violations = []

    if term.op in {"*", "/", "+", "-"}:
        for arg in term.args:
            if arg.op != "sym" and arg.op != "constant":
                violations.append(arg)
    elif term.op == "if":
        if len(term.args) != 3:
            violations.append(term)
        else:
            for arg in term.args:
                if arg.op != "sym" and arg.op != "constant":
                    violations.append(arg)
    else:
        for arg in term.args:
            type_viol = type_violations(arg, defs)
            violations.extend(type_viol)

    return violations


def eval_expr(term: Term, defs: Dict[str, SymbolEntry], input_symbols: Dict[str, float]) -> float:
    if term.op == "constant":
        return term.constant
    elif term.op == "sym":
        if term.sym in input_symbols:
            return input_symbols[term.sym]
        else:
            entry = defs[term.sym]
            return eval_expr(entry.expression, defs, input_symbols)
    elif term.op in {"*", "/", "+", "-"}:
        if term.op == "*":
            result = 1.0
        elif term.op == "/":
            result = eval_expr(term.args[0], defs, input_symbols)
            for arg in term.args[1:]:
                result /= eval_expr(arg, defs, input_symbols)
            return result
        elif term.op == "+":
            result = 0.0
        else:  # term.op == "-"
            result = eval_expr(term.args[0], defs, input_symbols)
            for arg in term.args[1:]:
                result -= eval_expr(arg, defs, input_symbols)
            return result

        for arg in term.args:
            result *= eval_expr(arg, defs, input_symbols)
        return result
    elif term.op in {">", ">=", "<", "<="}:
        return 1.0 if eval_expr(term.args[0], defs, input_symbols) > eval_expr(term.args[1], defs, input_symbols) else 0.0
    elif term.op == "if":
        condition = eval_expr(term.args[0], defs, input_symbols)
        return eval_expr(term.args[1], defs, input_symbols) if abs(condition) < 1e-9 else eval_expr(term.args[2], defs, input_symbols)
    else:
        return float('nan')


def caching_eval_expr(term: Term, defs: Dict[str, SymbolEntry], input_symbols: Dict[str, float], cache: Dict[str, float]) -> float:
    term_str = term.sym if term.op == "sym" else term.op
    for arg in term.args:
        term_str += caching_eval_expr(arg, defs, input_symbols, cache)

    if term_str in cache:
        return cache[term_str]

    result = eval_expr(term, defs, input_symbols)
    cache[term_str] = result
    return result


def parse_expression(expr_str: str) -> Term:
    # Implement JSON parsing here to convert the string into a Term object
    # For simplicity, assume the input expression string is already parsed into a Term object
    return json.loads(expr_str)


def parse_symbol_definitions(defs_str: str) -> Dict[str, SymbolEntry]:
    # Implement JSON parsing here to convert the string into a dictionary of SymbolEntry objects
    # For simplicity, assume the input symbol definitions string is already parsed into a dictionary of SymbolEntry objects
    return json.loads(defs_str)


def parse_input_symbols(input_symbols_str: str) -> Dict[str, float]:
    # Implement JSON parsing here to convert the string into a dictionary of input symbols
    # For simplicity, assume the input input symbols string is already parsed into a dictionary of float values
    return json.loads(input_symbols_str)


def main() -> None:
    # Get the expression as a string
    expr_str = input("Enter the expression as a JSON string: ")

    # Parse the expression string into a Term object
    expr_term = parse_expression(expr_str)

    # Get the symbol definitions as a string
    defs_str = input("Enter the symbol definitions as a JSON string: ")

    # Parse the symbol definitions string into a dictionary of symbol entries
    defs_map = parse_symbol_definitions(defs_str)

    # Get the input symbols as a string
    input_symbols_str = input("Enter the input symbols as a JSON string: ")

    # Parse the input symbols string into a dictionary of input symbols
    input_symbols_map = parse_input_symbols(input_symbols_str)

    # Perform computations
    perform_computations(expr_term, defs_map, input_symbols_map)


if _name_ == "_main_":
    main()