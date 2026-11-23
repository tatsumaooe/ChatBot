
import torch
import torch.nn as nn
from pathlib import Path

from model.gpt_model import GPTLanguageModel
from model.dataset import tokenizer, train_data, val_data, get_batch


# -------------------------
# Configuration
# -------------------------

BATCH_SIZE = 32
BLOCK_SIZE = 128
MAX_ITERS = 3000
LEARNING_RATE = 0.001
EVAL_INTERVAL = 250
EVAL_ITERS = 20

EMBEDDING_DIM = 128
NUM_HEADS = 4
NUM_LAYERS = 4
MAX_SEQ_LEN = 128


# -------------------------
# Device
# -------------------------

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Selected device:", device)


# -------------------------
# Initialize GPT
# -------------------------

vocab_size = len(tokenizer.stoi)

model = GPTLanguageModel(
    vocab_size=vocab_size,
    embedding_dim=EMBEDDING_DIM,
    num_heads=NUM_HEADS,
    num_layers=NUM_LAYERS,
    max_seq_len=MAX_SEQ_LEN
).to(device)

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE
)

print("Vocabulary size:", vocab_size)

print(
    "Parameters:",
    sum(p.numel() for p in model.parameters())
)


# -------------------------
# Evaluate model
# -------------------------

@torch.no_grad()
def estimate_loss():

    model.eval()

    results = {}

    for split, data in [
        ("train", train_data),
        ("val", val_data)
    ]:

        losses = torch.zeros(EVAL_ITERS)

        for k in range(EVAL_ITERS):

            x, y = get_batch(
                data,
                batch_size=BATCH_SIZE,
                block_size=BLOCK_SIZE
            )

            x = x.to(device)
            y = y.to(device)

            logits, loss = model(x, y)

            losses[k] = loss.item()

        results[split] = losses.mean().item()

    model.train()

    return results


# -------------------------
# Training loop
# -------------------------

print("\nStarting training...\n")

for iteration in range(MAX_ITERS):

    if iteration % EVAL_INTERVAL == 0:

        losses = estimate_loss()

        print(
            f"Step {iteration}: "
            f"Train Loss: {losses['train']:.4f}, "
            f"Val Loss: {losses['val']:.4f}"
        )

    # Get training batch
    x, y = get_batch(
        train_data,
        batch_size=BATCH_SIZE,
        block_size=BLOCK_SIZE
    )

    x = x.to(device)
    y = y.to(device)

    # Forward pass
    logits, loss = model(x, y)

    # Clear old gradients
    optimizer.zero_grad(set_to_none=True)

    # Backpropagation
    loss.backward()

    # Prevent excessively large gradients
    nn.utils.clip_grad_norm_(
        model.parameters(),
        max_norm=1.0
    )

    # Update model parameters
    optimizer.step()


# -------------------------
# Save model
# -------------------------

checkpoint_dir = Path("checkpoints")
checkpoint_dir.mkdir(exist_ok=True)

checkpoint_path = checkpoint_dir / "mygpt.pt"

torch.save(
    {
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "vocab_size": vocab_size,
        "embedding_dim": EMBEDDING_DIM,
        "num_heads": NUM_HEADS,
        "num_layers": NUM_LAYERS,
        "max_seq_len": MAX_SEQ_LEN,
        "block_size": BLOCK_SIZE,
        "merges": tokenizer.merges,
        "stoi": tokenizer.stoi,
        "itos": tokenizer.itos,
    },
    checkpoint_path
)

print("\nTraining completed!")
print("Model saved to:", checkpoint_path)
