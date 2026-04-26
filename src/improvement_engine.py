"""Iyilestirme oneri motoru — analiz raporundan oneriler uretir."""


class ImprovementEngine:
    """Analiz sonuclarina gore oncelikli iyilestirme onerileri uretir."""

    # Kriter bazli oneri sablonlari
    ONERI_SABLONLARI = {
        "Baslik SEO": {
            "dusuk": "Baslik cok kisa veya uzun. 60-80 karakter arasi, anahtar kelime iceren bir baslik olusturun.",
            "orta": "Baslik iyilestirilebilir. Ana anahtar kelimeyi basa alin, '|' ile alt baslik ekleyin.",
            "yuksek": "Baslik SEO'su iyi. Kucuk tweaklerle A/B test yapabilirsiniz.",
        },
        "Aciklama Kalitesi": {
            "dusuk": "Aciklama yetersiz. En az 500 karakter, bullet pointler, CTA ve hedef kitle belirtin.",
            "orta": "Aciklamaya 'Bu kursta neler ogreneceksiniz?' bolumu ve somut ciktilar ekleyin.",
            "yuksek": "Aciklama kaliteli. Ogrenci yorumlarindan alintilar ekleyerek guvenilirlik arttirabilirsiniz.",
        },
        "Mufredat Yapisi": {
            "dusuk": "Mufredat yeniden yapilandirilmali. Mantiksal siraya dizin, her bolume giris dersi ekleyin.",
            "orta": "Bolum basliklarini daha aciklayici yapin, ilerleme hissi veren bir yapi kurun.",
            "yuksek": "Mufredat iyi. Bonus bolum veya ek kaynaklar bolumu ekleyebilirsiniz.",
        },
        "Ders Sureleri": {
            "dusuk": "Dersler cok kisa veya cok uzun. Ideal: 5-15 dakika, toplam 3-10 saat.",
            "orta": "Uzun dersleri bolerek daha sindirilebilir hale getirin.",
            "yuksek": "Ders sureleri ideal. Mevcut yapiyi koruyun.",
        },
        "Uygulamali Icerik Orani": {
            "dusuk": "Uygulamali icerik yetersiz. Her teorik derse bir pratik ders eslestirin. Hedef: %40+.",
            "orta": "Daha fazla code-along, canli demo ve proje dersleri ekleyin.",
            "yuksek": "Uygulamali oran iyi. Mini projeler ekleyerek zenginlestirebilirsiniz.",
        },
        "Quiz/Degerlendirme": {
            "dusuk": "Quiz ve degerlendirme yok. Her bolum sonuna en az 5 soruluk quiz ekleyin.",
            "orta": "Quiz sayisini artirin, farkli soru tipleri (coktan secmeli, dogru/yanlis, eslestirme) kullanin.",
            "yuksek": "Degerlendirme sistemi iyi. Final testi veya sertifika sinavi ekleyebilirsiniz.",
        },
        "Kaynak Materyal": {
            "dusuk": "Indirilebilir kaynak yok. Cheat sheet, kod ornekleri ve ek okuma listesi ekleyin.",
            "orta": "Kaynaklari zenginlestirin: slayt PDF, proje dosyalari, referans kartlari.",
            "yuksek": "Kaynak materyaller yeterli. GitHub reposu veya kaynak paketi olusturabilirsiniz.",
        },
        "Yorum Analizi": {
            "dusuk": "Ogrenci memnuniyeti dusuk. Sik sikayetleri inceleyin ve icerik guncellemesi yapin.",
            "orta": "Olumsuz yorumlardaki ortak temalari adresleyin, Q&A'ya daha hizli yanit verin.",
            "yuksek": "Puanlar iyi. Memnun ogrencilerden review istemeye devam edin.",
        },
        "Rekabet Analizi": {
            "dusuk": "Rakip kurslardan farklilasin: benzersiz projeler, guncel icerik, ek kaynaklar ekleyin.",
            "orta": "Rakiplerde olmayan uygulamali projeler veya bonus icerikler ekleyin.",
            "yuksek": "Rekabetci konumunuz iyi. Guncel tutmaya devam edin.",
        },
        "Guncellik": {
            "dusuk": "Kurs 1 yildan eski. Icerigi guncelleyin, yeni dersler ekleyin, tarih bilgisini yenileyin.",
            "orta": "Son 6 ay icinde guncelleme yapilmis. 3 ayda bir kucuk guncellemeler planlayiin.",
            "yuksek": "Kurs guncel. Bu ritmi koruyun.",
        },
    }

    def suggest(self, analiz_raporu: dict) -> dict:
        """Analiz raporundan iyilestirme onerileri uret."""
        oneriler = []

        for kriter in analiz_raporu.get("kriterler", []):
            ad = kriter["kriter"]
            puan = kriter["puan"]

            if puan <= 4:
                oncelik = "YUKSEK"
                seviye = "dusuk"
            elif puan <= 7:
                oncelik = "ORTA"
                seviye = "orta"
            else:
                oncelik = "DUSUK"
                seviye = "yuksek"

            sablon = self.ONERI_SABLONLARI.get(ad, {})
            oneri_metni = sablon.get(seviye, f"{ad} icin iyilestirme yapilabilir.")

            oneriler.append({
                "kriter": ad,
                "mevcut_puan": puan,
                "oncelik": oncelik,
                "oneri": oneri_metni,
            })

        # Onceliklere gore sirala
        sira = {"YUKSEK": 0, "ORTA": 1, "DUSUK": 2}
        oneriler.sort(key=lambda x: sira.get(x["oncelik"], 3))

        return {
            "kurs_adi": analiz_raporu.get("kurs_adi", "Bilinmiyor"),
            "toplam_puan": analiz_raporu.get("toplam_puan", 0),
            "oneri_sayisi": len(oneriler),
            "yuksek_oncelik": len([o for o in oneriler if o["oncelik"] == "YUKSEK"]),
            "oneriler": oneriler,
        }
