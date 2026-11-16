#!/usr/bin/env python3
"""reelvault - Instagram saved postlarini oxuyur, Claude/sistem movzulularini suzur.

Addimlar (hamisi lokal, hesab/server lazim deyil):
  python reelvault.py urls  EXPORT_QOVLUGU_VEYA_FAYL     -> urls.txt
  python reelvault.py fetch --cookies cookies.txt        -> data/<kod>/info.json (+ audio)
  python reelvault.py transcribe                         -> data/<kod>/transcript.txt (faster-whisper)
  python reelvault.py build                              -> vault/*.md, INDEX.md, claude_saves.md
"""
import argparse, json, os, re, subprocess, sys, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA, VAULT = ROOT / "data", ROOT / "vault"
URL_RE = re.compile(r"https?://(?:www\.)?instagram\.com/(?:[\w.]+/)?(p|reel|reels|tv)/([A-Za-z0-9_-]+)")

# agirliqli acar sozler: Claude + sistem/agent movzusu
KEYWORDS = {
    "claude": 5, "anthropic": 5, "claude code": 6, "mcp": 4, "subagent": 4, "sub-agent": 4,
    "agentic": 3, "agent": 3, "agents": 3, "skill": 2, "skills": 2, "system prompt": 4,
    "prompt": 1, "workflow": 2, "automation": 2, "n8n": 2, "orchestrat": 3, "rag": 2,
    "llm": 2, "cursor": 2, "codex": 2, "openai": 1, "gemini": 1, "vibe coding": 2,
    "obsidian": 1, "second brain": 2, "sistem": 2, "agent sistemi": 3,
}
CORE = ("claude", "anthropic", "mcp", "agent", "sistem")
THRESHOLD = 4


def shortcodes_from_text(text):
    seen, out = set(), []
    for kind, code in URL_RE.findall(text):
        if code not in seen:
            seen.add(code)
            out.append((kind, code))
    return out


def cmd_urls(a):
    p = Path(a.source)
    files = [p] if p.is_file() else [f for f in p.rglob("*") if f.suffix in (".json", ".html", ".txt")]
    if not files:
        sys.exit("Fayl tapilmadi: " + a.source)
    seen, items = set(), []
    for f in files:
        if p.is_dir() and a.saved_only and "saved" not in str(f).lower():
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for kind, code in shortcodes_from_text(text):
            if code not in seen:
                seen.add(code)
                items.append((kind, code))
    out = ROOT / "urls.txt"
    out.write_text("\n".join(f"https://www.instagram.com/{'reel' if k != 'p' else 'p'}/{c}/" for k, c in items) + "\n")
    print(f"{len(items)} saved post tapildi -> {out}")


def need(tool):
    if not shutil.which(tool):
        sys.exit(f"'{tool}' yuklenmeyib. Windows: winget install {tool}")


def cmd_fetch(a):
    need("yt-dlp")
    urls = [u.strip() for u in (ROOT / "urls.txt").read_text().split() if u.strip()]
    if a.limit:
        urls = urls[: a.limit]
    DATA.mkdir(exist_ok=True)
    failed = []
    for i, u in enumerate(urls, 1):
        code = URL_RE.search(u).group(2)
        d = DATA / code
        if (d / "info.json").exists():
            continue
        d.mkdir(exist_ok=True)
        cmd = ["yt-dlp", "--cookies", a.cookies, "--write-info-json", "--no-playlist",
               "-o", str(d / "media.%(ext)s"), "--sleep-interval", "2", "--max-sleep-interval", "5"]
        cmd += ["-x", "--audio-format", "mp3"] if a.audio else ["--skip-download"]
        r = subprocess.run(cmd + [u], capture_output=True, text=True)
        produced = next(d.glob("media*.info.json"), None)
        if produced:
            produced.rename(d / "info.json")
            print(f"[{i}/{len(urls)}] OK   {code}")
        else:
            failed.append(u)
            (d / "FAILED.txt").write_text(r.stderr[-500:])
            print(f"[{i}/{len(urls)}] FAIL {code} (carousel/sekil ve ya silinib ola biler)")
    if failed:
        (ROOT / "failed.txt").write_text("\n".join(failed) + "\n")
        print(f"{len(failed)} post alinmadi -> failed.txt")


def _fix(s):
    """Instagram ixraci UTF-8-i yanlis kodlayir (mojibake); duzeldir."""
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def cmd_fromexport(a):
    """saved_posts.json icinde caption hazir gelir -> yuklemeye ehtiyac yoxdur."""
    p = Path(a.source)
    f = p if p.is_file() else next(p.rglob("saved_posts.json"), None)
    if not f:
        sys.exit("saved_posts.json tapilmadi")
    items = json.loads(f.read_text(encoding="utf-8"))
    n = 0
    for it in items:
        lv = it.get("label_values", [])
        if not lv or "href" not in lv[0]:
            continue
        m = URL_RE.search(lv[0]["href"])
        if not m:
            continue
        code = m.group(2)
        caption = _fix(lv[1].get("value", "")) if len(lv) > 1 else ""
        owner = "?"
        for e in lv:
            for sub in e.get("dict", []):
                inner = sub.get("dict", [])
                if len(inner) >= 3 and inner[2].get("value"):
                    owner = _fix(inner[2]["value"])
        d = DATA / code
        d.mkdir(parents=True, exist_ok=True)
        (d / "info.json").write_text(json.dumps({
            "description": caption, "uploader": owner, "webpage_url": lv[0]["href"],
            "upload_date": str(it.get("timestamp", ""))}, ensure_ascii=False), encoding="utf-8")
        n += 1
    print(f"{n} post data/ qovluguna yazildi (caption ile). Indi: python reelvault.py build")


def cmd_transcribe(a):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Once: pip install faster-whisper")
    model = WhisperModel(a.model, compute_type="int8")
    for d in sorted(DATA.glob("*")):
        audio = next(d.glob("media.*"), None)
        out = d / "transcript.txt"
        if not audio or audio.suffix == ".json" or out.exists():
            continue
        segs, _ = model.transcribe(str(audio))
        out.write_text(" ".join(s.text.strip() for s in segs), encoding="utf-8")
        print("transkript:", d.name)


def score(text):
    t = text.lower()
    s, hits = 0, []
    for k, w in KEYWORDS.items():
        n = len(re.findall(r"(?<![a-z])" + re.escape(k), t))
        if n:
            s += w * min(n, 3)
            hits.append(k)
    core = any(c in hits or any(h.startswith(c) for h in hits) for c in CORE)
    return s, hits, core


def cmd_build(a):
    VAULT.mkdir(exist_ok=True)
    rows = []
    for d in sorted(DATA.glob("*")):
        f = d / "info.json"
        if not f.exists():
            continue
        info = json.loads(f.read_text(encoding="utf-8"))
        caption = info.get("description") or info.get("title") or ""
        tr = (d / "transcript.txt").read_text(encoding="utf-8") if (d / "transcript.txt").exists() else ""
        s, hits, core = score(caption + " " + tr)
        rel = core and s >= THRESHOLD
        rows.append(dict(code=d.name, url=info.get("webpage_url", f"https://www.instagram.com/p/{d.name}/"),
                         owner=info.get("uploader") or info.get("channel") or "?",
                         date=info.get("upload_date", ""), caption=caption, transcript=tr,
                         score=s, hits=hits, rel=rel))
        (VAULT / f"{d.name}.md").write_text(
            f"---\nurl: {rows[-1]['url']}\nowner: {rows[-1]['owner']}\ndate: {rows[-1]['date']}\n"
            f"claude_related: {str(rel).lower()}\nscore: {s}\ntags: {hits}\n---\n\n"
            f"## Caption\n{caption}\n\n## Transkript\n{tr or '(yoxdur)'}\n", encoding="utf-8")
    rows.sort(key=lambda r: -r["score"])
    rel = [r for r in rows if r["rel"]]
    idx = [f"# Saved postlar ({len(rows)})\n", f"## Claude & sistemler ({len(rel)})\n"]
    idx += [f"- [{r['owner']}]({r['url']}) - skor {r['score']} - {', '.join(r['hits'][:5])}" for r in rel]
    idx += ["\n## Diger postlar\n"] + [f"- [{r['owner']}]({r['url']}) - {r['caption'][:70]!r}" for r in rows if not r["rel"]]
    (ROOT / "INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    big = [f"# Claude & sistem saved-leri ({len(rel)})\n"]
    for r in rel:
        big.append(f"\n---\n## {r['owner']} - {r['url']}\nSkor {r['score']} ({', '.join(r['hits'])})\n\n"
                   f"**Caption:** {r['caption']}\n\n**Transkript:** {r['transcript'][:4000] or '(yoxdur)'}\n")
    (ROOT / "claude_saves.md").write_text("".join(big), encoding="utf-8")
    print(f"{len(rows)} post, {len(rel)} Claude/sistem ile elaqeli -> INDEX.md, claude_saves.md")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    u = sp.add_parser("urls"); u.add_argument("source"); u.add_argument("--saved-only", action="store_true", default=True)
    f = sp.add_parser("fetch"); f.add_argument("--cookies", required=True); f.add_argument("--limit", type=int)
    f.add_argument("--audio", action="store_true", help="audio da yukle (transkript ucun)")
    t = sp.add_parser("transcribe"); t.add_argument("--model", default="small")
    sp.add_parser("build")
    x = sp.add_parser("fromexport"); x.add_argument("source")
    a = ap.parse_args()
    {"urls": cmd_urls, "fetch": cmd_fetch, "transcribe": cmd_transcribe, "build": cmd_build, "fromexport": cmd_fromexport}[a.cmd](a)


if __name__ == "__main__":
    main()
