"""Kurs guncelleme modulu — Playwright MCP ile Udemy'de degisiklik uygular."""

import json
from browser_scanner import BrowserScanner


class CourseUpdater:
    """Udemy kurs icerigini Playwright MCP uzerinden gunceller."""

    def __init__(self):
        self.scanner = BrowserScanner()

    def update_title(self, kurs_id: str, yeni_baslik: str) -> dict:
        """Kurs basligini guncelle."""
        return self.scanner.update_course(kurs_id, {"baslik": yeni_baslik})

    def update_description(self, kurs_id: str, yeni_aciklama: str) -> dict:
        """Kurs aciklamasini guncelle."""
        return self.scanner.update_course(kurs_id, {"aciklama": yeni_aciklama})

    def update_curriculum(self, kurs_id: str, degisiklikler: dict) -> dict:
        """Mufredat degisikliklerini uygula."""
        return self.scanner.update_course(kurs_id, {"mufredat": degisiklikler})

    def batch_update(self, kurs_id: str, tum_degisiklikler: dict) -> dict:
        """Toplu guncelleme."""
        return self.scanner.update_course(kurs_id, tum_degisiklikler)
