# What 10 English-speaking markets autocomplete

### Collected with the Long Tail Keyword Questions actor on Apify

**[apify.com/bhole_krishna/keyword-demand-scraper](https://apify.com/bhole_krishna/keyword-demand-scraper)**

Every row here came from that actor: live suggestions from Google, YouTube, Bing and DuckDuckGo — the list that drops down while you type. The headline finding below is a property of the *topic*, so the number in this dataset is not your number. One run per market gives you yours.

---

## Why this dataset exists

Every keyword tool offers country targeting. Hardly any of them tell you whether it is worth using.

So this was collected to answer one question with numbers: **if you run the same seed term in ten different countries, how different are the results?**

43,005 suggestions. 3 topics. 10 markets that all search in English. 4 engines. One day.

## The finding

| Topic | Median overlap between any two markets | Keywords in all 10 markets | Keywords in only one market |
|---|---|---|---|
| `credit card` | **46.9%** | 16.3% | **58.1%** |
| `running shoes` | 64.5% | 32.2% | 40.0% |
| `web hosting` | **93.7%** | 77.1% | 11.4% |

Credit cards are issued by local banks under local rules, so most of the demand is local: **58% of the credit-card keywords appeared in exactly one of the ten markets.** Web hosting is a global digital product bought the same way everywhere, and the ten markets returned **93.7% the same list** — country targeting on that topic is effort spent for nothing.

"Should I do country-specific keyword research?" has a real answer, and it is a property of your category, not of your tool.

## What market-exclusive keywords look like

Real rows, each suggested in exactly one market:

| Market | `credit card` | `running shoes` |
|---|---|---|
| IN | `credit card meaning in marathi` | `which running shoes is best for men` |
| ZA | `credit card capitec` | `running shoes edgars` |
| SG | `credit card citibank waiver` | `running shoes jewel` |
| PH | `credit card convert to cash` | `running shoes ukay` |
| AE | `credit card cash withdrawal malayalam` | `running shoes abu dhabi` |
| NG | `credit card checkout ui figma` | `running shoes lagos` |

Local banks, local retailers, local languages, local cities. No US-centric keyword database holds these, because they are not US demand.

The UK was the exception: only 10 of the 3,099 `credit card` keywords and a single one of the 1,584 `running shoes` keywords were exclusive to GB.

## The second finding: one engine is not enough

| Engine | Share of all 5,557 keywords it found | Of its own finds, share nothing else suggested |
|---|---|---|
| Google | 57.8% | 64.7% |
| YouTube | 42.4% | **68.4%** |
| Bing | 22.7% | 16.0% |
| DuckDuckGo | 20.5% | 10.4% |

**A Google-only keyword tool misses 42.2% of what people type.** YouTube's suggestion box is close to a separate corpus: more than two thirds of what it offers, no other engine does — people phrasing a search because they want to *watch* rather than read.

## Files

**`suggestions.csv`** (43,005 rows) — every suggestion as collected. One row per suggestion per query per engine per market: `seed`, `market`, `engine`, `query`, `rank_in_suggestions`, `keyword`, `intent`, `word_count`.

**`keyword_market_matrix.csv`** (5,557 rows) — the analysis table. One row per distinct keyword with `markets`, `market_count` (10 = universal, 1 = market-exclusive), `engines`, `engine_count` and `best_rank`.

**`market_overlap_pairs.csv`** (135 rows) — 45 market pairs × 3 seeds, with `shared`, `union`, `overlap_pct_jaccard` and the directional `share_of_a_also_in_b`.

**`engine_contribution.csv`** (20 rows) — per seed and pooled, each engine's reach and exclusivity, plus a `google-only tool would miss` row.

## Things to try with it

- Measure overlap for each topic and rank categories by how local their demand is.
- Find the keywords unique to one market and read them — that is where the local retailers and banks are.
- Compare `question` share by market: do some countries ask more than they search?
- Test whether market-exclusive keywords sit lower in the suggestion list than universal ones (`best_rank`).
- Check whether YouTube's exclusive keywords are longer than Google's.
- Use `rank_in_suggestions` to weight keywords by prominence instead of treating every suggestion equally.

## How it was collected

Every row came from the four engines' own public suggestion endpoints, gathered by the [**Long Tail Keyword Questions actor**](https://apify.com/bhole_krishna/keyword-demand-scraper) on Apify. No login, no API key, no paid keyword database, nothing behind a paywall. Of 4,680 requests, 0 failed.

Each seed was expanded into 39 queries per engine: the seed itself, the seed plus each letter a–z, and twelve question words in front. Every market got exactly the same 39 queries, which is what makes the comparison fair.

To collect this for your own category:

```json
{
  "seeds": ["your seed term"],
  "engines": ["google", "youtube", "bing", "duckduckgo"],
  "language": "en",
  "country": "US",
  "includeLetters": true,
  "includeQuestions": true
}
```

Run it once per market and compare the keyword sets. The actor also labels every keyword with search intent, records its rank in each engine's suggestion list, and where a keyword clearly names a real topic it attaches Wikipedia's counted monthly pageviews rather than a modelled search-volume estimate.

Full column documentation and a chart script: [github.com/krishnadubey965/autocomplete-10-markets](https://github.com/krishnadubey965/autocomplete-10-markets)

## Honest notes on the data

**Three seeds is a demonstration, not a law.** They were picked to span local-service, physical-product and global-digital categories. They show that the overlap figure varies enormously by topic; they do not establish what it will be for yours.

**Language was held fixed at `en`; only the country changed.** Running Germany or Brazil would have mixed language differences into market differences, and "German keywords differ from English ones" is not a finding. All ten markets here search in English.

**One snapshot, 21 November 2026.** Suggestion lists are live and they move.

**Not an exhaustive keyword list.** A deeper expansion would find more keywords. The comparison is fair because every market got the same queries.

**`intent` is rule-based, not inferred.** Question words mean `question`, price words mean `transactional`, comparison words mean `commercial`. It is a transparent rule, not a model.

**Suggestion endpoints are unpersonalised but not deterministic.** They can answer slightly differently from different datacentres, so a repeat run will not be byte-identical.

**`market_count = 10` does not mean equally popular everywhere**, only that all ten markets offered the phrase. `best_rank` is the column for prominence.

## Licence

CC BY 4.0. Use it commercially, publish from it, build on it; just credit the source.

*What 10 English-speaking markets autocomplete (2026). Collected with the Long Tail Keyword Questions actor on Apify. https://apify.com/bhole_krishna/keyword-demand-scraper*

Not affiliated with, authorised by or endorsed by Google, YouTube, Microsoft Bing or DuckDuckGo.
