import random
from collections import defaultdict
from nltk.tokenize import word_tokenize

class Bob:
    def __init__(self, corpus, order=3, smoothing=0.1):
        self.order = order
        self.smoothing = smoothing
        self.word_dict = self.generate_word_dict(corpus)

    def generate_word_dict(self, corpus):
        word_dict = defaultdict(lambda: defaultdict(float))
        words = word_tokenize(corpus.lower())
        for i in range(len(words) - self.order):
            context = tuple(words[i:i + self.order])
            next_word = words[i + self.order]
            word_dict[context][next_word] += 1
        for context in word_dict:
            total_count = sum(word_dict[context].values())
            for word in word_dict[context]:
                word_dict[context][word] = (word_dict[context][word] + self.smoothing) / (total_count + self.smoothing * len(word_dict[context]))
        return word_dict

    def generate_content(self, length=50):
        start_index = random.randint(0, len(self.word_dict) - 1)
        current_context = list(self.word_dict.keys())[start_index]
        content = ' '.join(current_context).capitalize()

        for _ in range(length - self.order):
            if current_context in self.word_dict:
                next_word = self.select_next_word(current_context)
                content += ' ' + next_word
                current_context = current_context[1:] + (next_word,)
            else:
                break

        # Add punctuation at the end
        if content[-1] not in ['.', '!', '?']:
            content += '.'

        return content

    def select_next_word(self, context):
        probabilities = self.word_dict[context]
        rand_prob = random.random()
        cumulative_prob = 0
        for word, prob in probabilities.items():
            cumulative_prob += prob
            if rand_prob <= cumulative_prob:
                return word

if __name__ == "__main__":
    # Example usage
    corpus = """Your text corpus goes here. It should be a long text with several sentences. 
                Ensure that the text is representative and diverse to improve content generation."""
    bob = Bob(corpus, order=3, smoothing=0.1)
    content = bob.generate_content(length=100)
    print(content)
