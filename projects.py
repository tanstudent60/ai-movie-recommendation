import time, pandas as pd
from textblob import TextBlob
from colorama import init, Fore
init(autoreset=True)

try:
    df = pd.read_csv("imdb_top_1000.csv")
except FileNotFoundError:
    print(Fore.LIGHTRED_EX + "❌ Oops! 'imdb_top_1000.csv' was not found. Please check the file location."); raise SystemExit

genres = sorted({g.strip() for xs in df["Genre"].dropna().str.split(", ") for g in xs})

def dots():
    for _ in range(3): print(Fore.LIGHTYELLOW_EX + " ●", end="", flush=True); time.sleep(0.5)

def senti(p): return "Uplifting 🌟" if p > 0 else "Dark 🌑" if p < 0 else "Balanced ⚖️"

def recommend(genre=None, mood=None, rating=None, n=5):
    d = df
    if genre: d = d[d["Genre"].str.contains(genre, case=False, na=False)]
    if rating is not None: d = d[d["IMDB_Rating"] >= rating]
    if d.empty: return "😕 No movies matched your filters. Try different options!"
    d, need_nonneg, out = d.sample(frac=1).reset_index(drop=True), bool(mood), []
    for _, r in d.iterrows():
        ov = r.get("Overview")
        if pd.isna(ov): continue
        pol = TextBlob(ov).sentiment.polarity
        if (not need_nonneg) or pol >= 0:
            out.append((r["Series_Title"], pol))
            if len(out) == n: break
    return out if out else "😕 No movies matched your vibe. Try a different mood or genre!"

def show(recs, name):
    print(Fore.LIGHTMAGENTA_EX + f"\n🎬 Handpicked Movie Picks for {name}:")
    print(Fore.LIGHTMAGENTA_EX + "─" * 45)
    for i, (t, p) in enumerate(recs, 1):
        print(f"{Fore.LIGHTCYAN_EX}{i}. 🍿 {t}")
        print(f"   {Fore.LIGHTYELLOW_EX}Vibe Score: {p:.2f}  |  Tone: {senti(p)}")

def get_genre():
    print(Fore.LIGHTGREEN_EX + "\n🎭 Available Genres:\n")
    for i, g in enumerate(genres, 1):
        print(f"  {Fore.LIGHTCYAN_EX}{i:>2}. {g}")
    print()
    while True:
        x = input(Fore.LIGHTYELLOW_EX + "🔢 Enter genre number or name: ").strip()
        if x.isdigit() and 1 <= int(x) <= len(genres): return genres[int(x) - 1]
        x = x.title()
        if x in genres: return x
        print(Fore.LIGHTRED_EX + "⚠  That genre wasn't found. Try again!\n")

def get_rating():
    while True:
        x = input(Fore.LIGHTYELLOW_EX + "⭐ Minimum IMDB rating (7.6–9.3) or type 'skip': ").strip()
        if x.lower() == "skip": return None
        try:
            r = float(x)
            if 7.6 <= r <= 9.3: return r
            print(Fore.LIGHTRED_EX + "⚠  Rating must be between 7.6 and 9.3. Try again!\n")
        except ValueError:
            print(Fore.LIGHTRED_EX + "⚠  Please enter a valid number or 'skip'.\n")

print(Fore.LIGHTCYAN_EX  + "╔══════════════════════════════════════════╗")
print(Fore.LIGHTCYAN_EX  + "║  🎬  Personal Movie Recommendation Bot  ║")
print(Fore.LIGHTCYAN_EX  + "╚══════════════════════════════════════════╝\n")

name = input(Fore.LIGHTYELLOW_EX + "👤 What's your name? ").strip()
print(f"\n{Fore.LIGHTGREEN_EX}👋 Hey {name}! Let's find your perfect watch for tonight!\n")

print(Fore.LIGHTBLUE_EX + "🔍 First, let's narrow down your taste...\n")
genre = get_genre()

mood = input(Fore.LIGHTYELLOW_EX + "\n💭 How are you feeling right now? Describe your mood: ").strip()
print(Fore.LIGHTBLUE_EX + "\n🧠 Reading your mood", end="", flush=True); dots()

mp = TextBlob(mood).sentiment.polarity
md = "positive 🌟" if mp > 0 else "negative 🌑" if mp < 0 else "neutral ⚖️"
print(f"\n{Fore.LIGHTGREEN_EX}✅ Mood detected: {md}  (Score: {mp:.2f})\n")

rating = get_rating()

print(f"{Fore.LIGHTBLUE_EX}\n🎯 Searching for the best picks for {name}", end="", flush=True); dots()

recs = recommend(genre=genre, mood=mood, rating=rating, n=5)
print(Fore.LIGHTRED_EX + "\n" + recs + "\n") if isinstance(recs, str) else show(recs, name)

while True:
    a = input(Fore.LIGHTYELLOW_EX + "\n🔄 Want more recommendations? (yes/no): ").strip().lower()
    if a == "no":
        print(Fore.LIGHTGREEN_EX + f"\n🎉 Enjoy your movie night, {name}! Grab the popcorn! 🍿\n"); break
    if a == "yes":
        recs = recommend(genre=genre, mood=mood, rating=rating, n=5)
        print(Fore.LIGHTRED_EX + "\n" + recs + "\n") if isinstance(recs, str) else show(recs, name)
    else:
        print(Fore.LIGHTRED_EX + "⚠  Please type 'yes' or 'no'.\n")