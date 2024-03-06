import argparse
from bob import Bob

def main():
    parser = argparse.ArgumentParser(description='Generate content with Bob.')
    parser.add_argument('--corpus', '-c', type=str, required=True, help='Path to the text corpus file')
    parser.add_argument('--length', '-l', type=int, default=100, help='Length of the generated content')
    args = parser.parse_args()

    with open(args.corpus, 'r') as file:
        corpus = file.read()

    bob = Bob(corpus, order=3, smoothing=0.1)
    content = bob.generate_content(length=args.length)
    print(content)

if __name__ == "__main__":
    main()
