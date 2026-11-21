"""Regenerate chart-light.svg and chart-dark.svg from the CSVs in data/.

No third-party libraries: the SVG is written by hand so the chart can be
rebuilt anywhere Python runs, and so every number on it is traceable to a row
in data/ rather than to a plotting library's defaults.

    python make_chart.py
"""
import csv
import statistics
from collections import defaultdict

MARKETS = 10
SEED_ORDER = ["credit card", "running shoes", "web hosting"]

# Palette validated for contrast against each surface, in both themes.
THEMES = {
    "light": dict(surface="#ffffff", ink="#0b0b0b", ink2="#52514e", ink3="#75736c",
                  grid="#e6e5e1", s1="#2a78d6", s2="#eb6834", s3="#1baf7a", on_fill="#ffffff"),
    "dark": dict(surface="#0d1117", ink="#f0efec", ink2="#c3c2b7", ink3="#9a988d",
                 grid="#272c33", s1="#3987e5", s2="#d95926", s3="#199e70", on_fill="#ffffff"),
}


def load():
    counts = defaultdict(lambda: defaultdict(int))   # seed -> market_count -> keywords
    engines = defaultdict(lambda: defaultdict(int))  # engine -> 'total'/'exclusive'
    total_keywords = 0
    with open("data/keyword_market_matrix.csv", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            counts[row["seed"]][int(row["market_count"])] += 1
            total_keywords += 1
            names = row["engines"].split("|")
            for name in names:
                engines[name]["total"] += 1
                if len(names) == 1:
                    engines[name]["exclusive"] += 1

    overlaps = defaultdict(list)
    with open("data/market_overlap_pairs.csv", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            overlaps[row["seed"]].append(float(row["overlap_pct_jaccard"]))
    return counts, engines, total_keywords, overlaps


def esc(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(theme_name):
    t = THEMES[theme_name]
    counts, engines, total_keywords, overlaps = load()

    W, H = 920, 620
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">',
        f'<rect width="{W}" height="{H}" fill="{t["surface"]}"/>',
    ]

    def text(x, y, s, size=13, fill=None, weight="400", anchor="start"):
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill or t["ink"]}" '
                   f'font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>')

    # ---------------- panel A: market agreement -----------------------------
    text(40, 44, "Whether keywords differ by country is decided by the topic, not the country",
         18, t["ink"], "700")
    text(40, 68, "43,005 autocomplete suggestions, 3 seeds x 10 English-speaking markets x 4 engines",
         13, t["ink2"])

    X0, BARW, BH, GAP = 196, 560, 40, 62
    top = 112
    text(40, top - 14, "Share of each topic's keywords, by how many of the 10 markets suggested them",
         12, t["ink3"], "600")

    for i, seed in enumerate(SEED_ORDER):
        y = top + i * GAP
        dist = counts[seed]
        total = sum(dist.values())
        all10 = dist.get(MARKETS, 0)
        only1 = dist.get(1, 0)
        middle = total - all10 - only1
        text(X0 - 14, y + BH / 2 + 5, seed, 14, t["ink"], "600", "end")

        x = X0
        for value, colour in ((all10, t["s3"]), (middle, t["s1"]), (only1, t["s2"])):
            w = BARW * value / total
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{BH}" fill="{colour}"/>')
            pct = 100 * value / total
            if w > 46:
                text(x + w / 2, y + BH / 2 + 5, f"{pct:.0f}%", 13, t["on_fill"], "700", "middle")
            x += w
        median = statistics.median(overlaps[seed])
        text(X0 + BARW + 14, y + BH / 2 + 5, f"{median:.0f}% median", 12, t["ink2"], "600")
        text(X0 + BARW + 14, y + BH / 2 + 19, "overlap per pair", 11, t["ink3"])

    legend_y = top + 3 * GAP + 6
    for dx, colour, label in ((0, t["s3"], "in all 10 markets"),
                              (170, t["s1"], "in 2-9 markets"),
                              (320, t["s2"], "in only 1 market")):
        out.append(f'<rect x="{X0 + dx}" y="{legend_y - 10}" width="12" height="12" rx="2" fill="{colour}"/>')
        text(X0 + dx + 18, legend_y, label, 12, t["ink2"])

    # ---------------- panel B: engine contribution --------------------------
    base = legend_y + 56
    out.append(f'<line x1="40" y1="{base - 28}" x2="{W - 40}" y2="{base - 28}" '
               f'stroke="{t["grid"]}" stroke-width="1"/>')
    text(40, base, "What each engine contributes, and how much of it nothing else suggests",
         15, t["ink"], "700")
    text(40, base + 22, f"Of {total_keywords:,} distinct keywords found. A Google-only tool would miss "
                        f"{100 * (total_keywords - engines['google']['total']) / total_keywords:.0f}%.",
         12, t["ink2"])

    rows = [("Google", "google"), ("YouTube", "youtube"), ("Bing", "bing"), ("DuckDuckGo", "duckduckgo")]
    EBH, EGAP = 26, 36
    etop = base + 48
    for i, (label, name) in enumerate(rows):
        y = etop + i * EGAP
        total_share = 100 * engines[name]["total"] / total_keywords
        excl_share = 100 * engines[name]["exclusive"] / total_keywords
        text(X0 - 14, y + EBH / 2 + 5, label, 13, t["ink"], "600", "end")
        we = BARW * excl_share / 100
        ws = BARW * (total_share - excl_share) / 100
        out.append(f'<rect x="{X0}" y="{y}" width="{we:.1f}" height="{EBH}" fill="{t["s2"]}"/>')
        out.append(f'<rect x="{X0 + we:.1f}" y="{y}" width="{ws:.1f}" height="{EBH}" fill="{t["s1"]}"/>')
        if we > 42:
            text(X0 + we / 2, y + EBH / 2 + 5, f"{excl_share:.0f}%", 12, t["on_fill"], "700", "middle")
        text(X0 + we + ws + 12, y + EBH / 2 + 5, f"{total_share:.1f}% of all keywords",
             12, t["ink2"], "600")

    ly = etop + 4 * EGAP + 4
    for dx, colour, label in ((0, t["s2"], "found by this engine alone"),
                              (230, t["s1"], "also found elsewhere")):
        out.append(f'<rect x="{X0 + dx}" y="{ly - 10}" width="12" height="12" rx="2" fill="{colour}"/>')
        text(X0 + dx + 18, ly, label, 12, t["ink2"])

    text(40, H - 18, "Collected with the Long Tail Keyword Questions actor on Apify - "
                     "apify.com/bhole_krishna/keyword-demand-scraper", 11, t["ink3"])
    out.append("</svg>")
    return "\n".join(out)


for name in ("light", "dark"):
    with open(f"chart-{name}.svg", "w", encoding="utf-8") as fh:
        fh.write(build(name))
    print(f"wrote chart-{name}.svg")
