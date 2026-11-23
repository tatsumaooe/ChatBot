
import re
from collections import Counter


class BPETokenizer:

    def __init__(self):
        self.merges = []
        self.vocab = set()

    def split_text(self, text):
        # Preserve words, whitespace and punctuation
        return re.findall(r"\w+|[^\w\s]+|\s+", text)

    @staticmethod
    def merge_pair(tokens, pair):

        merged = []
        j = 0

        while j < len(tokens):

            if (
                j < len(tokens) - 1
                and (tokens[j], tokens[j + 1]) == pair
            ):
                merged.append(tokens[j] + tokens[j + 1])
                j += 2
            else:
                merged.append(tokens[j])
                j += 1

        return merged

    def train(self, text, num_merges=20):

        # Merges never cross piece boundaries, so each unique piece
        # only needs to be processed once, weighted by its count
        piece_counts = Counter(self.split_text(text))

        pieces = {
            piece: list(piece)
            for piece in piece_counts
        }

        self.vocab = {
            token
            for tokens in pieces.values()
            for token in tokens
        }

        for _ in range(num_merges):

            pairs = Counter()

            # Count adjacent pairs within each piece
            for piece, tokens in pieces.items():
                count = piece_counts[piece]
                for pair in zip(tokens, tokens[1:]):
                    pairs[pair] += count

            if not pairs:
                break

            best_pair, frequency = pairs.most_common(1)[0]

            if frequency < 2:
                break

            self.merges.append(best_pair)
            self.vocab.add("".join(best_pair))

            # Apply merge to every piece
            for piece, tokens in pieces.items():
                pieces[piece] = self.merge_pair(tokens, best_pair)

    def encode(self, text):

        cache = {}
        result = []

        for piece in self.split_text(text):

            if piece not in cache:

                tokens = list(piece)

                for pair in self.merges:
                    tokens = self.merge_pair(tokens, pair)

                cache[piece] = tokens

            result.extend(cache[piece])

        return result


    def build_vocabulary_ids(self):

        self.tokens = sorted(self.vocab)

        self.stoi = {
            token: i
            for i, token in enumerate(self.tokens)
        }

        self.itos = {
            i: token
            for i, token in enumerate(self.tokens)
        }

    def encode_ids(self, text):

        tokens = self.encode(text)

        # Skip characters never seen during training
        # (e.g. emoji typed into the chat) instead of crashing
        return [
            self.stoi[token]
            for token in tokens
            if token in self.stoi
        ]

    def decode_ids(self, token_ids):

        tokens = [
            self.itos[token_id]
            for token_id in token_ids
        ]

        return self.decode(tokens)


    def decode(self, tokens):
        return "".join(tokens)


if __name__ == "__main__":

    text = (
        "low lower lowest "
        "low lower lowest "
        "new newer newest "
    ) * 10

    tokenizer = BPETokenizer()

    tokenizer.train(text, num_merges=20)
    tokenizer.build_vocabulary_ids()

    sample = "low lower newest"

    ids = tokenizer.encode_ids(sample)

    print("Token IDs:", ids)
    print("Vocabulary size:", len(tokenizer.stoi))
    print("Decoded:", tokenizer.decode_ids(ids))
  