# Udemy MCP

> **Udemy eğitmenleri için Model Context Protocol (MCP) sunucusu.**
> *MCP server for Udemy instructors — courses, reviews, Q&A, content analysis & video pipeline.*

Udemy Instructor API + Playwright tabanlı browser scanner ile, Claude Desktop / Cursor üzerinden kurslarınızı yönetin: yorumları çekin, müfredat analizi yapın, AI yardımıyla içerik üretin, eğitim videosu pipeline'ları çalıştırın.

[![Made with MCP](https://img.shields.io/badge/MCP-Server-blueviolet)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ⚠️ Udemy ToS Uyarısı (Dikkatle Okuyun) / Udemy ToS Notice

**Türkçe:**
Udemy [Terms of Service](https://www.udemy.com/terms/) §6.5 ve §7 maddeleri, otomatik veri toplama, scraping ve robot kullanımını **kısıtlar**. Bu MCP'deki **browser scanner** modülü Playwright ile sayfa otomasyonu yapar; yavaş modda dahi **eğitmen hesabınızın askıya alınması veya kapatılması riski sıfır değildir**. Bu yazılımı kullanmadan önce mutlaka kendi Udemy sözleşmenizi inceleyin. **Kullanım tamamen kendi sorumluluğunuzdadır**; yazar hiçbir hesap yaptırımından sorumlu tutulamaz.

**English:**
Udemy [Terms of Service](https://www.udemy.com/terms/) §6.5 and §7 **restrict** automated data gathering, scraping, and robot use. The **browser scanner** module here automates pages via Playwright; even in slow mode, **the risk of account suspension or termination is non-zero**. Review your own Udemy contract before use. **Use entirely at your own risk**; the author bears no responsibility for any account action.

> 💡 **Önerilen güvenli kullanım:** Sadece Instructor API endpoint'lerini (Bearer token ile) kullanın. Browser scanner modülünü ancak son çare olarak ve düşük frekansta kullanın.

---

## 🎯 Niçin?

Udemy'nin **resmi Instructor API dokümantasyonu** çok dağınık ve eksik. Eğitmenler:
- Yorumlarını filtreli görmek
- Kurslarını rakipleriyle karşılaştırmak
- Toplu içerik güncellemesi yapmak
- AI ile yeni ders üretmek

için ya manuel paneli kullanır ya da yarım kalmış scriptler yazar. Bu MCP, hepsini bir Claude/Cursor sohbetine indirger.

---

## ✨ Özellikler

### Instructor API Entegrasyonu (`api_client.py`)
- Kurs listeleme, detay, yorum, Q&A, abone sayısı
- Bearer token ile (kendi hesabınız)
- Otomatik retry + rate limit

### Browser Scanner (`browser_scanner.py`) — Opsiyonel & Riskli
- Playwright MCP ile entegre
- Hız sınırı (yavaş/normal/hızlı modlar) — **yine de ToS ihlali sayılabilir**
- Müfredat & altyazı tarama
- İnsan davranışı simülasyonu — **bot tespiti riskini azaltır ama tamamen ortadan kaldırmaz**

### İçerik Pipeline'ı
- Kurs müfredat analizi (`content_analyzer.py`)
- Yeni ders/quiz/script üretimi (`content_generator.py`)
- Otomatik HTML → video pipeline (Doodly / Toonly entegrasyonu)
- Meditasyon / seslendirme dönüşümleri

---

## 🚀 Kurulum

```bash
git clone https://github.com/mustafayilmazart/udemy-mcp
cd udemy-mcp
pip install -r requirements.txt
cp .env.example .env
# .env içine UDEMY_INSTRUCTOR_TOKEN= değerini girin
```

### Token Nasıl Alınır?

1. [udemy.com](https://www.udemy.com) → Eğitmen panelinde herhangi bir API çağrısı yapan sayfaya gidin
2. DevTools → Network → herhangi bir `instructor-api/v1/...` isteğini açın
3. **Request Headers** → `Authorization: bearer XXXXX` değerinin XXXXX kısmı sizin token'ınız
4. `.env` dosyasına `UDEMY_INSTRUCTOR_TOKEN=XXXXX` olarak yazın

> ⚠️ Bu token kişiseldir — kimseyle paylaşmayın, repo'ya commitlemeyin (`.gitignore`'da `.env` zaten var).

### Claude Desktop yapılandırması

```json
{
  "mcpServers": {
    "udemy": {
      "command": "python",
      "args": ["/path/to/udemy-mcp/main.py"]
    }
  }
}
```

---

## 📖 Kullanım Örnekleri

```
> Tüm kurslarımdaki son 30 günün 5 yıldızlı yorumlarını listele
```

```
> "Stres ve Başa Çıkma" kursumun müfredatını analiz et, eksik konuları öner
```

```
> Bu kurs için 3 dakikalık bir tanıtım scripti yaz, sonra ElevenLabs için seslendirmeye hazırla
```

---

## ⚠️ Önemli Yasal Uyarılar

1. **Sadece kendi kurslarınızda kullanın.** Bu MCP, başkasının kurslarını taramak için tasarlanmadı ve böyle kullanılırsa Udemy ToS'una **kesin olarak** aykırıdır.
2. **Udemy ToS'una saygı gösterin.** Browser scanner'daki rate limit'ler bilerek konulmuştur — düşürmeyin. Hesap askıya alma riski sizdedir.
3. **Üretilen içerik sizin sorumluluğunuzdadır.** AI ile üretilen ders metinleri, Udemy'nin kalite standartlarını karşılamayabilir; yayınlamadan önce mutlaka gözden geçirin.
4. **Garanti yok.** Bu yazılım "AS IS" sağlanır; "production-tested" değildir, yalnızca yazarın kendi 21 kursunda **kişisel kullanımda** denenmiştir.

---

## 📚 Atıflar

[ATTRIBUTIONS.md](ATTRIBUTIONS.md)

---

## 📄 Lisans

MIT — bkz. [LICENSE](LICENSE).

> Bu proje Udemy LLC ile **resmi olarak bağlantılı değildir**. "Udemy" markası Udemy LLC'ye aittir; bu projede yalnızca tanımlama amaçlı (nominative fair use) kullanılmıştır.
