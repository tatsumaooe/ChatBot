
import os

import torch

from pathlib import Path

from model.gpt_model import GPTLanguageModel
from model.bpe_tokenizer import BPETokenizer


# -------------------------
# Configuration
# -------------------------

# Set CHATBOT_CHECKPOINT to use a different model file
CHECKPOINT_PATH = Path(
    os.environ.get("CHATBOT_CHECKPOINT", "checkpoints/mygpt.pt")
)

MAX_NEW_TOKENS = 50
TEMPERATURE = 0.8


# -------------------------
# Load checkpoint
# -------------------------

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

checkpoint = torch.load(
    CHECKPOINT_PATH,
    map_location=device,
    weights_only=True
)

print("Device:", device)


# -------------------------
# Restore tokenizer
# -------------------------

tokenizer = BPETokenizer()

tokenizer.merges = checkpoint["merges"]
tokenizer.stoi = checkpoint["stoi"]
tokenizer.itos = checkpoint["itos"]
tokenizer.vocab = set(tokenizer.stoi.keys())


# -------------------------
# Rebuild GPT
# -------------------------

model = GPTLanguageModel(
    vocab_size=checkpoint["vocab_size"],
    embedding_dim=checkpoint["embedding_dim"],
    num_heads=checkpoint["num_heads"],
    num_layers=checkpoint["num_layers"],
    max_seq_len=checkpoint["max_seq_len"]
).to(device)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model.eval()

print("GPT model loaded successfully!")


# -------------------------
# Text generation
# -------------------------

@torch.no_grad()
def generate(prompt, max_new_tokens=50, temperature=0.8):

    if temperature <= 0:
        raise ValueError("Temperature must be greater than zero")

    # Encode prompt
    prompt_tokens = tokenizer.encode_ids(prompt)

    if not prompt_tokens:
        raise ValueError("Prompt cannot be empty")

    idx = torch.tensor(
        [prompt_tokens],
        dtype=torch.long,
        device=device
    )

    for _ in range(max_new_tokens):

        # Keep context within model limits
        idx_cond = idx[:, -checkpoint["max_seq_len"]:]

        # Predict next token
        logits, loss = model(idx_cond)

        logits = logits[:, -1, :]

        # Temperature sampling
        logits = logits / temperature

        # Keep only the top 10 predictions
        top_k = 10

        values, indices = torch.topk(
            logits,
            k=min(top_k, logits.size(-1)),
            dim=-1
        )

        # Convert remaining scores into probabilities
        probabilities = torch.softmax(values, dim=-1)

        # Sample from top-k tokens
        sampled_index = torch.multinomial(
            probabilities,
            num_samples=1
        )

        # Recover original vocabulary token ID
        next_token = torch.gather(
            indices,
            -1,
            sampled_index
        )
        # Append generated token
        idx = torch.cat(
            (idx, next_token),
            dim=1
        )

    # Decode generated sequence
    return tokenizer.decode_ids(
        idx[0].tolist()
    )


# -------------------------
# Test generation
# -------------------------

if __name__ == "__main__":

    prompt = "Hello"

    print("\nPrompt:", prompt)

    result = generate(
        prompt,
        max_new_tokens=50,
        temperature=TEMPERATURE
    )

    print("\nGenerated text:")
    print(result)
