import unittest
from pathlib import Path

HTML = (Path(__file__).resolve().parents[1] / "index.html").read_text(encoding="utf-8")

class OfferPageTests(unittest.TestCase):
    def test_ten_bonus_showcase_explains_buyer_outcomes(self):
        self.assertGreaterEqual(HTML.count('class="bonus-card"'), 10)
        for label in ("10 bônus", "Kit Primeira Venda", "Mapa das 30 Coleções", "Banco de 100 Nomes", "Kit Vitrine", "Cartões de Cuidado", "Calendário"):
            self.assertIn(label, HTML)

    def test_final_mechanism_uses_our_generator_and_standard_label(self):
        self.assertIn("nosso Gerador de Rótulos", HTML)
        self.assertIn("assets/rotulos/exemplo-rotulo-sabonete.png", HTML)

if __name__ == "__main__": unittest.main()
