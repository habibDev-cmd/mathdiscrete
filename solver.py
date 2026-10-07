"""Deterministic solvers for a focused set of discrete mathematics exercises."""

from __future__ import annotations

import ast
import itertools
import math
import re
from collections import deque
from typing import Any


class InputError(ValueError):
    """Raised when a problem is outside the supported input grammar."""


def _boolean_value(node: ast.AST, assignment: dict[str, bool]) -> bool:
    if isinstance(node, ast.Name):
        return assignment[node.id]
    if isinstance(node, ast.Constant) and isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not _boolean_value(node.operand, assignment)
    if isinstance(node, ast.BoolOp):
        values = [_boolean_value(value, assignment) for value in node.values]
        if isinstance(node.op, ast.And):
            return all(values)
        if isinstance(node.op, ast.Or):
            return any(values)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitXor):
        return _boolean_value(node.left, assignment) ^ _boolean_value(node.right, assignment)
    raise InputError("Ekspresi memakai operator yang belum didukung.")


def truth_table(expression: str, max_variables: int = 8) -> dict[str, Any]:
    """Evaluate an expression using and/or/not/^ with a complete truth table."""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as error:
        raise InputError("Format ekspresi tidak valid.") from error

    names = sorted({node.id for node in ast.walk(tree) if isinstance(node, ast.Name)})
    if not names:
        raise InputError("Ekspresi harus memuat setidaknya satu variabel, misalnya p and q.")
    if len(names) > max_variables:
        raise InputError(f"Maksimal {max_variables} variabel agar tabel tetap terbaca.")

    rows = []
    for values in itertools.product((False, True), repeat=len(names)):
        assignment = dict(zip(names, values))
        rows.append({**assignment, "hasil": _boolean_value(tree.body, assignment)})

    outcomes = [row["hasil"] for row in rows]
    classification = "tautologi" if all(outcomes) else "kontradiksi" if not any(outcomes) else "kontingensi"
    return {"variables": names, "rows": rows, "classification": classification}


def _parse_set(value: str) -> set[Any]:
    try:
        parsed = ast.literal_eval(value)
    except (SyntaxError, ValueError) as error:
        raise InputError("Gunakan literal himpunan Python, misalnya {1, 2, 3}.") from error
    if not isinstance(parsed, (set, frozenset, list, tuple)):
        raise InputError("Masukan harus berupa himpunan, list, atau tuple.")
    try:
        return set(parsed)
    except TypeError as error:
        raise InputError("Anggota himpunan harus berupa nilai sederhana yang dapat dibandingkan.") from error


def set_operation(left_text: str, right_text: str) -> dict[str, set[Any]]:
    left, right = _parse_set(left_text), _parse_set(right_text)
    return {
        "A ∪ B": left | right,
        "A ∩ B": left & right,
        "A − B": left - right,
        "B − A": right - left,
        "A △ B": left ^ right,
    }


def counting(operation: str, n: int, r: int) -> int:
    if n < 0 or r < 0 or r > n:
        raise InputError("Syarat harus 0 ≤ r ≤ n.")
    if operation == "Permutasi nPr":
        return math.perm(n, r)
    if operation == "Kombinasi nCr":
        return math.comb(n, r)
    raise InputError("Pilih operasi permutasi atau kombinasi.")


def _tokens(text: str) -> list[str]:
    values = [token.strip() for token in text.split(",") if token.strip()]
    if not values or len(set(values)) != len(values):
        raise InputError("Daftar simpul harus berisi nama unik yang dipisahkan koma.")
    return values


def graph_summary(vertices_text: str, edges_text: str) -> dict[str, Any]:
    vertices = _tokens(vertices_text)
    adjacency = {vertex: set() for vertex in vertices}
    for raw_edge in edges_text.splitlines():
        raw_edge = raw_edge.strip()
        if not raw_edge:
            continue
        parts = re.split(r"\s*[-,]\s*", raw_edge)
        if len(parts) != 2 or any(vertex not in adjacency for vertex in parts):
            raise InputError(f"Sisi tidak valid: {raw_edge}. Gunakan format A-B dan simpul yang terdaftar.")
        left, right = parts
        if left == right:
            raise InputError("MVP ini hanya menerima graf sederhana tanpa loop.")
        adjacency[left].add(right)
        adjacency[right].add(left)

    unseen = set(vertices)
    components = []
    while unseen:
        start = unseen.pop()
        component = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current] & unseen:
                unseen.remove(neighbor)
                component.add(neighbor)
                queue.append(neighbor)
        components.append(sorted(component))

    degrees = {vertex: len(neighbors) for vertex, neighbors in adjacency.items()}
    return {
        "vertices": vertices,
        "edges": sum(degrees.values()) // 2,
        "degrees": degrees,
        "components": components,
        "connected": len(components) == 1,
        "adjacency": adjacency,
    }


def _parse_pairs(text: str) -> set[tuple[str, str]]:
    pairs = set()
    for raw_pair in text.splitlines():
        raw_pair = raw_pair.strip().strip("()")
        if not raw_pair:
            continue
        parts = [part.strip() for part in raw_pair.split(",")]
        if len(parts) != 2 or not all(parts):
            raise InputError(f"Pasangan tidak valid: {raw_pair}. Gunakan format a,b per baris.")
        pairs.add((parts[0], parts[1]))
    return pairs


def relation_properties(domain_text: str, pairs_text: str) -> dict[str, Any]:
    domain = set(_tokens(domain_text))
    relation = _parse_pairs(pairs_text)
    outside = {item for pair in relation for item in pair} - domain
    if outside:
        raise InputError("Semua elemen pasangan relasi harus tercantum di domain.")

    reflexive = all((item, item) in relation for item in domain)
    symmetric = all((right, left) in relation for left, right in relation)
    antisymmetric = all(left == right or (right, left) not in relation for left, right in relation)
    transitive = all(
        (left, end) in relation
        for left, middle in relation
        for second, end in relation
        if middle == second
    )
    return {
        "refleksif": reflexive,
        "simetris": symmetric,
        "antisimetris": antisymmetric,
        "transitif": transitive,
        "ekuivalensi": reflexive and symmetric and transitive,
        "relasi": relation,
    }