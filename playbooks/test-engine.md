# Test mühərriki — sürətli məhsul testi sistemi

## 0. Əsas fikir
Məqsəd "hər saat yeni məhsul"dur. Real məhdudiyyət Claude yox, **pul və data**dır: bir məhsulu qiymətləndirmək üçün müəyyən xərc və bir neçə saat/gün lazımdır. Ona görə sistem **paralel portfel**dir: daimi "boru kəməri" (pipeline), hər saat bir yeni namizəd boru kəmərinə **girir**, əksəriyyəti ucuz mərhələdə çıxarılır, azı qalib kimi böyüyür.

Gündəlik yeni test sayı = `günlük_test_büdcəsi ÷ mərhələ-2 büdcəsi`. (Nümunə: $40/gün ÷ $5 = gündə 8 yeni test.) Büdcə artdıqca sürət artır.

## 1. Mərhələlər (funnel)
Parametrlər `state/config.md`-dən: `B` = başa-baş CPA (bir sifarişin ümumi mənfəəti: qiymət − məhsul − çatdırılma − ödəniş komissiyası), `AOV` = orta sifariş.

| Mərhələ | Xərc | Nəyə baxılır | Keçid qaydası (başlanğıc heuristika, datayla dəyişdir) |
|---|---|---|---|
| **S0 Tədqiqat** | $0 | Rəqib reklamı uzun müddət işləyir? Marja ≥ 50%? Çəkmək/çatdırmaq asan? Qadağalı deyil? | Yalnız 4/4 meyar ödənsə keçir |
| **S1 Kreativ test** | ≈$5–10 | 3 hook × məhsul; 3 san tutma, CTR, ATC | Hook rate ≥ ~25–30%, CTR ≥ ~1% (link), ≥1 ATC → keçir, əks halda öldür |
| **S2 Satış testi** | `≤ 1.5 × B` | Alış var? | Xərc `1.5×B`-ə çatıb **0 alış** → öldür. ≥1 alış və CPA ≤ `B` → keçir |
| **S3 Təsdiq** | `≈ 3–5 × B` | ≥3 alış, CPA ≤ `0.7×B` | Təmin olunsa → **Qalib** |
| **S4 Miqyas** | artan | ROAS, marja, təkrar | Büdcəni gündə **≤20%** artır; CPA `B`-ni keçsə dayan |

Bu rəqəmlər başlanğıc fərziyyədir, ilk 50–100 testdən sonra **özün** yenidən kalibrə et və `state/config.md`-ə yaz.

## 2. Hər test üçün paket (Claude hazırlayır)
`state/tests.csv`-də sətir + `tests/<id>/` qovluğunda: tədqiqat qeydi, rəqib reklamlarından nəticə, 3 hook, 1–2 ssenari, reklam mətnləri (≥3 variant), məhsul səhifəsi qaralaması, qiymət/marja hesabı.

## 3. Rəqib və trend analizi (hər gün)
- **Meta Ad Library:** niş açar sözləri və rəqib səhifələri üzrə aktiv reklamlar; ≥14 gündür işləyənlər güclü siqnaldır.
- **TikTok Creative Center:** trend reklamlar, səslər, hook-lar.
- Açıq Reels/TikTok: nə qədər baxış/şərh; şərhlərdə alıcı sualları ("haradan alım?", qiymət).
- Çıxış: `reports/competitors-<tarix>.md` — *nə işləyir, nəyi kopyalamırıq, necə fərqlənirik.* Fərqlənmə burada mütləqdir: daha güclü təklif/zəmanət, daha yaxşı hook, yerli uyğunluq, daha yaxşı məhsul səhifəsi.
- Alət: brauzer/Chrome avtomatlaşdırması **yalnız oxumaq** üçün (açıq səhifələr). Giriş tələb edən yerdə dayan və sahibə de.

## 4. Kreativ konveyer
Gündə toplu: bir sessiyada 8–10 məhsul paketi. Video: telefon/UGC və ya AI alətləri (§6). Hər video 15–30 san, ilk 2 san hook, altyazı mütləq. Qalib hook → 5 variant; itirən → 7 günə kimi öldür.

## 5. İcra arxitekturası (limitə qənaət)
- **Claude = beyin** (gündə 1–2 toplu sessiya): tədqiqat, ssenari, qərar.
- **Skript/API = əllər** (ucuz, hər saat): kampaniya yaratma (PAUSED → sahibin əvvəlcədən təsdiq etdiyi qaydalarla aktiv), hesabat yığma, qaydalarla avtomatik "öldür" (xərc limiti keçən və 0 alışlı reklamı dayandır).
- **Platforma limiti = təhlükəsizlik:** Meta hesabında **hesab xərc limiti** və kart limiti sahib tərəfindən bir dəfə qoyulur. Beləcə agent texniki cəhətdən limitdən çox xərcləyə bilməz və hər klik üçün təsdiq lazım olmur.
- Hər saatlıq iş skriptlə, Claude-u yalnız qərar lazım olanda çağır (limit sərfiyyatı).

## 6. Alət kəşfi (Claude özü tapır)
Yeni alət lazım olanda: (1) internetdə axtar, (2) 2–3 variantı **qiymət, pulsuz səviyyə, risk, rəsmi API var/yoxdur** üzrə cədvəldə müqayisə et, (3) satıcı bloqlarına inanma, rəsmi sayt/istifadəçi rəylərinə bax, (4) ən ucuz kifayət edəni tövsiyə et, (5) `state/tools.md`-ə yaz. Ödəniş sahibdən təsdiq alır.

## 7. Gündəlik dövr
1. Səhər: dünənki rəqəmlər, mərhələlərə görə keçid/öldür qərarları.
2. Rəqib/trend analizi → yeni 8–10 namizəd (S0).
3. Keçənlər üçün kreativ paket (S1).
4. Gün ərzində skript statusu izləyir və avtomatik "öldür" tətbiq edir.
5. Axşam: `reports/<tarix>.md` + sahibə yalnız **ödəniş/təsdiq** siyahısı.
