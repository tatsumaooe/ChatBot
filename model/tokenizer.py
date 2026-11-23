
class CharTokenizer:

    def __init__(self, text):

        # Build vocabulary from unique characters
        self.chars = sorted(set(text))

        self.vocab_size = len(self.chars)

        # Character -> ID
        self.stoi = {
            ch: i for i, ch in enumerate(self.chars)
        }

        # ID -> Character
        self.itos = {
            i: ch for i, ch in enumerate(self.chars)
        }

    def encode(self, text):

        return [
            self.stoi[ch] for ch in text
        ]

    def decode(self, token_ids):

        return "".join(
            self.itos[i] for i in token_ids
        )


if __name__ == "__main__":

    text = """
    hello world
    hello GPT
    I am building my own AI model.
    """

    tokenizer = CharTokenizer(text)

    print("Vocabulary size:", tokenizer.vocab_size)

    sample = "hello GPT"

    encoded = tokenizer.encode(sample)

    decoded = tokenizer.decode(encoded)

    print("\nOriginal text:")
    print(sample)

    print("\nEncoded tokens:")
    print(encoded)

    print("\nDecoded text:")
    print(decoded)

    print("\nVocabulary:")
    print(tokenizer.stoi)
