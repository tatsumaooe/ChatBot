
import torch
from pathlib import Path

from model.bpe_tokenizer import BPETokenizer


# 1. Load training text
#    training.txt: general knowledge prose
#    chat.txt: User/Bot conversations (built by data/build_chat_data.py)
DATA_FILES = [
    Path("data/training.txt"),
    Path("data/chat.txt"),
]

text = "\n\n".join(
    path.read_text(encoding="utf-8")
    for path in DATA_FILES
)


# 2. Train tokenizer
tokenizer = BPETokenizer()

tokenizer.train(text, num_merges=300)

tokenizer.build_vocabulary_ids()

vocab_size = len(tokenizer.stoi)


# 3. Convert text into token IDs
token_ids = tokenizer.encode_ids(text)

data = torch.tensor(token_ids, dtype=torch.long)


# 4. Split dataset
split = int(0.9 * len(data))

train_data = data[:split]
val_data = data[split:]


# 5. Generate training batches
def get_batch(data, batch_size=2, block_size=16):

    if len(data) <= block_size:
        raise ValueError("Not enough tokens for this block size")

    ix = torch.randint(
        len(data) - block_size,
        (batch_size,)
    )

    x = torch.stack([
        data[i:i + block_size]
        for i in ix
    ])

    y = torch.stack([
        data[i + 1:i + block_size + 1]
        for i in ix
    ])

    return x, y


# 6. Test dataset
if __name__ == "__main__":

    x, y = get_batch(train_data)

    print("Vocabulary size:", vocab_size)
    print("Total tokens:", len(data))

    print("Training tokens:", len(train_data))
    print("Validation tokens:", len(val_data))

    print("\nInput shape:", x.shape)
    print("Target shape:", y.shape)

    print("\nInput:")
    print(x)

    print("\nTargets:")
    print(y)
