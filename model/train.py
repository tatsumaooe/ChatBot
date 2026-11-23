
import time

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
MAX_ITERS = 7000
LEARNING_RATE = 0.001
EVAL_INTERVAL = 250
EVAL_ITERS = 20

EMBEDDING_DIM = 192
NUM_HEADS = 6
NUM_LAYERS = 6
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

# Slowly lower the learning rate so the model settles
# on exact answers near the end of training
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=MAX_ITERS,
    eta_min=LEARNING_RATE / 10
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
# Save model
# -------------------------

checkpoint_dir = Path("checkpoints")
checkpoint_dir.mkdir(exist_ok=True)

checkpoint_path = checkpoint_dir / "mygpt.pt"


def save_checkpoint():

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


# -------------------------
# Training loop
# -------------------------

print("\nStarting training...\n")

start_time = time.time()

for iteration in range(MAX_ITERS):

    if iteration % EVAL_INTERVAL == 0:

        losses = estimate_loss()

        minutes = (time.time() - start_time) / 60

        print(
            f"Step {iteration}: "
            f"Train Loss: {losses['train']:.4f}, "
            f"Val Loss: {losses['val']:.4f} "
            f"({minutes:.1f} min)"
        )

        # Save progress so an interrupted run isn't lost
        if iteration > 0:
            save_checkpoint()

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
    scheduler.step()


losses = estimate_loss()

print(
    f"Final: Train Loss: {losses['train']:.4f}, "
    f"Val Loss: {losses['val']:.4f}"
)

save_checkpoint()

print("\nTraining completed!")
print("Model saved to:", checkpoint_path)
