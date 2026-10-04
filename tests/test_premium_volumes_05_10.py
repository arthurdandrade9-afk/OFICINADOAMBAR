import unittest
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "05-primeira-venda-7-dias-premium.pdf": (18, 22, ("DIA 1", "DIA 7", "ROTEIRO DE WHATSAPP")),
    "06-mapa-30-colecoes-premium.pdf": (24, 32, ("Spa de Domingo", "Casa Serena", "EMBALAGEM")),
    "07-banco-100-nomes-premium.pdf": (18, 24, ("100 NOMES", "Ambarina", "FILTRO DE ESCOLHA")),
    "08-vitrine-fotos-e-textos-premium.pdf": (20, 26, ("ROTEIRO DE FOTO", "Seu novo jeito favorito", "CHECKLIST")),
    "09-cartoes-e-tags-premium.pdf": (18, 24, ("MODELO 01", "MODELO 10", "GUIA DE IMPRESS")),
    "10-calendario-comercial-premium.pdf": (20, 26, ("JANEIRO", "DEZEMBRO", "PLANO DE 90 DIAS")),
}


class PremiumVolumesTests(unittest.TestCase):
    def test_volumes_have_promised_depth_and_core_sections(self):
        for filename, (minimum, maximum, markers) in CASES.items():
            path = ROOT / "deliverables" / "bonus" / filename
            self.assertTrue(path.exists(), filename)
            reader = PdfReader(str(path))
            self.assertGreaterEqual(len(reader.pages), minimum, filename)
            self.assertLessEqual(len(reader.pages), maximum, filename)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            for marker in markers:
                self.assertIn(marker, text, f"{filename}: {marker}")


if __name__ == "__main__":
    unittest.main()
