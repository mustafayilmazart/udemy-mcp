"""Rakip kurs analiz modulu."""

import json
from browser_scanner import BrowserScanner


class CompetitorScanner:
    """Udemy'de rakip kurslari tarar ve karsilastirir."""

    def __init__(self):
        self.scanner = BrowserScanner()

    def scan(self, anahtar_kelime: str, limit: int = 5) -> dict:
        """Rakip kurslari tara."""
        return self.scanner.scan_competitors(anahtar_kelime, limit)

    def compare(self, kendi_kursun: dict, rakipler: list) -> dict:
        """Kendi kursunu rakiplerle karsilastir."""
        karsilastirma = []
        for rakip in rakipler:
            karsilastirma.append({
                "rakip_baslik": rakip.get("baslik", "?"),
                "rakip_puan": rakip.get("puan", 0),
                "rakip_ogrenci": rakip.get("ogrenci_sayisi", 0),
                "farklilasma_onerileri": [
                    "Daha fazla uygulamali icerik ekle",
                    "Turkce kaynak paketi sun",
                    "Guncel tutma taahhut ver",
                ],
            })
        return {
            "kendi_kursun": kendi_kursun.get("baslik", "?"),
            "rakip_sayisi": len(rakipler),
            "karsilastirma": karsilastirma,
        }
