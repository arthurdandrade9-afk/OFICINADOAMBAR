import unittest
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "deliverables" / "bonus" / "01-guia-premium-de-fornecedores.pdf"
ASSETS = ROOT / "assets" / "bonus-premium" / "volume-01"

class SupplierGuideTests(unittest.TestCase):
    def test_premium_guide_has_required_depth_and_original_art(self):
        self.assertTrue((ASSETS / "fornecedores-capa.png").exists())
        self.assertTrue((ASSETS / "comparativo-amostras.png").exists())
        self.assertTrue(PDF.exists())
        reader = PdfReader(str(PDF))
        self.assertGreaterEqual(len(reader.pages), 14)
        self.assertLessEqual(len(reader.pages), 18)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        for expected in ("6 perguntas essenciais", "Sinais de alerta", "Comparativo de propostas", "Ficha de amostra", "Plano de ação"):
            self.assertIn(expected, text)

if __name__ == "__main__": unittest.main()
