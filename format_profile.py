
import argparse
import re
from utils import shorten_links_in_text

HEADER = """# Andrew G. Stanton

**Bitcoiner. Builder. Rooted in the Victorious Gospel.**  
CTO @ StartNation | Founder: Golden Gate Group & Blue Planet Ventures  
Faith-forward · Startup-scarred · Still building.

---

📍 **Following Jesus. Building with conviction. Betting on people.**  
🙏 Victorious Gospel believer  
⚡️ Proof of Work > Proof of Hype  
📈 Equity trader · Aspiring Bitcoin contributor  
🧠 35+ years in dev · Still learning · Still showing up

---

### 🚀 Startups I’ve Founded
"""

FOOTER = """

---

### 🔗 Other Links

- [LinkedIn](https://tinyurl.com/yv36rdam)
- [Facebook](https://tinyurl.com/ypmsmfww)
- [Twitter/X](https://tinyurl.com/yqha2urx)
- [Discord](https://tinyurl.com/ylar9kn2)
- [GitHub](https://tinyurl.com/yku3jd9z)

---

### ⚡ Nostr + Zaps

- **Npub:** `npub19wvckp8z58lxs4djuz43pwujka6tthaq77yjd3axttsgppnj0ersgdguvd`
- **Zap me:** [tinyurl.com/yuyu2b9t](https://tinyurl.com/yuyu2b9t)

Clients:
- [Snort](https://tinyurl.com/yryevvrd)
- [Coracle](https://tinyurl.com/yv6lx6uz)

---

### #hashtags

`#bitcoin`, `#nostr`, `#faith`, `#victoriousgospel`, `#proofOfWork`,  
`#startupbuilder`, `#bitcoinerforgood`, `#sovereignstacker`
"""

def format_profile_section(raw):
    output = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if line.startswith("http"):
            name = re.sub(r"https?://", "", line).split("/")[0].capitalize()
            output.append(f"- [{name}]({line})")
        else:
            output.append(line)
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Format and clean a profile into styled markdown with shortened links.")
    parser.add_argument('--input', type=str, required=True, help="Input file containing raw profile text")
    parser.add_argument('--output', type=str, help="Output file (optional)")
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        raw = f.read()

    shortened = shorten_links_in_text(raw)
    body = format_profile_section(shortened)

    final = f"{HEADER}\n{body}\n{FOOTER}"

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(final)
    else:
        print(final)

if __name__ == "__main__":
    main()
