"""Udemy kurs icerik analizcisi — 10 kriterli degerlendirme."""

from datetime import datetime


class ContentAnalyzer:
    """Kurs verisini 10 kriter uzerinden analiz eder, toplam /100 puan verir."""

    KRITERLER = [
        {"id": "baslik_seo", "ad": "Baslik SEO", "agirlik": 1.0,
         "aciklama": "Anahtar kelime, uzunluk (60-80 karakter), ilgi cekicilik"},
        {"id": "aciklama_kalitesi", "ad": "Aciklama Kalitesi", "agirlik": 1.0,
         "aciklama": "Uzunluk, yapı, CTA, bullet point, hedef kitle belirginligi"},
        {"id": "mufredat_yapisi", "ad": "Mufredat Yapisi", "agirlik": 1.0,
         "aciklama": "Bolum sayisi, ders sirasi, mantiksal akis, progresyon"},
        {"id": "ders_sureleri", "ad": "Ders Sureleri", "agirlik": 1.0,
         "aciklama": "Ortalama 5-15dk, toplam 3-10 saat, dengeli dagılım"},
        {"id": "uygulamali_oran", "ad": "Uygulamali Icerik Orani", "agirlik": 1.0,
         "aciklama": "Hands-on iceriklerin toplama orani (%40+ hedef)"},
        {"id": "quiz_degerlendirme", "ad": "Quiz/Degerlendirme", "agirlik": 1.0,
         "aciklama": "Her bolumde quiz, proje odevleri, final testi"},
        {"id": "kaynak_materyal", "ad": "Kaynak Materyal", "agirlik": 1.0,
         "aciklama": "Indirilebilir kaynak, cheat sheet, kod ornegi"},
        {"id": "yorum_analizi", "ad": "Yorum Analizi", "agirlik": 1.0,
         "aciklama": "Ortalama puan, negatif yorum oranlari, sik sikayet konulari"},
        {"id": "rekabet", "ad": "Rekabet Analizi", "agirlik": 1.0,
         "aciklama": "Benzer kurslara kiyasla farklilik ve avantaj"},
        {"id": "guncellik", "ad": "Guncellik", "agirlik": 1.0,
         "aciklama": "Son guncelleme tarihi, icerik yaslanmasi"},
    ]

    def analyze(self, kurs: dict) -> dict:
        """Kurs verisini analiz et, puan ve detay don."""
        sonuclar = []
        toplam = 0

        for kriter in self.KRITERLER:
            puan = self._kriter_puanla(kriter["id"], kurs)
            sonuclar.append({
                "kriter": kriter["ad"],
                "puan": puan,
                "max": 10,
                "aciklama": kriter["aciklama"],
            })
            toplam += puan

        seviye = "mukemmel" if toplam >= 90 else "iyi" if toplam >= 80 else "orta" if toplam >= 70 else "iyilestirme_gerekli"

        return {
            "kurs_adi": kurs.get("title", kurs.get("baslik", "Bilinmiyor")),
            "analiz_tarihi": datetime.now().isoformat(),
            "toplam_puan": toplam,
            "max_puan": 100,
            "seviye": seviye,
            "kriterler": sonuclar,
        }

    def _kriter_puanla(self, kriter_id: str, kurs: dict) -> int:
        """Tek bir kriteri puanla (0-10)."""
        baslik = kurs.get("title", kurs.get("baslik", ""))
        aciklama = kurs.get("description", kurs.get("aciklama", ""))

        if kriter_id == "baslik_seo":
            uzunluk = len(baslik)
            if 60 <= uzunluk <= 80:
                return 9
            elif 40 <= uzunluk <= 100:
                return 6
            elif uzunluk > 0:
                return 3
            return 0

        if kriter_id == "aciklama_kalitesi":
            uzunluk = len(aciklama)
            if uzunluk >= 500:
                return 8
            elif uzunluk >= 200:
                return 5
            elif uzunluk > 0:
                return 3
            return 0

        if kriter_id == "mufredat_yapisi":
            dersler = kurs.get("num_lectures", kurs.get("ders_sayisi", 0))
            if 30 <= dersler <= 80:
                return 8
            elif 15 <= dersler <= 100:
                return 6
            elif dersler > 0:
                return 4
            return 0

        if kriter_id == "ders_sureleri":
            toplam = kurs.get("content_length_video", kurs.get("toplam_sure_saat", 0))
            if isinstance(toplam, (int, float)) and 3 <= toplam <= 10:
                return 8
            elif isinstance(toplam, (int, float)) and toplam > 0:
                return 5
            return 3  # Veri yoksa varsayilan

        if kriter_id == "guncellik":
            son_guncelleme = kurs.get("last_update_date", kurs.get("son_guncelleme", ""))
            if son_guncelleme:
                try:
                    tarih = datetime.fromisoformat(son_guncelleme.replace("Z", "+00:00"))
                    gun_fark = (datetime.now(tarih.tzinfo) - tarih).days
                    if gun_fark < 90:
                        return 10
                    elif gun_fark < 180:
                        return 7
                    elif gun_fark < 365:
                        return 4
                    return 2
                except (ValueError, TypeError):
                    pass
            return 5  # Varsayilan

        if kriter_id == "yorum_analizi":
            puan = kurs.get("avg_rating", kurs.get("rating", kurs.get("ortalama_puan", 0)))
            if isinstance(puan, (int, float)):
                if puan >= 4.5:
                    return 9
                elif puan >= 4.0:
                    return 7
                elif puan >= 3.5:
                    return 5
                elif puan > 0:
                    return 3
            return 5

        # Diger kriterler icin varsayilan (veri olmadan tam puanlama yapilamaz)
        return 5
