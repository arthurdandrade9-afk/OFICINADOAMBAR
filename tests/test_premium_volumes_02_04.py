import unittest
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "02-custos-e-precificacao-premium.pdf": (18, 24, "Formação de preço"),
    "03-15-dicas-de-economia-premium.pdf": (14, 18, "Economia segura"),
    "04-atelie-de-rotulos-premium.pdf": (16, 22, "Hierarquia visual"),
}

class PremiumVolumesTests(unittest.TestCase):
    def test_volumes_have_required_depth(self):
        for name, (minimum, maximum, marker) in CASES.items():
            path = ROOT / "deliverables" / "bonus" / name
            self.assertTrue(path.exists(), name)
            reader = PdfReader(str(path))
            self.assertGreaterEqual(len(reader.pages), minimum, name)
            self.assertLessEqual(len(reader.pages), maximum, name)
            text = "\n".join(p.extract_text() or "" for p in reader.pages)
            self.assertIn(marker, text)

if __name__ == "__main__": unittest.main()
