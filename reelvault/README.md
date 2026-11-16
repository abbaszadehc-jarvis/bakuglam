# reelvault — Instagram saved-lərinizi oxuyan sistem

Hesab, Supabase və ya Vercel lazım deyil. Hamısı kompüterinizdə işləyir, yalnız Python standart kitabxanası.

## 1. Bir dəfə quraşdırın (Windows)
```
winget install Python.Python.3.12 yt-dlp ffmpeg
pip install faster-whisper
```

## 2. Instagram ixracı (rəsmi, parol vermirsiniz)
Instagram → Settings → Accounts Center → Your information and permissions → Download your information → **Saved** seçin, format **JSON** → yükləyin və açın.

## 3. İşlədin
```
python reelvault.py urls  C:\yol\instagram-export
python reelvault.py fetch --cookies cookies.txt --audio
python reelvault.py transcribe
python reelvault.py build
```
- `cookies.txt`: Chrome-da Instagram-a daxil olun, "Get cookies.txt LOCALLY" uzantısı ilə `instagram.com` üçün ixrac edin. **Heç yerə yükləməyin.** Cookie olmadan yalnız `urls` və `build` işləyir.
- `--limit 20` ilə əvvəl az sayda sınayın.
- Dayansa, eyni əmri yenidən işlədin, tamamlananlar keçilir.

## 4. Nəticə
- `INDEX.md`: "Claude & sistemlər" bölməsi balla sıralanıb.
- `claude_saves.md`: Claude və sistem postlarının hamısı bir faylda. Bunu Claude-a verin: "Bu saved-lərin xülasəsini çıxar, mövzulara böl və nə qurmağa dəyər olduğunu de".
- `vault/*.md`: hər post üçün qeyd (Obsidian-da açılır).

Süzgəc açar sözlərlə işləyir (`reelvault.py` içində `KEYWORDS`), istədiyiniz sözü əlavə edə bilərsiniz.
Carousel və şəkil postları `yt-dlp` ilə alınmır, `failed.txt` faylına düşür.
