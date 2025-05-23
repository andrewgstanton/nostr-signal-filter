
import argparse
import os
import sys
from utils import shorten_links_in_text

def main():
    parser = argparse.ArgumentParser(description="Shorten all URLs in a text or markdown post using TinyURL.")
    parser.add_argument('--input', type=str, help="Path to input file. If omitted, reads from stdin.")
    parser.add_argument('--output', type=str, help="Path to save output. If omitted, prints to stdout.")
    args = parser.parse_args()

    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    processed = shorten_links_in_text(content)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(processed)
    else:
        print(processed)

if __name__ == "__main__":
    main()
