import unittest

from chat_agent import answer_question
from solver import InputError, counting, graph_summary, relation_properties, set_operation, truth_table


class SolverTests(unittest.TestCase):
    def test_truth_table_classification_and_rows(self):
        result = truth_table("p or not p")
        self.assertEqual(result["classification"], "tautologi")
        self.assertEqual(len(result["rows"]), 2)

    def test_truth_table_rejects_unsupported_syntax(self):
        with self.assertRaises(InputError):
            truth_table("__import__('os').system('false')")

    def test_set_operations(self):
        result = set_operation("{1, 2}", "{2, 3}")
        self.assertEqual(result["A ∪ B"], {1, 2, 3})
        self.assertEqual(result["A ∩ B"], {2})

    def test_counting(self):
        self.assertEqual(counting("Permutasi nPr", 5, 2), 20)
        self.assertEqual(counting("Kombinasi nCr", 5, 2), 10)
        with self.assertRaises(InputError):
            counting("Kombinasi nCr", 2, 3)

    def test_graph_components_and_degrees(self):
        result = graph_summary("A, B, C", "A-B")
        self.assertFalse(result["connected"])
        self.assertEqual(result["degrees"], {"A": 1, "B": 1, "C": 0})

    def test_equivalence_relation(self):
        result = relation_properties("a, b", "a,a\nb,b\na,b\nb,a")
        self.assertTrue(result["ekuivalensi"])

    def test_chat_routes_propositional_logic(self):
        answer = answer_question("Buat tabel kebenaran p and not p")
        self.assertIn("Kontradiksi", answer["text"])
        self.assertEqual(len(answer["table"]), 2)

    def test_chat_routes_counting_in_indonesian(self):
        answer = answer_question("Berapa cara memilih 3 dari 8?")
        self.assertIn("56", answer["text"])

    def test_chat_routes_set_operations(self):
        answer = answer_question("Operasi himpunan A={1,2}, B={2,3}")
        self.assertIn("A ∪ B", answer["text"])
        self.assertIn("[1, 2, 3]", answer["text"])

    def test_chat_routes_graph_analysis(self):
        answer = answer_question("Analisis graf simpul: A, B, C sisi: A-B; B-C")
        self.assertIn("2 sisi", answer["text"])
        self.assertTrue(answer["table"])

    def test_chat_routes_relation_properties(self):
        answer = answer_question("Periksa relasi domain: a, b relasi: (a,a); (b,b); (a,b); (b,a)")
        self.assertIn("Ekuivalensi**: ya", answer["text"])

    def test_chat_normalizes_uppercase_logic_operators(self):
        answer = answer_question("Tabel kebenaran P DAN Q")
        self.assertIn("Kontingensi", answer["text"])

    def test_chat_asks_for_supported_input_when_ambiguous(self):
        answer = answer_question("Tolong selesaikan soal ini")
        self.assertIn("belum mengenali", answer["text"])


if __name__ == "__main__":
    unittest.main()