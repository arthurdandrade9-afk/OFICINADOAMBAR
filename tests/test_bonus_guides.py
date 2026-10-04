import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
BONUS_DIR = REPO / "deliverables" / "bonus"
EXPECTED_BONUSES = (
    "01-kit-primeira-venda-7-dias.pdf",
    "02-mapa-30-colecoes.pdf",
    "03-banco-100-nomes.pdf",
    "04-kit-vitrine-que-vende.pdf",
    "05-cartoes-e-tags.pdf",
    "06-calendario-de-datas.pdf",
)


class BonusGuideTests(unittest.TestCase):
    def test_six_bonus_pdfs_exist_and_are_substantial(self):
        for filename in EXPECTED_BONUSES:
            artifact = BONUS_DIR / filename
            self.assertTrue(artifact.exists(), filename)
            self.assertGreater(artifact.stat().st_size, 10_000, filename)


if __name__ == "__main__":
    unittest.main()
