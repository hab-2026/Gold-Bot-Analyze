"""Prompts and system personas for the Gold ICT Agent."""

from __future__ import annotations
import json

# Stable persona focused entirely on Gold and ICT concepts.
PERSONA = (
    "You are an elite Smart Money Concepts (SMC) and Inner Circle Trader (ICT) analyst "
    "specializing in XAU/USD (Gold). Your goal is to analyze news and market structure "
    "to find high-probability trade setups. You never just summarize; you look for liquidity "
    "sweeps, fair value gaps (FVGs), and order blocks (OBs). You combine fundamental news "
    "(Fed, CPI, DXY) with technical ICT concepts. You ALWAYS reply with a single valid JSON "
    "value and nothing else — no markdown fences, no commentary."
)

FETCH_SYSTEM = PERSONA
ANALYZE_SYSTEM = PERSONA
PERSPECTIVES_SYSTEM = PERSONA
MONITOR_SYSTEM = PERSONA

CLASSIFY_SYSTEM = (
    "You are a precise news classifier for the Gold market. You reply with valid JSON only."
)

HISTORY_SYSTEM = (
    "You are a market historian who specializes in Gold. You connect today's macro events "
    "to historical price action patterns in XAU/USD. You reply with valid JSON only."
)

SYNTHESIS_SYSTEM = (
    "You are a lead portfolio manager synthesizing the views of multiple traders into a "
    "single unified trading plan for Gold. You reply with valid JSON only."
)

VERDICT_SYSTEM = (
    "You are the final AI trading assistant. Give a definitive verdict on Gold based on ICT "
    "and macro fundamentals. You reply with valid JSON only."
)

REWRITE_SYSTEM = (
    "You are an expert editor. You turn dense analysis into plain, simple English for a "
    "Telegram channel. Clearly highlight the Bias, Point of Interest (POI), and Stop Loss. "
    "You reply with valid JSON only."
)

# ---- AGENT 1: News Fetcher ----

_FETCH_SCHEMA = (
    '{"stories":[{"headline":"short, clear headline",'
    '"summary":"2-3 sentences explaining what happened",'
    '"why":"one sentence on why it matters for Gold"}]}'
)

def news_fetch_prompt(today: str) -> str:
    return (
        f"Today is {today}. Search across several financial news outlets for the most "
        f"significant macroeconomic news and geopolitical events that will impact Gold (XAU/USD) "
        f"in the next 24 hours. Focus on the Fed, inflation (CPI/PPI), DXY, and bond yields. "
        f"Choose the 5 most impactful stories.\n\n"
        f"Return ONLY this JSON:\n{_FETCH_SCHEMA}"
    )

def search_fetch_prompt(query: str, today: str) -> str:
    return (
        f'Today is {today}. The user wants to understand: "{query}". Search '
        f"several outlets for the latest developments and return the 5 most important angles "
        f"on how this affects Gold (XAU/USD).\n\n"
        f"Return ONLY this JSON:\n{_FETCH_SCHEMA}"
    )

# ---- AGENT 2: Classifier ----

def classify_prompt(raw: list[dict]) -> str:
    listing = "\n".join(
        f"{i + 1}. {s['headline']} — {s['summary']}" for i, s in enumerate(raw)
    )
    return (
        f"Classify each news story below based on its impact on Gold.\n\n{listing}\n\n"
        "For each story give three things:\n"
        "- domain: exactly one of Fed Policy, Inflation, Geopolitics, USD Strength, Market Structure.\n"
        "- urgency: an integer 1-10 for how much it will move Gold.\n"
        "- severity: exactly one of CRITICAL, HIGH, MEDIUM, LOW.\n\n"
        "Return ONLY this JSON, one item per story in the same order:\n"
        '{"items":[{"domain":"...","urgency":0,"severity":"..."}]}'
    )

# ---- AGENT 3: Analyst ----

def analyze_prompt(story: dict) -> str:
    return (
        "Analyze this news story strictly from an ICT (Inner Circle Trader) and Smart Money perspective for Gold.\n\n"
        f"STORY: {story['headline']}\n{story['summary']}\n\n"
        "Return ONLY this JSON:\n"
        '{"marketStructure":"Is Gold bullish or bearish? Look for MSS/BOS.",'
        '"liquidityTargets":"Where is the Buy-Side (BSL) and Sell-Side Liquidity (SSL) resting?",'
        '"fairValueGaps":"Are there any FVGs that price needs to fill?",'
        '"orderBlocks":"Where is the high-probability Point of Interest (POI)?",'
        '"narratives":[{"side":"e.g. Retail vs Smart Money","framing":"how the news traps retail traders"}]}\n'
        "Give 2-3 items in narratives."
    )

# ---- AGENT 4: Impact Mapper ----

def impact_prompt(story: dict) -> str:
    return (
        "Map the ripple effects of this news on Gold's price action.\n\n"
        f"STORY: {story['headline']}\n{story['summary']}\n\n"
        "Return ONLY this JSON:\n"
        '{"impacts":[{"domain":"one of: Liquidity, FVG, Order Block, Bias","impact":"the concrete effect on price","signal":"exactly one of: bullish, bearish, sweep, watch"}],'
        '"winners":["who profits from this setup"],"losers":["who gets stopped out"]}\n'
        "Give 3 impacts, 2 winners and 2 losers."
    )

# ---- AGENT 5: Historian ----

def history_prompt(story: dict) -> str:
    return (
        "Think like an ICT market historian. A news story is below.\n\n"
        f"STORY: {story['headline']}\n{story['summary']}\n\n"
        "Return ONLY this JSON:\n"
        '{"historicalPattern":{"parallel":"a specific similar macro event from history","lesson":"how Gold reacted technically (liquidity sweep, etc.)","divergence":"the key way this time is different"},'
        '"blindSpots":["an angle the retail crowd is missing"],'
        '"predictions":[{"horizon":"e.g. NY Session / 1 week","prediction":"where liquidity will be taken"}],'
        '"contrarianView":"argue AGAINST the obvious direction"}\n'
        "Give 2 blindSpots and 2 predictions."
    )

# ---- Multi-Agent View: 5 analysts ----

def perspectives_prompt(story: dict) -> str:
    return (
        "Five expert Gold analysts each examine this story. Each MUST think in their own distinct way.\n\n"
        f"STORY: {story['headline']}\n{story['summary']}\n\n"
        "The analysts:\n"
        "1. ICT Scalper (⚡) — looks for 15m/1H FVGs and Order Blocks.\n"
        "2. Macro Fundamentalist (🏦) — looks at DXY and Fed policy.\n"
        "3. Swing Trader (📈) — looks at daily/4H market structure.\n"
        "4. Risk Manager (🛡️) — focuses only on where the Stop Loss goes and invalidation.\n"
        "5. Contrarian (🔄) — looks for the liquidity sweep that will fake everyone out.\n\n"
        "Return ONLY this JSON:\n"
        '{"agents":[{"role":"ICT Scalper","emoji":"⚡","lens":"Looks for short-term FVGs","take":"their perspective","prediction":"what they expect to happen next"}]}\n'
        "Include all five analysts in the order above."
    )

# ---- Debate Mode: synthesis ----

def synthesis_prompt(takes: dict) -> str:
    return (
        "Below are five analysts' views on the same Gold setup. Act as the lead portfolio manager.\n\n"
        f"{json.dumps(takes)}\n\n"
        "Return ONLY this JSON:\n"
        '{"agreement":"what most analysts agree on (e.g. overall daily bias)",'
        '"tension":"where they disagree (e.g. scalp long vs. swing short)",'
        '"contrarian":"the best argument against the mainstream view"}'
    )

# ---- Verdict ----

def verdict_prompt(topic: str, story: dict) -> str:
    return (
        f'The user asked about: "{topic}". The key development is below.\n\n'
        f"STORY: {story['headline']}\n{story['summary']}\n\n"
        "Return ONLY this JSON:\n"
        '{"bias":"Bullish / Bearish / Neutral",'
        '"liquidityTarget":"Where is price likely going to sweep?",'
        '"poi":"Point of Interest (Entry Level)",'
        '"invalidation":"Where is the setup wrong? (Stop Loss)",'
        '"opinion":"Your final take on the trade, 2-3 sentences."}\n'
    )

# ---- Continuous monitor ----

def monitor_prompt(today: str) -> str:
    return (
        f"Today is {today}. Search the web for major breaking news from the last few hours.\n"
        "Decide if anything is CRITICAL for Gold — e.g. surprise rate hikes/cuts, CPI, NFP, or war.\n\n"
        "Return ONLY this JSON:\n"
        '{"critical":true or false,"items":[{"headline":"","summary":"what happened","why":"why this is critical for Gold"}]}\n'
        'If nothing is critical, return {"critical":false,"items":[]}.'
    )

# ---- AGENT 6: Rewriter ----

def rewrite_prompt(label: str, payload: str) -> str:
    return (
        f"Below is a JSON object containing a {label}. Rewrite the text to be perfect for a Telegram message.\n"
        "Use emojis. Clearly highlight the ICT Bias, POI, and Invalidation (Stop Loss). "
        "Keep every JSON key exactly the same. Only rewrite the text values.\n"
        f"Return ONLY the rewritten JSON.\n\nJSON:\n{payload}"
    )
