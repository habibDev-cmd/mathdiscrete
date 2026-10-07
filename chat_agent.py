"""Rule-based chat routing for the supported discrete mathematics solvers."""

from __future__ import annotations

import re
from typing import Any

from solver import InputError, counting, graph_summary, relation_properties, set_operation, truth_table


def _response(text: str, table: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {"text": text, "table": table}


def _solve_logic(question: str) -> dict[str, Any]:
    expression = question.casefold()
    expression = re.sub(
        r"\b(tolong|buatkan|buat|hitung|cek|periksa|tabel\s+kebenaran|logika\s+proposisional|ekspresi|apakah|termasuk|adalah|tautologi|kontradiksi|kontingensi|dari)\b",
        " ",
        expression,
        flags=re.IGNORECASE,
    )
    for source, target in (("∧", " and "), ("∨", " or "), ("¬", " not "), ("~", " not ")):
        expression = expression.replace(source, target)
    expression = re.sub(r"\b(dan|atau|tidak)\b", lambda match: {"dan": "and", "atau": "or", "tidak": "not"}[match.group(1)], expression)
    expression = re.sub(r"[?.,:;]", " ", expression).strip()
    result = truth_table(expression)
    label = result["classification"].title()
    return _response(
        f"Ekspresi `{expression}` diklasifikasikan sebagai **{label}**. "
        f"Saya mengevaluasi {len(result['rows'])} kemungkinan nilai untuk variabel "
        f"{', '.join(f'`{name}`' for name in result['variables'])}. Tabelnya ada di bawah.",
        result["rows"],
    )


def _solve_sets(question: str) -> dict[str, Any]:
    match_a = re.search(r"\bA\s*[:=]\s*(\{[^}]*\})", question, flags=re.IGNORECASE)
    match_b = re.search(r"\bB\s*[:=]\s*(\{[^}]*\})", question, flags=re.IGNORECASE)
    if not match_a or not match_b:
        raise InputError("Tuliskan kedua himpunan, contohnya: `A={1,2,3}, B={2,3,4}`.")
    result = set_operation(match_a.group(1), match_b.group(1))
    lines = [f"- **{name}** = `{sorted(values, key=str)}`" for name, values in result.items()]
    return _response("Operasi pada dua himpunan tersebut menghasilkan:\n\n" + "\n".join(lines))


def _solve_counting(question: str) -> dict[str, Any]:
    text = question.lower()
    operation = "Permutasi nPr" if any(word in text for word in ("permutasi", "menyusun", "urutan")) else "Kombinasi nCr"
    match = re.search(r"(?:memilih|ambil|pilih)\s*(\d+)\s*(?:orang|objek|benda|unsur|huruf)?\s*(?:dari|dalam)\s*(\d+)", text)
    if match:
        r, n = map(int, match.groups())
    else:
        match = re.search(r"(?:dari|dalam)\s*(\d+).*?(?:dipilih|diambil|memilih|pilih)\s*(\d+)", text)
        if match:
            n, r = map(int, match.groups())
        else:
            match = re.search(r"(?:permutasi|kombinasi)\s*(\d+)\s*(?:pilih|ambil)\s*(\d+)", text)
            if match:
                n, r = map(int, match.groups())
            else:
                match = re.search(r"\bn\s*=\s*(\d+).*?\br\s*=\s*(\d+)", text)
                if not match:
                    raise InputError("Sebutkan n dan r, misalnya `berapa cara memilih 3 dari 8` atau `kombinasi n=8 r=3`.")
                n, r = map(int, match.groups())

    answer = counting(operation, n, r)
    formula = f"{n}!/({n}-{r})!" if operation.startswith("Permutasi") else f"{n}!/({r}!({n}-{r})!)"
    return _response(
        f"Ini **{'permutasi' if operation.startswith('Permutasi') else 'kombinasi'}**: "
        f"urutan {'diperhitungkan' if operation.startswith('Permutasi') else 'tidak diperhitungkan'}.\n\n"
        f"Rumus: `{formula}`\n\nHasilnya **{answer:,}**."
    )


def _solve_graph(question: str) -> dict[str, Any]:
    vertices_match = re.search(r"(?:simpul|vertices)\s*[:=]\s*(.+?)(?=\s+(?:sisi|edges)\s*[:=]|$)", question, re.IGNORECASE | re.DOTALL)
    edges_match = re.search(r"(?:sisi|edges)\s*[:=]\s*(.+)$", question, re.IGNORECASE | re.DOTALL)
    if not vertices_match or not edges_match:
        raise InputError("Tuliskan `simpul: A, B, C` dan `sisi: A-B; B-C`.")
    vertices = vertices_match.group(1).strip().strip("{}[]")
    edges = re.sub(r"\s*[;\n]\s*", "\n", edges_match.group(1).strip())
    result = graph_summary(vertices, edges)
    degree_text = ", ".join(f"{vertex}: {degree}" for vertex, degree in result["degrees"].items())
    component_text = "; ".join("{" + ", ".join(component) + "}" for component in result["components"])
    return _response(
        f"Graf memiliki **{len(result['vertices'])} simpul** dan **{result['edges']} sisi**.\n\n"
        f"Derajat simpul: {degree_text}.\n\n"
        f"Komponen terhubung: {component_text}. Graf ini **{'terhubung' if result['connected'] else 'tidak terhubung'}**.",
        [{"Simpul": vertex, "Derajat": degree} for vertex, degree in result["degrees"].items()],
    )


def _solve_relation(question: str) -> dict[str, Any]:
    domain_match = re.search(r"(?:domain|himpunan)\s*[:=]\s*(.+?)(?=\s+(?:relasi|R)\s*[:=]|$)", question, re.IGNORECASE | re.DOTALL)
    relation_match = re.search(r"(?:relasi|R)\s*[:=]\s*(.+)$", question, re.IGNORECASE | re.DOTALL)
    if not domain_match or not relation_match:
        raise InputError("Tuliskan `domain: a, b` dan `relasi: (a,a); (a,b); (b,b)`.")
    domain = domain_match.group(1).strip().strip("{}[]")
    pairs = re.findall(r"\(([^()]*)\)", relation_match.group(1))
    if not pairs:
        raise InputError("Pasangan relasi belum terbaca. Gunakan format `(a,b); (b,a)`.")
    result = relation_properties(domain, "\n".join(pairs))
    properties = ("refleksif", "simetris", "antisimetris", "transitif", "ekuivalensi")
    lines = [f"- **{name.title()}**: {'ya' if result[name] else 'tidak'}" for name in properties]
    return _response("Pemeriksaan relasi pada domain tersebut:\n\n" + "\n".join(lines))


def answer_question(question: str) -> dict[str, Any]:
    """Route a clear natural-language prompt to a supported deterministic solver."""
    cleaned = question.strip()
    lowered = cleaned.lower()
    if not cleaned:
        return _response("Tulis soal yang ingin kamu bahas, ya.")

    try:
        if any(term in lowered for term in ("tabel kebenaran", "tautologi", "kontradiksi", "kontingensi", "logika proposisional")):
            return _solve_logic(cleaned)
        has_two_sets = re.search(r"\bA\s*[:=]\s*\{[^}]*\}.*\bB\s*[:=]\s*\{[^}]*\}", cleaned, re.IGNORECASE | re.DOTALL)
        if has_two_sets:
            return _solve_sets(cleaned)
        if any(term in lowered for term in ("permutasi", "kombinasi", "memilih", "menyusun", "urutan")):
            return _solve_counting(cleaned)
        if any(term in lowered for term in ("graf", "simpul", "sisi", "terhubung", "derajat")):
            return _solve_graph(cleaned)
        if any(term in lowered for term in ("relasi", "refleksif", "simetris", "transitif", "ekuivalensi", "antisimetris")):
            return _solve_relation(cleaned)
    except InputError as error:
        return _response(f"Saya belum bisa menghitungnya: {error}")

    return _response(
        "Saya belum mengenali tipe soal itu. Saat ini saya bisa membantu logika proposisional, "
        "operasi himpunan, permutasi/kombinasi, graf sederhana, dan sifat relasi. "
        "Coba tulis data soal dengan format yang jelas; contoh format ada di panel samping."
    )