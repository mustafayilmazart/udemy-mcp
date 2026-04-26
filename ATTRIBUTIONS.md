# Atıflar & Yararlanılan Kaynaklar

## Çekirdek Bağımlılıklar

| Paket | Lisans | Kullanım |
|---|---|---|
| [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | MIT | MCP sunucu altyapısı |
| [httpx](https://www.python-httpx.org/) | BSD-3-Clause | Asenkron HTTP |
| [Playwright](https://playwright.dev/python/) | Apache 2.0 | Browser otomasyon |

## API & Servisler

- **Udemy Instructor API** — © Udemy, LLC. Bu projedeki kullanım [Udemy API ToS'a](https://www.udemy.com/developers/instructor/) uygundur. Her kullanıcı kendi token'ı ile yalnızca kendi içeriğine erişir.
- **ElevenLabs API** (opsiyonel seslendirme) — © ElevenLabs Inc.
- **Doodly / Toonly** (opsiyonel video pipeline) — © Bryxen Inc. Yalnızca lokal lisanslı sürüm üzerinden otomasyon yapılır.

## İlham Alınan Çalışmalar

- [**udemy-dl**](https://github.com/r0oth3x49/udemy-dl) (MIT, arşivlenmiş) — Udemy URL/auth pattern referansı
- [**Playwright MCP**](https://github.com/microsoft/playwright-mcp) (MIT) — Browser scanner integration paterni
- [**Computer Use** by Anthropic](https://www.anthropic.com/news/3-5-models-and-computer-use) — Browser automation ergonomi yaklaşımı

> Yukarıdaki projelerden kod **kopyalanmamış**, yalnızca yaklaşım ilhamı alınmıştır.

## Markalar

- "Udemy" Udemy LLC'nin tescilli markasıdır. Bu repo Udemy ile bağlantılı değildir.
- "Claude" Anthropic PBC'ye aittir.
- "Doodly" ve "Toonly" Bryxen Inc.'e aittir.

## Veriler

Bu MCP, **kullanıcının kendi Udemy hesabının verilerini** çeker. Üçüncü taraf eğitmen verisi toplamaz, depolamaz, paylaşmaz. Cache yalnızca lokal `data/` dizininde tutulur ve `.gitignore`'da yer alır.
