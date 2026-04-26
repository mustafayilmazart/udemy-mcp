# Security Policy

## Reporting / Bildirim

Güvenlik açıkları için: **medya@kesif.org**
For security issues: **medya@kesif.org**

- Public issue **açmayın** / do **not** file public issues
- 72 saat yanıt / 72-hour response
- 14 gün düzeltme hedefi / 14-day fix target

## Common Concerns / Yaygın Endişeler

### Bearer Token Sızıntısı

`UDEMY_INSTRUCTOR_TOKEN` **kişiseldir**. `.env`'i asla commit etmeyin. `.gitignore`'da otomatik olarak yer alır.

Token sızdığını fark ederseniz:
1. Udemy Instructor → DevTools'tan yeni Authorization header alın (eski token otomatik geçersiz)
2. `.env`'i güncelleyin
3. Eğer git history'sine commit ettiyseniz → `git filter-repo` ile temizleyin

### Hesap Askıya Alınması

Browser scanner kullanırken Udemy ToS ihlali yaptığınızı düşünüyorsanız:
1. Browser scanner'ı **derhal durdurun**
2. Udemy Support ile iletişime geçin
3. Yalnızca Instructor API endpoint'lerini kullanın

Hesap askıya alma riski **yazarın sorumluluğunda değildir**.

## Supported Versions

Yalnızca en son major sürüm desteklenir.
