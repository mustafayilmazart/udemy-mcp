"""Udemy MCP - Egitim Icerik Pipeline Ana Sunucu"""

import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP

from api_client import UdemyAPIClient
from browser_scanner import BrowserScanner
from content_analyzer import ContentAnalyzer
from content_generator import ContentGenerator
from improvement_engine import ImprovementEngine

# .env yukle
load_dotenv(Path(__file__).parent.parent / "config" / ".env")

DATA_DIR = Path(os.getenv("DATA_DIR", Path(__file__).parent.parent / "data"))

mcp = FastMCP(
    "udemy-mcp",
    instructions="Udemy Egitim Icerik Pipeline - Tara, Analiz Et, Iyilestir, Uret, Uygula",
)

api = UdemyAPIClient()
# Hiz modu: "yavas" (guvenli), "normal" (dengeli), "hizli" (riskli)
scanner = BrowserScanner(hiz_modu=os.getenv("UDEMY_HIZ_MODU", "yavas"))
analyzer = ContentAnalyzer()
generator = ContentGenerator()
improver = ImprovementEngine()


# ── 1. TARAMA ARACLARI ──────────────────────────────────────────

@mcp.tool()
async def udemy_kurs_tara(kurs_url: str) -> str:
    """Playwright ile Udemy kursunu tarar, icerigini JSON olarak kaydeder.
    Browser MCP'ye 'kurs_url' adresini acip icerik okuma istegi gonderir."""
    return json.dumps({
        "durum": "hazir",
        "talimat": f"Playwright MCP ile su adresi ac: {kurs_url}\n"
                   "Sayfadaki mufredat, ders listesi, aciklama, "
                   "egitmen bilgisi ve yorumlari oku.\n"
                   "Sonuclari JSON olarak data/courses/ altina kaydet.",
        "kayit_dizini": str(DATA_DIR / "courses"),
    }, ensure_ascii=False)


@mcp.tool()
async def udemy_api_kurslarim() -> str:
    """Udemy Instructor API ile kendi kurslarimi listeler."""
    result = await api.get_courses()
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_api_yorumlar(kurs_id: str) -> str:
    """Belirtilen kursun yorumlarini API'den ceker."""
    result = await api.get_reviews(kurs_id)
    # Yorumlari kaydet
    kayit = DATA_DIR / "reviews" / f"{kurs_id}_reviews.json"
    kayit.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return json.dumps(result, ensure_ascii=False, indent=2)


# ── 1B. DERINLEMESINE TARAMA ARACLARI (Playwright MCP) ─────────

@mcp.tool()
async def udemy_instructor_panel_tara() -> str:
    """Instructor paneldeki tum kurslari listeler.
    Tarayicida Udemy hesabiniz acik olmali. Playwright MCP ile panele girer."""
    talimat = scanner.scan_instructor_dashboard()
    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Asagidaki talimatlari Playwright MCP ile adim adim uygula",
        **talimat,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_mufredat_tara(kurs_slug: str) -> str:
    """Kursun mufredatini derinlemesine tarar — her bolum, ders, tip, sure.
    kurs_slug: Kursun URL'sindeki isim (ornek: 'python-sifirdan-ileri')
    Tarayicida Udemy hesabiniz acik olmali."""
    manage_url = f"https://www.udemy.com/course/{kurs_slug}/manage/curriculum"
    talimat = scanner.scan_course_curriculum_deep(manage_url)
    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Instructor panelden mufredat yapisini tara",
        **talimat,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_ders_icerik_tara(kurs_slug: str, ders_id: str) -> str:
    """Tek bir dersin icerigini tarar — video, altyazi/transcript, kaynaklar.
    kurs_slug: Kursun URL slug'i
    ders_id: Dersin ID'si (URL'den alinir)
    Tarayicida Udemy hesabiniz acik olmali."""
    ders_url = f"https://www.udemy.com/course/{kurs_slug}/learn/lecture/{ders_id}"
    talimat = scanner.scan_lecture_content(ders_url)
    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Ders sayfasina gir, video/altyazi/kaynak bilgilerini cek",
        **talimat,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_altyazi_cek(kurs_slug: str, ders_id: str) -> str:
    """Dersin altyazi/transcript metnini tam olarak ceker.
    kurs_slug: Kursun URL slug'i
    ders_id: Dersin ID'si
    Tarayicida Udemy hesabiniz acik olmali."""
    ders_url = f"https://www.udemy.com/course/{kurs_slug}/learn/lecture/{ders_id}"
    talimat = scanner.scan_lecture_subtitles(ders_url)
    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Ders videosunun transcript/altyazi metnini cek",
        **talimat,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_quiz_tara(kurs_slug: str, quiz_id: str) -> str:
    """Quiz/test icerigini tarar — sorular, secenekler, dogru cevaplar.
    kurs_slug: Kursun URL slug'i
    quiz_id: Quiz ID'si
    Tarayicida Udemy hesabiniz acik olmali."""
    quiz_url = f"https://www.udemy.com/course/{kurs_slug}/manage/quizzes/{quiz_id}"
    talimat = scanner.scan_quiz_detail(quiz_url)
    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Quiz duzenleme sayfasindan tum soru ve cevaplari cek",
        **talimat,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_tam_kurs_tara(kurs_slug: str) -> str:
    """Tum kursu bastan sona derinlemesine tarar.
    Her bolum, her ders, altyazilar, quizler, odevler dahil.
    kurs_slug: Kursun URL slug'i (ornek: 'python-sifirdan-ileri')
    Tarayicida Udemy hesabiniz acik olmali.
    DIKKAT: Bu kapsamli bir tarama, uzun surebilir."""
    talimat = scanner.scan_full_course_deep(kurs_slug)

    # Kayit dizinlerini olustur
    for alt in ["courses", "analysis", "improvements", "generated", "reviews"]:
        (DATA_DIR / alt).mkdir(parents=True, exist_ok=True)

    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Tum kursu bastan sona tara: mufredat, dersler, altyazilar, quizler, odevler",
        "kayit_dizini": str(DATA_DIR / "courses"),
        "kayit_dosyasi": f"{kurs_slug}_full.json",
        **talimat,
    }, ensure_ascii=False, indent=2)


# ── 1C. OGRENCI HESABI TARAMA ARACLARI (Playwright MCP) ────────

@mcp.tool()
async def udemy_kayitli_kurslarim() -> str:
    """Ogrenci hesabindaki satin alinmis tum kurslari listeler.
    Tarayicida Udemy ogrenci hesabiniz acik olmali.
    My Courses sayfasini tarar: baslik, egitmen, ilerleme durumu."""
    talimat = scanner.scan_my_enrolled_courses()
    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Ogrenci hesabindaki kayitli kurslari listele",
        **talimat,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_ogrenci_kurs_tara(kurs_slug: str) -> str:
    """Ogrenci olarak kayitli olunan kursun mufredat yapisini tarar.
    kurs_slug: Kursun URL slug'i (ornek: 'react-the-complete-guide')
    Sol panelden tum bolum ve dersleri, tipleri, sureleri listeler.
    Tarayicida Udemy hesabiniz acik olmali."""
    talimat = scanner.scan_enrolled_course_content(kurs_slug)
    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Ogrenci gorunumunden kursun mufredat yapisini tara",
        **talimat,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_ogrenci_ders_tara(kurs_slug: str, ders_id: str) -> str:
    """Ogrenci olarak kayitli kursta tek ders icerigini tarar.
    Video, transcript/altyazi, kaynaklar, ders aciklamasi.
    kurs_slug: Kursun URL slug'i
    ders_id: Dersin ID'si
    Tarayicida Udemy hesabiniz acik olmali."""
    talimat = scanner.scan_enrolled_lecture(kurs_slug, ders_id)
    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Ogrenci gorunumunden tek ders icerigini tara",
        **talimat,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_ogrenci_altyazi_cek(kurs_slug: str, ders_id: str) -> str:
    """Ogrenci olarak izlenen dersin altyazi/transcript metnini ceker.
    kurs_slug: Kursun URL slug'i
    ders_id: Dersin ID'si
    Transcript sekmesi veya CC butonundan altyazi metnini alir.
    Tarayicida Udemy hesabiniz acik olmali."""
    talimat = scanner.scan_enrolled_lecture_subtitles(kurs_slug, ders_id)
    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Ogrenci gorunumunden ders altyazi/transcript cek",
        **talimat,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_ogrenci_quiz_tara(kurs_slug: str, quiz_id: str) -> str:
    """Ogrenci olarak kayitli kursta quiz/test icerigini tarar.
    Sorulari, secenekleri ve dogru cevaplari okur.
    kurs_slug: Kursun URL slug'i
    quiz_id: Quiz ID'si
    Tarayicida Udemy hesabiniz acik olmali."""
    talimat = scanner.scan_enrolled_quiz(kurs_slug, quiz_id)
    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Ogrenci gorunumunden quiz soru ve cevaplarini tara",
        **talimat,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_ogrenci_tam_kurs_tara(kurs_slug: str) -> str:
    """Ogrenci hesabindaki kursu BASTAN SONA derinlemesine tarar.
    Her ders, altyazi, quiz, coding exercise, odev — hepsi dahil.
    kurs_slug: Kursun URL slug'i (ornek: 'react-the-complete-guide')
    Tarayicida Udemy hesabiniz acik olmali.
    DIKKAT: Kapsamli tarama, kurs buyuklugune gore uzun surebilir."""
    talimat = scanner.scan_enrolled_full_course(kurs_slug)

    for alt in ["courses", "analysis", "improvements", "generated", "reviews"]:
        (DATA_DIR / alt).mkdir(parents=True, exist_ok=True)

    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Ogrenci gorunumunden tum kursu bastan sona tara",
        "kayit_dizini": str(DATA_DIR / "courses"),
        "kayit_dosyasi": f"{kurs_slug}_ogrenci_full.json",
        **talimat,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_yorum_tara(kurs_slug: str) -> str:
    """Kursun public sayfasindan yorumlari tarar.
    Puan dagilimi, yorum metinleri, ortalama puan.
    kurs_slug: Kursun URL slug'i
    Giris yapmis olmak gerekmez, public sayfa."""
    talimat = scanner.scan_course_reviews_page(kurs_slug)
    return json.dumps({
        "durum": "playwright_mcp_ile_calistir",
        "aciklama": "Kursun public sayfasindan yorumlari ve puanlari tara",
        **talimat,
    }, ensure_ascii=False, indent=2)


# ── 2. ANALIZ ARACLARI ──────────────────────────────────────────

@mcp.tool()
async def udemy_analiz(kurs_verisi: str) -> str:
    """Kurs verisini 10 kriter ile analiz eder, /100 puan verir.
    kurs_verisi: JSON string veya data/courses/ altindaki dosya adi."""
    # Dosya adi verilmisse oku
    veri_yolu = DATA_DIR / "courses" / kurs_verisi
    if veri_yolu.exists():
        kurs = json.loads(veri_yolu.read_text(encoding="utf-8"))
    else:
        kurs = json.loads(kurs_verisi)

    rapor = analyzer.analyze(kurs)

    # Raporu kaydet
    kayit = DATA_DIR / "analysis" / f"analiz_{datetime.now():%Y%m%d_%H%M%S}.json"
    kayit.write_text(json.dumps(rapor, ensure_ascii=False, indent=2), encoding="utf-8")

    return json.dumps(rapor, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_rakip_tara(anahtar_kelime: str, limit: int = 5) -> str:
    """Belirtilen anahtar kelimede rakip kurslari tarar.
    Playwright MCP ile Udemy arama sayfasini acar."""
    return json.dumps({
        "durum": "hazir",
        "talimat": f"Playwright MCP ile Udemy'de '{anahtar_kelime}' ara.\n"
                   f"Ilk {limit} kursu listele: baslik, egitmen, puan, "
                   "ogrenci sayisi, fiyat, mufredat ozeti.\n"
                   "Sonuclari data/analysis/ altina kaydet.",
        "arama_url": f"https://www.udemy.com/courses/search/?q={anahtar_kelime}&lang=tr",
    }, ensure_ascii=False)


# ── 3. IYILESTIRME ARACLARI ─────────────────────────────────────

@mcp.tool()
async def udemy_iyilestir(analiz_raporu: str) -> str:
    """Analiz raporuna gore iyilestirme onerileri uretir.
    analiz_raporu: JSON string veya data/analysis/ altindaki dosya adi."""
    veri_yolu = DATA_DIR / "analysis" / analiz_raporu
    if veri_yolu.exists():
        rapor = json.loads(veri_yolu.read_text(encoding="utf-8"))
    else:
        rapor = json.loads(analiz_raporu)

    oneriler = improver.suggest(rapor)

    kayit = DATA_DIR / "improvements" / f"oneri_{datetime.now():%Y%m%d_%H%M%S}.json"
    kayit.write_text(json.dumps(oneriler, ensure_ascii=False, indent=2), encoding="utf-8")

    return json.dumps(oneriler, ensure_ascii=False, indent=2)


# ── 4. ICERIK URETIM ARACLARI ───────────────────────────────────

@mcp.tool()
async def udemy_baslik_olustur(konu: str, hedef_kitle: str = "baslangic") -> str:
    """SEO uyumlu kurs basligi olusturur."""
    return generator.generate_title(konu, hedef_kitle)


@mcp.tool()
async def udemy_aciklama_yaz(baslik: str, mufredat_ozeti: str = "") -> str:
    """Kurs aciklamasi yazar (Udemy standartlarina uygun)."""
    return generator.generate_description(baslik, mufredat_ozeti)


@mcp.tool()
async def udemy_mufredat_olustur(konu: str, seviye: str = "baslangic", sure_saat: int = 5) -> str:
    """Kurs mufredati olusturur: bolumler, dersler, sureler."""
    mufredat = generator.generate_curriculum(konu, seviye, sure_saat)
    return json.dumps(mufredat, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_ders_scripti(ders_basligi: str, sure_dakika: int = 10, dil: str = "tr") -> str:
    """Tek bir ders icin seslendirme scripti uretir."""
    return generator.generate_lecture_script(ders_basligi, sure_dakika, dil)


@mcp.tool()
async def udemy_quiz_uret(konu: str, soru_sayisi: int = 5, zorluk: str = "orta") -> str:
    """Quiz/degerlendirme sorulari uretir."""
    quiz = generator.generate_quiz(konu, soru_sayisi, zorluk)
    return json.dumps(quiz, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_proje_tanimla(konu: str, seviye: str = "baslangic") -> str:
    """Uygulamali proje tanimi olusturur."""
    return json.dumps(generator.generate_project(konu, seviye), ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_kaynak_paketi(konu: str) -> str:
    """Ders kaynak paketi olusturur: cheat sheet, linkler, kod ornekleri."""
    return json.dumps(generator.generate_resources(konu), ensure_ascii=False, indent=2)


# ── 5. GUNCELLEME VE RAPORLAMA ──────────────────────────────────

@mcp.tool()
async def udemy_guncelle(kurs_id: str, degisiklikler: str) -> str:
    """Playwright ile Udemy'de kurs icerigini gunceller.
    degisiklikler: JSON {alan: yeni_deger} formati."""
    return json.dumps({
        "durum": "hazir",
        "talimat": f"Playwright MCP ile Udemy instructor panelini ac.\n"
                   f"Kurs ID: {kurs_id}\n"
                   f"Su degisiklikleri uygula: {degisiklikler}\n"
                   "Her degisiklikten sonra kaydet butonuna bas.",
        "guvenlik": scanner.limiter.oturum_bilgisi(),
    }, ensure_ascii=False)


@mcp.tool()
async def udemy_hiz_modu(mod: str = "yavas") -> str:
    """Tarama hiz modunu degistirir. Bot tespitinden kacinmak icin kullanilir.
    mod: 'yavas' (guvenli, varsayilan), 'normal' (dengeli), 'hizli' (riskli!)
    - yavas: 4-7sn bekleme, 10 sayfada 45sn mola, max 30 sayfa/oturum
    - normal: 2-4sn bekleme, 10 sayfada 30sn mola, max 50 sayfa/oturum
    - hizli: 1-2sn bekleme, 15 sayfada 15sn mola, max 100 sayfa (RISKLI!)"""
    global scanner
    from browser_scanner import BrowserScanner, RateLimiter
    if mod not in RateLimiter.MODLAR:
        return json.dumps({"hata": f"Gecersiz mod: {mod}. Secenekler: yavas, normal, hizli"}, ensure_ascii=False)
    scanner = BrowserScanner(hiz_modu=mod)
    return json.dumps({
        "durum": "degistirildi",
        "yeni_mod": mod,
        **scanner.limiter.oturum_bilgisi(),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
async def udemy_rapor(kapsam: str = "genel") -> str:
    """Pipeline durum raporu: taranan kurslar, analizler, oneriler, uretilen icerikler."""
    rapor = {
        "tarih": datetime.now().isoformat(),
        "kapsam": kapsam,
        "istatistik": {
            "taranan_kurs": len(list((DATA_DIR / "courses").glob("*.json"))),
            "analiz_raporu": len(list((DATA_DIR / "analysis").glob("*.json"))),
            "iyilestirme_onerisi": len(list((DATA_DIR / "improvements").glob("*.json"))),
            "uretilen_icerik": len(list((DATA_DIR / "generated").glob("*"))),
            "yorum_dosyasi": len(list((DATA_DIR / "reviews").glob("*.json"))),
        },
        "tarama_guvenlik": scanner.limiter.oturum_bilgisi(),
    }
    return json.dumps(rapor, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
