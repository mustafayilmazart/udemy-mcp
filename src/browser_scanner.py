"""Playwright Browser Otomasyon — Udemy kurs tarama modulu.

Bu modul Playwright MCP ile birlikte calisir. Claude, bu talimatlari
alip Playwright MCP araciligi ile browser'i kontrol eder.
Instructor panelinden ve ogrenci hesabindan ders ders icerik, altyazi, quiz tarar.

GUVENLIK: Tum tarama islemlerinde hiz siniri uygulanir.
Udemy'nin bot tespitinden kacinmak icin insan davranisi simule edilir.
"""

import json
from datetime import datetime
from pathlib import Path


class RateLimiter:
    """Udemy tarama hiz sinirleyici — bot tespitinden kacinma.

    Tum Playwright tarama talimatlarına otomatik bekleme suresi ekler.
    Modlar:
      - yavas (varsayilan): 4-7sn sayfa arasi, 45sn/10 sayfa, max 30/oturum
      - normal: 2-4sn sayfa arasi, 30sn/10 sayfa, max 50/oturum
      - hizli: 1-2sn sayfa arasi, 15sn/10 sayfa, max 100/oturum (riskli!)
    """

    MODLAR = {
        "yavas": {
            "sayfa_arasi_min": 4,
            "sayfa_arasi_max": 7,
            "mola_her_n_sayfa": 10,
            "mola_suresi_sn": 45,
            "oturum_max_sayfa": 30,
            "scroll_bekleme": 2,
            "aciklama": "Guvenli mod — insan hizinda tarama, ban riski yok",
        },
        "normal": {
            "sayfa_arasi_min": 2,
            "sayfa_arasi_max": 4,
            "mola_her_n_sayfa": 10,
            "mola_suresi_sn": 30,
            "oturum_max_sayfa": 50,
            "scroll_bekleme": 1,
            "aciklama": "Dengeli mod — makul hizda, dusuk risk",
        },
        "hizli": {
            "sayfa_arasi_min": 1,
            "sayfa_arasi_max": 2,
            "mola_her_n_sayfa": 15,
            "mola_suresi_sn": 15,
            "oturum_max_sayfa": 100,
            "scroll_bekleme": 0.5,
            "aciklama": "Hizli mod — RISKLI! Sadece kendi kurslariniz icin",
        },
    }

    def __init__(self, mod: str = "yavas"):
        self.mod = mod if mod in self.MODLAR else "yavas"
        self.ayarlar = self.MODLAR[self.mod]

    def guvenlik_talimatlari(self) -> list:
        """Playwright MCP'ye gonderilecek hiz siniri talimatlari."""
        a = self.ayarlar
        return [
            "",
            "=== GUVENLIK: HIZ SINIRI KURALLARI ===",
            f"MOD: {self.mod.upper()} — {a['aciklama']}",
            "",
            f"- Her sayfa gecisinden sonra {a['sayfa_arasi_min']}-{a['sayfa_arasi_max']} saniye BEKLE",
            f"  (rastgele sure sec, her seferinde farkli olsun)",
            f"- Her {a['mola_her_n_sayfa']} sayfada bir {a['mola_suresi_sn']} saniye MOLA ver",
            f"- Bir oturumda MAKSIMUM {a['oturum_max_sayfa']} sayfa tara, sonra dur",
            f"- Scroll islemlerinden sonra {a['scroll_bekleme']} saniye bekle",
            "- Sayfalar arasi rastgele mouse hareketi yap (insan simulasyonu)",
            "- Ayni sayfayi iki kez ZIYARET ETME",
            "- Hata alirsan (429, captcha, timeout) HEMEN DUR, kullaniciya bildir",
            "- Captcha cikarsa taramayi DURDUR ve kullaniciya haber ver",
            "",
            f"TOPLAM LIMIT: Bu oturumda en fazla {a['oturum_max_sayfa']} sayfa acilabilir.",
            "Limite ulasirsan 'Limit doldu, devam etmek icin yeni oturum baslatın' mesaji dondur.",
            "=== GUVENLIK SONU ===",
            "",
        ]

    def oturum_bilgisi(self) -> dict:
        """Oturum hiz siniri bilgilerini dict olarak dondur."""
        a = self.ayarlar
        return {
            "hiz_siniri_modu": self.mod,
            "sayfa_arasi_bekleme": f"{a['sayfa_arasi_min']}-{a['sayfa_arasi_max']} saniye",
            "mola": f"Her {a['mola_her_n_sayfa']} sayfada {a['mola_suresi_sn']} saniye",
            "oturum_limiti": f"Max {a['oturum_max_sayfa']} sayfa",
            "uyari": "Captcha veya 429 hatasi durumunda tarama otomatik durur",
        }


class BrowserScanner:
    """Udemy tarama talimatlari uretir — hiz sinirli ve guvenli."""

    def __init__(self, hiz_modu: str = "yavas"):
        self.limiter = RateLimiter(hiz_modu)

    def _talimat_ekle(self, adimlar: list) -> list:
        """Tum talimatlara hiz siniri kurallarini ekler."""
        return self.limiter.guvenlik_talimatlari() + adimlar

    def _sonuc_hazirla(self, data: dict) -> dict:
        """Sonuc dict'ine hiz siniri bilgilerini ekler."""
        data["guvenlik"] = self.limiter.oturum_bilgisi()
        if "adimlar" in data:
            data["adimlar"] = self._talimat_ekle(data["adimlar"])
        return data

    def __getattribute__(self, name):
        """Tum scan_ metodlarinin sonucuna otomatik hiz siniri ekler."""
        attr = super().__getattribute__(name)
        if name.startswith("scan_") and callable(attr):
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                if isinstance(result, dict):
                    return self._sonuc_hazirla(result)
                return result
            return wrapper
        return attr

    # Udemy CSS secicileri (instructor panel)
    SELECTORS = {
        # Instructor panel
        "kurs_listesi": "[data-purpose='course-card']",
        "kurs_baslik": "[data-purpose='course-title-link']",
        "kurs_ogrenci": "[data-purpose='course-students']",
        "kurs_rating": "[data-purpose='course-rating']",
        "kurs_gelir": "[data-purpose='course-revenue']",

        # Kurs duzenleme - mufredat
        "bolum_listesi": ".curriculum-section",
        "bolum_baslik": ".section-heading__title",
        "ders_listesi": ".curriculum-item",
        "ders_baslik": ".curriculum-item__title",
        "ders_sure": ".curriculum-item__content-length",
        "ders_tip": ".curriculum-item__type-icon",

        # Ders detay
        "video_player": "video",
        "altyazi_btn": "[data-purpose='captions-dropdown']",
        "altyazi_track": "track[kind='captions']",
        "transcript_panel": "[data-purpose='transcript-panel']",
        "transcript_text": "[data-purpose='transcript-cue-container']",

        # Quiz
        "quiz_container": ".assessment-container",
        "quiz_soru": ".assessment-question",
        "quiz_secenek": ".assessment-option",
        "quiz_cevap": ".assessment-answer",

        # Kurs onizleme (public sayfa)
        "mufredat_bolum": "[data-purpose='curriculum-section-container']",
        "mufredat_genislet": "[data-purpose='expand-toggle']",
        "toplam_ders": "[data-purpose='curriculum-stats']",
    }

    def scan_course(self, kurs_url: str) -> dict:
        """Tek kurs tarama talimati uret."""
        return {
            "islem": "kurs_tara",
            "url": kurs_url,
            "adimlar": [
                f"1. Playwright ile {kurs_url} adresini ac",
                "2. Sayfa yuklenene kadar bekle",
                "3. Kurs basligini oku (h1 veya [data-purpose='lead-title'])",
                "4. Kurs aciklamasini oku",
                "5. Mufredat bolumunu genislet (tum 'Show more' butonlarina tikla)",
                "6. Ders listesini oku: bolum adi, ders adi, ders suresi",
                "7. Egitmen bilgisini oku",
                "8. Yorum/rating bilgisini oku",
                "9. Tum veriyi JSON olarak dondur",
            ],
            "selectors": {
                "baslik": "h1, [data-purpose='lead-title']",
                "aciklama": "[data-purpose='lead-headline'], [data-purpose='safely-set-inner-html:description']",
                "mufredat": self.SELECTORS["mufredat_bolum"],
                "genislet": self.SELECTORS["mufredat_genislet"],
            },
            "cikti_formati": {
                "baslik": "str",
                "aciklama": "str",
                "egitmen": "str",
                "rating": "float",
                "ogrenci_sayisi": "int",
                "mufredat": [{"bolum": "str", "dersler": [{"ad": "str", "sure": "str", "tip": "str"}]}],
                "yorumlar": [{"yazar": "str", "puan": "int", "yorum": "str"}],
            },
        }

    def scan_instructor_dashboard(self) -> dict:
        """Instructor panel ana sayfa tarama — tum kurslari listele."""
        return {
            "islem": "instructor_dashboard_tara",
            "url": "https://www.udemy.com/instructor/courses/",
            "adimlar": [
                "1. Playwright ile https://www.udemy.com/instructor/courses/ adresine git",
                "2. Sayfa yuklenene kadar bekle (2-3 saniye)",
                "3. Eger giris sayfasina yonlendirildiyse, kullanicinin zaten giris yapmis olmasi gerekir — hata dondur",
                "4. Sayfadaki tum kurs kartlarini bul",
                "5. Her kurs icin su bilgileri oku:",
                "   - Kurs basligi ve URL'si",
                "   - Ogrenci sayisi",
                "   - Ortalama puan",
                "   - Durum (yayinda/taslak)",
                "6. Tum kurslari JSON dizisi olarak dondur",
            ],
            "selectors": self.SELECTORS,
            "cikti_formati": {
                "kurslar": [{
                    "baslik": "str",
                    "url": "str",
                    "ogrenci_sayisi": "int",
                    "rating": "float",
                    "durum": "str",
                }]
            },
        }

    def scan_course_curriculum_deep(self, kurs_manage_url: str) -> dict:
        """Instructor panelden kursun mufredatini derinlemesine tara.
        Her bolum, her ders, ders tipi (video/quiz/makale), sure bilgisi."""
        return {
            "islem": "mufredat_derin_tara",
            "url": kurs_manage_url,
            "adimlar": [
                f"1. Playwright ile {kurs_manage_url} adresine git",
                "2. Sol menuden 'Curriculum' / 'Mufredat' sekmesine tikla",
                "3. Sayfa tamamen yuklenene kadar bekle",
                "4. Tum bolumleri (Section) listele",
                "5. Her bolum icin:",
                "   a. Bolum basligini oku",
                "   b. Bolumdeki tum dersleri listele",
                "   c. Her ders icin: baslik, tip (Video/Quiz/Article/Assignment), sure",
                "   d. Ders tipini ikondan veya etiketten belirle",
                "6. Her bolumun altindaki quiz'leri ayri isaretle",
                "7. Coding exercise varsa belirt",
                "8. Tum yapiyi JSON olarak dondur",
            ],
            "cikti_formati": {
                "kurs_adi": "str",
                "toplam_bolum": "int",
                "toplam_ders": "int",
                "toplam_sure": "str",
                "bolumler": [{
                    "sira": "int",
                    "baslik": "str",
                    "ders_sayisi": "int",
                    "dersler": [{
                        "sira": "int",
                        "baslik": "str",
                        "tip": "Video | Quiz | Article | Assignment | Coding Exercise",
                        "sure": "str (dakika:saniye)",
                        "onizleme": "bool",
                    }]
                }]
            },
        }

    def scan_lecture_content(self, ders_url: str) -> dict:
        """Tek bir dersin icerigini tara — video, altyazi, kaynaklar."""
        return {
            "islem": "ders_icerik_tara",
            "url": ders_url,
            "adimlar": [
                f"1. Playwright ile {ders_url} adresine git",
                "2. Ders sayfasi yuklenene kadar bekle",
                "3. Ders basligini oku",
                "4. Video suresi bilgisini oku",
                "5. Altyazi/transcript varsa:",
                "   a. Transcript panelini ac (varsa)",
                "   b. Tum transcript metnini oku",
                "   c. Altyazi dillerini listele",
                "6. Ders aciklamasi/notu varsa oku",
                "7. Indirilebilir kaynaklar varsa listele",
                "8. JSON olarak dondur",
            ],
            "cikti_formati": {
                "ders_basligi": "str",
                "sure": "str",
                "tip": "str",
                "transcript": "str (tam metin)",
                "altyazi_dilleri": ["str"],
                "ders_notu": "str",
                "kaynaklar": [{"ad": "str", "tip": "str"}],
            },
        }

    def scan_lecture_subtitles(self, ders_url: str) -> dict:
        """Dersin altyazilarini/transcript'ini tam metin olarak cek."""
        return {
            "islem": "altyazi_tara",
            "url": ders_url,
            "adimlar": [
                f"1. Playwright ile {ders_url} adresine git",
                "2. Video player'in yuklenmesini bekle",
                "3. Transcript/altyazi panelini ac:",
                "   - 'Transcript' butonuna tikla veya",
                "   - CC (Closed Captions) butonuna tikla",
                "4. Transcript panelindeki tum metni oku",
                "   - Her satirda zaman damgasi ve metin var",
                "   - Hepsini birlestir",
                "5. Eger transcript paneli yoksa:",
                "   - Video elementindeki <track> etiketlerini kontrol et",
                "   - .vtt dosya URL'sini bul ve icerigini cek",
                "6. Tam transcript metnini dondur",
            ],
            "cikti_formati": {
                "ders_basligi": "str",
                "dil": "str",
                "transcript": "str (tam metin, zaman damgalari haric)",
                "transcript_zamanli": [{"zaman": "str", "metin": "str"}],
                "kaynak": "panel | vtt_dosya",
            },
        }

    def scan_quiz_detail(self, quiz_url: str) -> dict:
        """Quiz/test icerigini tara — sorular, secenekler, dogru cevaplar."""
        return {
            "islem": "quiz_tara",
            "url": quiz_url,
            "adimlar": [
                f"1. Playwright ile {quiz_url} adresine git (instructor panel)",
                "2. Quiz duzenleme sayfasini ac",
                "3. Tum sorulari listele",
                "4. Her soru icin:",
                "   a. Soru metnini oku",
                "   b. Soru tipini belirle (coktan secmeli, dogru/yanlis, vs)",
                "   c. Tum secenekleri oku",
                "   d. Dogru cevabi isaretle",
                "   e. Aciklama/feedback metnini oku",
                "5. Tum quiz verisini JSON olarak dondur",
            ],
            "cikti_formati": {
                "quiz_basligi": "str",
                "soru_sayisi": "int",
                "sorular": [{
                    "sira": "int",
                    "soru": "str",
                    "tip": "coktan_secmeli | dogru_yanlis | eslestirme",
                    "secenekler": ["str"],
                    "dogru_cevap": "str",
                    "aciklama": "str",
                }]
            },
        }

    def scan_assignment_detail(self, odev_url: str) -> dict:
        """Odev/assignment detayini tara."""
        return {
            "islem": "odev_tara",
            "url": odev_url,
            "adimlar": [
                f"1. Playwright ile {odev_url} adresine git",
                "2. Odev baslik ve aciklamasini oku",
                "3. Talimat metnini tam olarak oku",
                "4. Eklenmis kaynak dosyalari listele",
                "5. Degerlendirme kriterlerini oku (varsa)",
                "6. JSON olarak dondur",
            ],
            "cikti_formati": {
                "odev_basligi": "str",
                "aciklama": "str",
                "talimatlar": "str",
                "kaynaklar": [{"ad": "str"}],
                "degerlendirme_kriterleri": ["str"],
            },
        }

    def scan_full_course_deep(self, kurs_slug: str) -> dict:
        """Tum kursu derinlemesine tara — her ders, altyazi, quiz dahil.
        Bu kapsamli bir tarama, kurs slug'ini alir ve her seyi tarar."""
        base = f"https://www.udemy.com/course/{kurs_slug}/manage"
        learn = f"https://www.udemy.com/course/{kurs_slug}/learn"
        return {
            "islem": "tam_kurs_tara",
            "kurs_slug": kurs_slug,
            "urls": {
                "manage": base,
                "curriculum": f"{base}/curriculum",
                "learn": learn,
            },
            "adimlar": [
                "=== ADIM 1: GENEL BILGI ===",
                f"1. {base}/basics adresine git",
                "2. Kurs basligi, alt baslik, aciklama, kategori, dil bilgilerini oku",
                "",
                "=== ADIM 2: MUFREDAT YAPISI ===",
                f"3. {base}/curriculum adresine git",
                "4. Tum bolumleri ve dersleri listele (baslik, tip, sure)",
                "5. Quiz ve odevleri isaretle",
                "",
                "=== ADIM 3: HER DERSIN ICERIGI ===",
                f"6. {learn}/lecture/DERS_ID formatinda her derse gir",
                "7. Her ders icin:",
                "   a. Video suresi",
                "   b. Transcript/altyazi panelini ac ve tam metni cek",
                "   c. Ders notu/aciklamasini oku",
                "   d. Ek kaynaklari listele",
                "",
                "=== ADIM 4: QUIZLER ===",
                "8. Her quiz icin:",
                "   a. Soru metinlerini oku",
                "   b. Secenekleri ve dogru cevaplari oku",
                "   c. Aciklamalari oku",
                "",
                "=== ADIM 5: ODEVLER ===",
                "9. Her assignment icin:",
                "   a. Talimat metnini oku",
                "   b. Degerlendirme kriterlerini oku",
                "",
                "=== ADIM 6: KAYDET ===",
                "10. Tum veriyi data/courses/KURS_SLUG_full.json olarak kaydet",
            ],
            "cikti_formati": {
                "kurs_adi": "str",
                "kurs_slug": "str",
                "genel_bilgi": {
                    "baslik": "str",
                    "alt_baslik": "str",
                    "aciklama": "str",
                    "kategori": "str",
                    "dil": "str",
                },
                "mufredat": [{
                    "bolum_sira": "int",
                    "bolum_baslik": "str",
                    "dersler": [{
                        "sira": "int",
                        "baslik": "str",
                        "tip": "Video | Quiz | Article | Assignment",
                        "sure": "str",
                        "transcript": "str (altyazi metni)",
                        "ders_notu": "str",
                        "kaynaklar": ["str"],
                        "quiz_sorulari": [{
                            "soru": "str",
                            "secenekler": ["str"],
                            "dogru_cevap": "str",
                        }],
                    }]
                }],
                "toplam_istatistik": {
                    "bolum_sayisi": "int",
                    "video_sayisi": "int",
                    "quiz_sayisi": "int",
                    "odev_sayisi": "int",
                    "toplam_sure": "str",
                    "transcript_kelime_sayisi": "int",
                },
            },
        }

    # ── OGRENCI TARAFI TARAMA ARACLARI ──────────────────────────────

    def scan_my_enrolled_courses(self) -> dict:
        """Ogrenci hesabindaki satin alinmis kurslari listele."""
        return {
            "islem": "kayitli_kurslar_tara",
            "url": "https://www.udemy.com/home/my-courses/learning/",
            "adimlar": [
                "1. Playwright ile https://www.udemy.com/home/my-courses/learning/ adresine git",
                "2. Sayfa yuklenene kadar bekle (2-3 saniye)",
                "3. Eger giris sayfasina yonlendirildiyse — kullanicinin oturumu acik degil, hata dondur",
                "4. Sayfadaki tum kurs kartlarini bul",
                "5. Sayfa sonuna kadar scroll yap (lazy loading ile tum kurslar yuklensin)",
                "6. Her kurs icin su bilgileri oku:",
                "   - Kurs basligi",
                "   - Kurs URL'si (slug'i cikar)",
                "   - Egitmen adi",
                "   - Ilerleme yuzde (% tamamlandi)",
                "   - Son erisim tarihi",
                "   - Kurs gorseli",
                "7. Toplam kurs sayisini belirt",
                "8. 'Tum Kurslar', 'Listelerim', 'Arsivlenmis' sekmeleri varsa hepsini tara",
                "9. JSON olarak dondur",
            ],
            "cikti_formati": {
                "toplam_kurs": "int",
                "kurslar": [{
                    "baslik": "str",
                    "url": "str",
                    "slug": "str",
                    "egitmen": "str",
                    "ilerleme_yuzde": "int",
                    "son_erisim": "str",
                }]
            },
        }

    def scan_enrolled_course_content(self, kurs_slug: str) -> dict:
        """Ogrenci olarak kayitli olunan kursun icerigini tara.
        Ders listesi, altyazi, quiz — ogrenci gorunumunden."""
        learn_url = f"https://www.udemy.com/course/{kurs_slug}/learn"
        return {
            "islem": "ogrenci_kurs_icerik_tara",
            "url": learn_url,
            "kurs_slug": kurs_slug,
            "adimlar": [
                f"1. Playwright ile {learn_url} adresine git",
                "2. Sol paneldeki mufredat listesinin yuklenmesini bekle",
                "3. Sol paneli (sidebar) ac (kapali ise)",
                "4. Tum bolum basliklarini genislet (expand)",
                "5. Her bolum icin:",
                "   a. Bolum basligini oku",
                "   b. Bolumdeki tum dersleri listele",
                "   c. Her ders icin:",
                "      - Ders basligi",
                "      - Ders tipi (video ikonu, dosya ikonu, quiz ikonu vs)",
                "      - Ders suresi",
                "      - Tamamlandi mi? (checkmark var mi)",
                "      - Ders URL'si / ID'si (tiklanabilir linkten cikar)",
                "6. Tum yapiyi JSON olarak dondur",
            ],
            "cikti_formati": {
                "kurs_adi": "str",
                "kurs_slug": "str",
                "toplam_bolum": "int",
                "toplam_ders": "int",
                "tamamlanma_orani": "int (%)",
                "bolumler": [{
                    "sira": "int",
                    "baslik": "str",
                    "ders_sayisi": "int",
                    "dersler": [{
                        "sira": "int",
                        "baslik": "str",
                        "tip": "Video | Quiz | Article | Assignment | Coding Exercise",
                        "sure": "str",
                        "tamamlandi": "bool",
                        "ders_id": "str",
                    }]
                }]
            },
        }

    def scan_enrolled_lecture(self, kurs_slug: str, ders_id: str) -> dict:
        """Ogrenci olarak kayitli olunan kursta tek ders icerigini tara."""
        ders_url = f"https://www.udemy.com/course/{kurs_slug}/learn/lecture/{ders_id}"
        return {
            "islem": "ogrenci_ders_tara",
            "url": ders_url,
            "adimlar": [
                f"1. Playwright ile {ders_url} adresine git",
                "2. Video player'in yuklenmesini bekle",
                "3. Ders basligini oku (ust kisimdan)",
                "4. Video suresi bilgisini oku",
                "5. Transcript/altyazi islemleri:",
                "   a. Video altindaki 'Transcript' sekmesine tikla",
                "   b. Transcript paneli actiysa tum metni oku",
                "   c. Transcript yoksa, video player'daki CC butonuna tikla",
                "   d. Altyazi dillerini listele",
                "   e. Altyazi metnini satirlar halinde oku",
                "6. 'Notes' / 'Notlar' sekmesini kontrol et",
                "7. 'Resources' / 'Kaynaklar' sekmesini kontrol et:",
                "   - Indirilebilir dosyalari listele",
                "   - Harici linkleri listele",
                "8. 'Overview' / 'Genel Bakis' sekmesini kontrol et:",
                "   - Ders aciklamasini oku",
                "9. JSON olarak dondur",
            ],
            "cikti_formati": {
                "ders_basligi": "str",
                "ders_id": "str",
                "sure": "str",
                "tip": "str",
                "transcript": "str (tam metin)",
                "altyazi_dilleri": ["str"],
                "ders_aciklamasi": "str",
                "kaynaklar": [{"ad": "str", "tip": "dosya | link", "url": "str"}],
                "notlarim": "str",
            },
        }

    def scan_enrolled_lecture_subtitles(self, kurs_slug: str, ders_id: str) -> dict:
        """Ogrenci olarak izlenen dersin altyazi/transcript metnini cek."""
        ders_url = f"https://www.udemy.com/course/{kurs_slug}/learn/lecture/{ders_id}"
        return {
            "islem": "ogrenci_altyazi_cek",
            "url": ders_url,
            "adimlar": [
                f"1. Playwright ile {ders_url} adresine git",
                "2. Video player'in yuklenmesini bekle",
                "3. Video altindaki sekmelerde 'Transcript' sekmesine tikla",
                "4. Eger Transcript sekmesi varsa:",
                "   a. Tum transcript satirlarini oku",
                "   b. Her satirdaki zaman damgasi + metni al",
                "   c. Sayfa sonuna kadar scroll yap (tum transcript yuklensin)",
                "5. Eger Transcript sekmesi yoksa:",
                "   a. Video player'daki CC/altyazi butonuna tikla",
                "   b. Mevcut dilleri listele",
                "   c. Turkce altyazi varsa sec, yoksa Ingilizce sec",
                "   d. Sayfanin HTML'inde <track> elementlerini ara",
                "   e. .vtt dosya URL'sini bul ve icerigini fetch et",
                "6. Altyazi metnini birlestirip temiz metin olarak dondur",
                "7. Hem zamanli hem zamansiz versiyonu dondur",
            ],
            "cikti_formati": {
                "ders_basligi": "str",
                "ders_id": "str",
                "dil": "str",
                "mevcud_diller": ["str"],
                "transcript_temiz": "str (sadece metin, zaman damgasi yok)",
                "transcript_zamanli": [{"zaman": "00:00:00", "metin": "str"}],
                "kelime_sayisi": "int",
                "kaynak": "transcript_sekmesi | vtt_dosya | cc_butonu",
            },
        }

    def scan_enrolled_quiz(self, kurs_slug: str, quiz_id: str) -> dict:
        """Ogrenci olarak kayitli kursta quiz/test icerigini tara."""
        quiz_url = f"https://www.udemy.com/course/{kurs_slug}/learn/quiz/{quiz_id}"
        return {
            "islem": "ogrenci_quiz_tara",
            "url": quiz_url,
            "adimlar": [
                f"1. Playwright ile {quiz_url} adresine git",
                "2. Quiz sayfasinin yuklenmesini bekle",
                "3. 'Start Quiz' / 'Teste Basla' butonuna tikla (henuz baslamadiysa)",
                "4. Her soru icin:",
                "   a. Soru metnini oku",
                "   b. Tum secenekleri oku",
                "   c. Soru tipini belirle (coktan secmeli, cok cevapli, dogru/yanlis)",
                "   d. Bir secenek sec ve 'Check Answer' / 'Cevabi Kontrol Et' tikla",
                "   e. Dogru cevabi ve aciklamayi oku",
                "   f. Sonraki soruya gec",
                "5. Tum sorulari topla",
                "6. Quiz sonuc ekranindaki puani oku",
                "7. JSON olarak dondur",
                "",
                "NOT: Quiz'i bozmamak icin dikkatli ol.",
                "Eger quiz daha once cozulmusse 'Retry' ile tekrar baslat.",
            ],
            "cikti_formati": {
                "quiz_basligi": "str",
                "quiz_id": "str",
                "soru_sayisi": "int",
                "sorular": [{
                    "sira": "int",
                    "soru": "str",
                    "tip": "coktan_secmeli | cok_cevapli | dogru_yanlis",
                    "secenekler": ["str"],
                    "dogru_cevap": "str | [str]",
                    "aciklama": "str",
                }],
                "sonuc_puan": "str",
            },
        }

    def scan_enrolled_full_course(self, kurs_slug: str) -> dict:
        """Ogrenci hesabindaki kursu bastan sona tara — her ders, altyazi, quiz dahil."""
        learn_url = f"https://www.udemy.com/course/{kurs_slug}/learn"
        return {
            "islem": "ogrenci_tam_kurs_tara",
            "kurs_slug": kurs_slug,
            "url": learn_url,
            "adimlar": [
                "=== ADIM 1: KURS GENEL BILGI ===",
                f"1. {learn_url} adresine git",
                "2. Kurs basligini, egitmen adini oku",
                "3. Ilerleme durumunu (% tamamlandi) oku",
                "",
                "=== ADIM 2: MUFREDAT YAPISI ===",
                "4. Sol paneldeki tum bolumleri genislet",
                "5. Her bolum ve ders icin: baslik, tip, sure, tamamlandi mi",
                "6. Tum ders ID'lerini topla",
                "",
                "=== ADIM 3: HER DERSIN DETAYI ===",
                "7. Her video derse tek tek gir:",
                "   a. Transcript sekmesini ac, tam metni cek",
                "   b. Kaynaklar sekmesini kontrol et",
                "   c. Ders aciklamasini oku",
                "   d. Sonraki derse gec",
                "",
                "=== ADIM 4: QUIZLER ===",
                "8. Her quiz'e gir:",
                "   a. Sorulari, secenekleri, dogru cevaplari oku",
                "   b. Aciklamalari oku",
                "",
                "=== ADIM 5: CODING EXERCISE / ODEVLER ===",
                "9. Coding exercise varsa:",
                "   a. Problem tanimini oku",
                "   b. Baslangic kodunu oku",
                "   c. Beklenen ciktiyi oku",
                "",
                "=== ADIM 6: KAYDET ===",
                "10. Tum veriyi JSON olarak kaydet",
                "11. Ogrenci perspektifinden notlar ekle:",
                "    - Hangi dersler tamamlandi",
                "    - Toplam ilerleme",
                "    - Quiz sonuclari",
            ],
            "cikti_formati": {
                "kurs_adi": "str",
                "kurs_slug": "str",
                "egitmen": "str",
                "ilerleme_yuzde": "int",
                "mufredat": [{
                    "bolum_sira": "int",
                    "bolum_baslik": "str",
                    "dersler": [{
                        "sira": "int",
                        "baslik": "str",
                        "tip": "Video | Quiz | Article | Assignment | Coding Exercise",
                        "sure": "str",
                        "tamamlandi": "bool",
                        "ders_id": "str",
                        "transcript": "str (altyazi metni — sadece videolar icin)",
                        "kaynaklar": [{"ad": "str", "url": "str"}],
                        "quiz_sorulari": [{
                            "soru": "str",
                            "secenekler": ["str"],
                            "dogru_cevap": "str",
                            "aciklama": "str",
                        }],
                        "coding_exercise": {
                            "problem": "str",
                            "baslangic_kodu": "str",
                            "beklenen_cikti": "str",
                        },
                    }]
                }],
                "toplam_istatistik": {
                    "bolum_sayisi": "int",
                    "video_sayisi": "int",
                    "quiz_sayisi": "int",
                    "odev_sayisi": "int",
                    "toplam_sure": "str",
                    "tamamlanan_ders": "int",
                    "kalan_ders": "int",
                    "transcript_kelime_sayisi": "int",
                },
            },
        }

    def scan_course_reviews_page(self, kurs_slug: str) -> dict:
        """Kursun public sayfasindan yorumlari tara."""
        url = f"https://www.udemy.com/course/{kurs_slug}/"
        return {
            "islem": "yorum_sayfasi_tara",
            "url": url,
            "adimlar": [
                f"1. Playwright ile {url} adresine git",
                "2. Yorumlar bolumune scroll yap",
                "3. 'Show more reviews' butonuna tiklayarak daha fazla yorum yukle (5-10 kez)",
                "4. Her yorum icin:",
                "   a. Yazar adi",
                "   b. Yildiz puani (1-5)",
                "   c. Yorum tarihi",
                "   d. Yorum metni",
                "   e. Faydali bulma sayisi",
                "5. Ortalama puan ve yorum sayisini oku",
                "6. Puan dagilimini oku (5 yildiz: %X, 4 yildiz: %Y, ...)",
                "7. JSON olarak dondur",
            ],
            "cikti_formati": {
                "kurs_adi": "str",
                "ortalama_puan": "float",
                "toplam_yorum": "int",
                "puan_dagilimi": {"5": "int%", "4": "int%", "3": "int%", "2": "int%", "1": "int%"},
                "yorumlar": [{
                    "yazar": "str",
                    "puan": "int",
                    "tarih": "str",
                    "yorum": "str",
                    "faydali": "int",
                }],
            },
        }

    def scan_instructor_panel(self) -> dict:
        """Instructor panel tarama talimati (eski uyumluluk)."""
        return self.scan_instructor_dashboard()

    def scan_competitors(self, anahtar_kelime: str, limit: int = 5) -> dict:
        """Rakip kurs tarama talimati."""
        return {
            "islem": "rakip_tara",
            "url": f"https://www.udemy.com/courses/search/?q={anahtar_kelime}&lang=tr",
            "limit": limit,
            "adimlar": [
                f"1. Playwright ile Udemy'de '{anahtar_kelime}' ara",
                f"2. Ilk {limit} kursu listele",
                "3. Her kurs icin: baslik, egitmen, puan, ogrenci sayisi, fiyat",
                "4. Her kursun mufredat onizlemesini oku",
                "5. Karsilastirmali tablo olustur",
            ],
        }

    def update_course(self, kurs_id: str, degisiklikler: dict) -> dict:
        """Kurs guncelleme talimati."""
        return {
            "islem": "kurs_guncelle",
            "url": f"https://www.udemy.com/course/{kurs_id}/manage/basics/",
            "degisiklikler": degisiklikler,
            "adimlar": [
                "1. Playwright ile kurs duzenleme sayfasina git",
                f"2. Degisiklikleri uygula: {json.dumps(degisiklikler, ensure_ascii=False)}",
                "3. Her degisiklikten sonra 'Kaydet' butonuna tikla",
                "4. Basarili kaydedildigini dogrula",
            ],
        }
