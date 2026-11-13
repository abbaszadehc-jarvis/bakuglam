# Shopify + Agentik İdarəetmə Planı (v0.2)

> **Vəziyyət:** mağaza 8 gün sonra açılır. Məqsəd: Claude agentləri işin əsasını görür, sən yalnız **təsdiq edirsən**.
> `⚠️` = qiymət/qayda yoxlanmamış mənbədən və ya yaddaşdandır, ödəməzdən əvvəl rəsmi saytdan yoxla.

## 0. Dürüst başlanğıc

1. **$100.000/ay hədəfdir, plan deyil.** Bunu iki ayrı rəqəmə böl: *dövriyyə* (gəlir) və *xalis mənfəət*. Nümunə: orta sifariş $50, ROAS 2.5 olarsa, $100k dövriyyə üçün ≈2.000 sifariş və ≈$40k reklam xərci lazımdır; mənfəət isə bunun ancaq kiçik hissəsidir. Hansını nəzərdə tutursan? Cavabına görə yol dəyişir.
2. **8 gündə mağaza açılır, satış avtomatik gəlmir.** İlk 30–60 gün test mərhələsidir. Real ilk hədəf: *ilk 50 sifariş və müsbət marja.*
3. **Agent ≠ nəzarətsiz.** Claude hazırlayır və təklif edir, **pul xərcləyən və ictimai paylaşan hər addımı sən təsdiqləyirsən.**
4. **Ən böyük blokerlər:** (a) Shopify Payments Azərbaycanda dəstəklənmir ⚠️ (b) Meta reklam hesabının bloklanması (bax §5).

## 1. Agent arxitekturası

Bir **Baş agent (Orchestrator)** və ixtisaslaşmış alt agentlər. Hamısı bu repoda `agents/` qovluğunda təlimat faylları (prompt + qaydalar) və `reports/` qovluğunda nəticələrlə işləyir.

| Agent | İşi | Sən nəyi təsdiqləyirsən |
|---|---|---|
| **Tədqiqat** | Niş, məhsul, qiymət, rəqib analizi | Məhsul seçimi |
| **Mağaza qurucu** | Shopify səhifələri, məhsul təsvirləri, siyasətlər, SEO | Açılışdan əvvəl bütün mağaza |
| **Kreativ** | Ssenari, hook, video planı, reklam mətni | Hər video/reklam |
| **Reklam (Meta)** | Kampaniya strukturu, büdcə, test planı, gündəlik hesabat | Hər büdcə və kampaniya |
| **Analitika** | Rəqəmlər: ROAS, CPA, marja; "böyüt/dəyiş/öldür" tövsiyəsi | Həftəlik qərar |
| **Müştəri xidməti** | Email/DM cavab qaralamaları | Qeyri-standart cavablar |

**Günlük ritm:** səhər agent hesabat yazır (dünənki rəqəmlər + 3 təklif) → sən 15 dəq baxıb təsdiqləyirsən → agent icra edir.

## 2. Alət yığını (başlanğıc üçün minimal, peşəkar)

| İş | Alət | Təxmini qiymət ⚠️ | Qeyd |
|---|---|---|---|
| Mağaza | **Shopify Basic** | ~$29–39/ay | Pulsuz mövzu (Dawn) kifayətdir |
| Agent beyni | **Claude** (Claude Code / Pro-Max) | ~$20–100+/ay | Limiti nəzərə al: ağır işi planla |
| Redaktə | **CapCut** | pulsuz / ~$15 | Başlanğıcda pulsuz |
| Uzun → qısa video | OpusClip | pulsuz / ~$15 | İstəyə bağlı |
| Səs/səsləndirmə | ElevenLabs | pulsuz səviyyə / ~$5–22 | Azərbaycan dili keyfiyyətini yoxla |
| AI video/UGC | Hooked, Revid və s. | ~$29+ | **Yalnız organik test işlədikdən sonra** |
| Şəkil/dizayn | Canva | pulsuz / ~$15 | Claude Canva ilə də qoşula bilər |
| Email | Shopify Email → sonra Klaviyo | pulsuz başlanğıc | |
| Rəqib reklamları | **Meta Ad Library** (rəsmi, pulsuz) | pulsuz | §4 |
| Tədarük | CJ Dropshipping / AliExpress / Alibaba | məhsul qiyməti | Nümunə sifariş et |
| İdarə | GitHub (bu repo) + Google Sheets | pulsuz | Hesabatlar və tapşırıqlar |

**Realistik başlanğıc büdcəsi:** alətlər ≈ **$80–150/ay**, reklam testi ≈ **$20–50/gün** (≈$600–1.500/ay) + məhsul nümunələri $50–200 + ödəniş/şirkət qurulumu (məbləğ qurulumdan asılıdır).

## 3. 8 günlük açılış planı

| Gün | İş | Kim |
|---|---|---|
| **1** | Bazar (ABŞ/UK ingilis dili vs. yerli) + niş seçimi, 10 məhsul namizədi | Tədqiqat agenti → sən seçirsən |
| **2** | **Ödəniş sxemi qərarı** (xaricdə şirkət + Stripe/PayPal, yoxsa yerli gateway). Hüquqi/mühasib məsləhəti. Meta Business hesabı + domen | Sən (agent sənəd siyahısı hazırlayır) |
| **3** | Shopify qurulumu: mövzu, naviqasiya, məhsul səhifələri, siyasət səhifələri (qaytarma, gizlilik, çatdırılma), vergi | Mağaza agenti |
| **4** | Məhsul nümunələri sifariş, təchizatçı müqayisəsi, qiymət/marja cədvəli | Tədqiqat + Analitika |
| **5** | Rəqib reklam analizi (§4), 10 hook, 5 video ssenarisi | Kreativ agent |
| **6** | İlk 5–10 video çəkilişi/redaktəsi, TikTok/Instagram hesabları, pixel quraşdırması | Sən + Kreativ |
| **7** | Reklam kampaniya strukturu, hesabat cədvəli, test ödənişi (real sifariş), mağazanın yoxlanışı | Reklam + sən |
| **8** | **Açılış.** Organik paylaşım + kiçik reklam testi | Sən təsdiqləyirsən |

Qayda: gün 2-də ödəniş yolu aydın deyilsə, açılış **dayanır**; ödənişsiz mağaza sifariş qəbul etmir.

## 4. Rəqib və reklam analizi (agentik)

- **Meta Ad Library** (facebook.com/ads/library): rəsmi və açıqdır. Rəqibin aktiv reklamları, nə qədər müddətdir işlədiyi (uzun işləyən = çox güman qazanclı) görünür. Agent ekran görüntülərini/mətnləri oxuyub təhlil edir: hook növü, vəd, təklif, video uzunluğu, CTA.
- **TikTok Creative Center** (pulsuz): trend reklamlar və səslər.
- **Çıxış:** `reports/competitors.md` — rəqib başına: nə deyirlər, nəyi təkrar edirik, **nəylə fərqlənirik** (daha yaxşı təklif, daha güclü zəmanət, daha yaxşı hook, yerli bazara uyğunluq).
- **Etməyəcəklərimiz:** Instagram-dan kütləvi scraping və hesabla avtomatlaşdırılmış giriş. Bu Meta qaydalarını pozur ⚠️ və hesabın bağlanmasına səbəb ola bilər. Ad Library kifayət qədər güclüdür.

## 5. Meta reklamı: agent necə işləyir, risklər

**Üç variant (təhlükəsizlik sırası ilə):**
1. **Agent hazırlayır, sən Ads Manager-də yerləşdirirsən** — ən təhlükəsiz. Agent kampaniya strukturunu, mətnləri, auditoriyanı hazır cədvəl kimi verir.
2. **Rəsmi Meta Marketing API** ilə agent kampaniya yaradır (ilk dəfə **PAUSED**, sən aktiv edirsən). Developer app və icazələr tələb edir ⚠️. Peşəkar və stabil yol.
3. **Chrome extension / brauzer avtomatlaşdırması** ilə Ads Manager-də klikləmə. Texniki mümkündür (Claude in Chrome kimi), amma **ən riskli**: Meta qeyri-adi davranışı və yeni hesabları sərt yoxlayır, hesab bloklana bilər. Yalnız kiçik, təsdiqlənmiş addımlarda və **sən izləyərək** işlət.

**Tövsiyə:** 1 ilə başla → ilk satışlardan sonra 2-yə keç → 3-ü ancaq zəruri olanda.

**Reklam strukturu (başlanğıc):** 1 kampaniya, Advantage+ satış, gündə $20–50, 3–5 kreativ × 2–3 hook; 3–4 gün sonra baxış: öldür / saxla / böyüt. Büdcəni gündə 20%-dən artıq qaldırma.

**Əlavə pozuntu riskləri:** reklamda yalan vəd, "əvvəl/sonra" iddiaları, sağlamlıq/maliyyə iddiaları, başqasının məzmunu, qadağan məhsullar. Agentin qaydalarında bunlar sərt filtr olmalıdır.

## 5.1 Hesab təhlükəsizliyi

- Ayrı Meta Business Manager, 2FA, domen təsdiqi, düzgün ödəniş kartı.
- Parolları/tokenləri agentə **çatdırma**; mümkünsə API tokenləri məhdud icazə ilə.
- Agent heç vaxt kartdan **təsdiqsiz** ödəniş etməməlidir.

## 6. Viral video sistemi (agentik)

1. **Kreativ agent** hər məhsula: 5 hook, 3 ssenari (15–30 san), ekran mətni, çəkiliş siyahısı yazır.
2. **Sən** telefonla çəkirsən (təbii işıq) və ya AI/stok ilə hazırlanır. İlk 2 saniyə qərar verir.
3. **CapCut** ilə redaktə (altyazı mütləqdir, çoxu səssiz baxır).
4. Paylaşım: TikTok, Reels, Shorts — eyni video, 3 platforma.
5. **Analitika agenti:** 3 san tutma, orta izləmə, saxlama/paylaşma; 1.000 baxışdan sonra: qalib → 5 variant, qeyri-qalib → öldür.
6. Həftədə **10–15 video** hədəfi; viral = çox sayda test.

## 7. Real mənzərə: $100k/ay

| Nəticə | Nə lazımdır |
|---|---|
| ≈$100k dövriyyə | 2.000 sifariş/ay (AOV $50), ≈$30–40k reklam, sabit qalib məhsul |
| ≈$100k mənfəət | Bunun 3–5 qatı dövriyyə və ya yüksək marjalı private label məhsul |

Bu, əksər mağazaların 1-ci ayında çatmadığı hədəfdir. Yol: **test → 1–3 qalib → miqyas → brend.** Hər mərhələdə rəqəmə baxıb qərar veririk.

## 8. Mənim sənə lazım olanlar (cavab ver)

1. Hədəf: $100k **dövriyyə**, yoxsa **xalis mənfəət**? Nə vaxta qədər?
2. Başlanğıc üçün real büdcə: alətlər + reklam + məhsul.
3. Hansı bazar: ABŞ/UK, Türkiyə, yoxsa Azərbaycan?
4. Hüquqi qurum/ödəniş: Azərbaycan vergi ödəyicisisən? Xaricdə şirkət/hesab açmaq mümkündürmü?
5. Niş ideyan varmı? Yoxdursa, tədqiqat agenti 10 ideya çıxarar.
6. Özün kamera qarşısına çıxacaqsan, yoxsa üzsüz (əl, məhsul, səs)?

## 8.1 Sürətli test mühərriki (v0.3)

Daimi təlimat `CLAUDE.md`-dədir (Claude hər sessiyada özü oxuyur, sənin təkrar öyrətməyinə ehtiyac yoxdur). Test sistemi `playbooks/test-engine.md`, parametrlər `state/config.md`, nəticələr `state/tests.csv`.
Əsas: "hər saat yeni məhsul" = boru kəmərinə hər saat yeni namizəd girir; sürəti **büdcə** müəyyən edir. Claude gündə 1–2 toplu sessiyada düşünür, skript/API saatlıq icranı görür, Meta hesab xərc limiti isə təhlükəsizlik çəpəridir.

## 9. Növbəti addım

Cavablarını verən kimi: (a) `agents/` qovluğunda agent təlimatlarını yazıram, (b) 1-ci gün tədqiqatı (niş, məhsul, rəqiblər) üçün axtarış edirəm. Qiymətlər və qaydalar ödəməzdən əvvəl rəsmi saytdan yenidən yoxlanacaq.

## Mənbələr (əvvəlki araşdırmadan)

- [NerdWallet: Shopify pricing](https://www.nerdwallet.com/article/small-business/shopify-pricing)
- [Shopify icması: Azərbaycanda Shopify Payments](https://community.shopify.com/t/does-shopify-payments-work-in-azerbaijan-need-help-with-setup-issues/296146)
- [Printful: dropshipping vs private label](https://www.printful.com/blog/dropshipping-vs-private-label)
- [Jupitrr: UGC video editors](https://jupitrr.com/best/ugc-video-editors)

*Bu versiyadakı Meta və alət qiymətləri, API qaydaları araşdırma ilə təsdiqlənməyib, yaddaşa əsaslanır.*
