"""Icerik uretim modulleri — 8 farkli icerik tipi."""

import json
from datetime import datetime
from pathlib import Path


class ContentGenerator:
    """Udemy kurs icerikleri uretir: baslik, aciklama, mufredat, script, quiz, proje, kaynak."""

    def generate_title(self, konu: str, hedef_kitle: str = "baslangic") -> str:
        """SEO uyumlu kurs basligi sablonu uret."""
        seviye_map = {
            "baslangic": "Sifirdan",
            "orta": "Uygulamali",
            "ileri": "Ileri Seviye",
        }
        seviye = seviye_map.get(hedef_kitle, "Kapsamli")
        return json.dumps({
            "baslik_onerileri": [
                f"{seviye} {konu} Kursu: A'dan Z'ye Uygulamali Egitim",
                f"{konu} Masterclass | {seviye} Baslangic Rehberi [2026]",
                f"{konu}: {seviye} Ogrenin + Gercek Projeler ile Pratik",
            ],
            "seo_ipuclari": [
                "60-80 karakter arasi tutun",
                "Ana anahtar kelimeyi basa yerlestirin",
                "Yil ekleyin (guncellik hissi)",
                "'Uygulamali', 'A-Z', 'Masterclass' gibi cekici kelimeler kullanin",
            ],
        }, ensure_ascii=False, indent=2)

    def generate_description(self, baslik: str, mufredat_ozeti: str = "") -> str:
        """Kurs aciklamasi sablonu uret."""
        return json.dumps({
            "aciklama_sablonu": f"""Bu kursta {baslik} konusunu sifirdan ileri seviyeye kadar ogreneceksiniz.

NELER OGRENECEKSINIZ:
- Temel kavramlar ve terminoloji
- Uygulamali projeler ile gercek dunya deneyimi
- En iyi pratikler ve profesyonel ipuclari
- Hata ayiklama ve problem cozme teknikleri

{f'MUFREDAT OZETI: {mufredat_ozeti}' if mufredat_ozeti else ''}

BU KURS KIME UYGUN?
- Konuya yeni baslayanlar
- Bilgilerini guncellemek isteyenler
- Kariyer degisikligi dusununler
- Uygulamali ogrenmeyi tercih edenler

NEDEN BU KURS?
- Tamamen Turkce icerik
- Gercek projeler ile pratik
- Omur boyu erisim + guncellemeler
- Sorulariniza hizli yanit""",
            "uzunluk_hedefi": "500-1000 karakter",
        }, ensure_ascii=False, indent=2)

    def generate_curriculum(self, konu: str, seviye: str = "baslangic", sure_saat: int = 5) -> dict:
        """Mufredat sablonu uret."""
        ders_sayisi = sure_saat * 6  # Saat basina ~6 ders (10dk ortalama)
        bolum_sayisi = max(5, sure_saat)

        return {
            "konu": konu,
            "seviye": seviye,
            "hedef_sure_saat": sure_saat,
            "tahmini_ders_sayisi": ders_sayisi,
            "bolum_sayisi": bolum_sayisi,
            "mufredat_sablonu": [
                {"bolum": 1, "baslik": f"Giris ve {konu} Temelleri",
                 "dersler": ["Kursa Hosgeldiniz", f"{konu} Nedir?", "Gelistirme Ortami Kurulumu",
                             "Ilk Uygulama", "Bolum Ozeti + Quiz"]},
                {"bolum": 2, "baslik": "Temel Kavramlar",
                 "dersler": ["Kavram 1: Teori", "Kavram 1: Pratik", "Kavram 2: Teori",
                             "Kavram 2: Pratik", "Mini Proje #1"]},
                {"bolum": 3, "baslik": "Orta Seviye Konular",
                 "dersler": ["Ileri Kavram 1", "Ileri Kavram 2", "Entegrasyon",
                             "Hata Ayiklama", "Mini Proje #2"]},
                {"bolum": 4, "baslik": "Uygulamali Proje",
                 "dersler": ["Proje Planlama", "Tasarim", "Gelistirme - 1",
                             "Gelistirme - 2", "Test ve Yayinlama"]},
                {"bolum": 5, "baslik": "Sonuc ve Ileri Adimlar",
                 "dersler": ["En Iyi Pratikler", "Kaynak Onerileri",
                             "Kariyer Ipuclari", "Final Testi", "Tebrikler!"]},
            ],
            "not": "Bu bir sablon. Konuya ozel derslerle doldurun.",
        }

    def generate_lecture_script(self, ders_basligi: str, sure_dakika: int = 10, dil: str = "tr") -> str:
        """Ders scripti sablonu."""
        kelime_sayisi = sure_dakika * 130  # Dakikada ~130 kelime (Turkce seslendirme)
        return json.dumps({
            "ders_basligi": ders_basligi,
            "hedef_sure": f"{sure_dakika} dakika",
            "hedef_kelime": kelime_sayisi,
            "dil": dil,
            "script_sablonu": {
                "giris": f"Merhaba! Bu derste {ders_basligi} konusunu inceleyecegiz. "
                         "Dersin sonunda ... yapabileceksiniz.",
                "ana_icerik": "[ANA ICERIK BURAYA — teori + ornek + demo]",
                "ozet": "Bu derste ogrendiklerimizi ozetleyelim: ...",
                "gecis": "Bir sonraki derste ... konusuna geciyoruz. Gorusmek uzere!",
            },
            "ipuclari": [
                "Ekran paylasimi ile canli demo gosterin",
                "Her 2-3 dakikada bir soru sorun veya ornek verin",
                "Turkce teknik terimlerin Ingilizcesini de belirtin",
            ],
        }, ensure_ascii=False, indent=2)

    def generate_quiz(self, konu: str, soru_sayisi: int = 5, zorluk: str = "orta") -> dict:
        """Quiz sablonu uret."""
        return {
            "konu": konu,
            "soru_sayisi": soru_sayisi,
            "zorluk": zorluk,
            "format": "Coktan secmeli (4 secenek, 1 dogru)",
            "sorular": [
                {
                    "soru_no": i + 1,
                    "soru": f"[{konu} ile ilgili soru {i + 1}]",
                    "secenekler": ["A) ...", "B) ...", "C) ...", "D) ..."],
                    "dogru_cevap": "A",
                    "aciklama": "[Neden bu cevap dogru — kisa aciklama]",
                }
                for i in range(soru_sayisi)
            ],
            "not": "Sablondaki [...] kisimlarini konuya ozel doldurun.",
        }

    def generate_project(self, konu: str, seviye: str = "baslangic") -> dict:
        """Proje tanimi sablonu."""
        return {
            "konu": konu,
            "seviye": seviye,
            "proje_sablonu": {
                "baslik": f"[{konu}] Uygulamali Proje",
                "hedef": "Bu projede ... uygulamasini sifirdan gelistireceksiniz.",
                "gereksinimler": ["Gereksinim 1", "Gereksinim 2", "Gereksinim 3"],
                "adimlar": [
                    "Adim 1: Proje yapisini olusturun",
                    "Adim 2: Temel fonksiyonlari kodlayin",
                    "Adim 3: UI/arayuz tasarlayin",
                    "Adim 4: Test edin",
                    "Adim 5: Dokumanlayin ve yayinlayin",
                ],
                "teslim_kriterleri": [
                    "Calisir durumda uygulama",
                    "Temiz ve yorumlanmis kod",
                    "README dosyasi",
                ],
                "tahmini_sure": "2-4 saat",
            },
        }

    def generate_resources(self, konu: str) -> dict:
        """Kaynak paketi sablonu."""
        return {
            "konu": konu,
            "kaynaklar": {
                "cheat_sheet": f"{konu} Hizli Referans Karti (PDF)",
                "kod_ornekleri": f"{konu} ornek kodlar (GitHub repo linki)",
                "ek_okuma": [
                    "Resmi dokumantasyon linki",
                    "Onerilen blog/makale listesi",
                    "YouTube kanal onerileri",
                ],
                "araclar": [
                    "Gelistirme ortami onerileri",
                    "Faydali eklentiler/uzantilar",
                    "Online deneme ortamlari",
                ],
            },
            "not": "Linkleri ve icerikleri konuya ozel doldurun.",
        }
