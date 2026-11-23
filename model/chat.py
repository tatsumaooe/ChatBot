
import sys

import torch

from model.generate import model, tokenizer, device, checkpoint
from model.safety import safety_reply



# -------------------------
# Configuration
# -------------------------

MAX_REPLY_TOKENS = 120
TEMPERATURE = 0.5
TOP_K = 10

# Previous exchanges kept as context for the next reply
HISTORY_TURNS = 3


# -------------------------
# Generate one reply
# -------------------------

@torch.no_grad()
def reply(prompt):

    idx = torch.tensor(
        [tokenizer.encode_ids(prompt)],
        dtype=torch.long,
        device=device
    )

    reply_tokens = []

    for _ in range(MAX_REPLY_TOKENS):

        # Keep context within model limits
        idx_cond = idx[:, -checkpoint["max_seq_len"]:]

        logits, _ = model(idx_cond)

        logits = logits[:, -1, :] / TEMPERATURE

        # Sample from the top-k tokens
        values, indices = torch.topk(
            logits,
            k=min(TOP_K, logits.size(-1)),
            dim=-1
        )

        probabilities = torch.softmax(values, dim=-1)

        sampled_index = torch.multinomial(
            probabilities,
            num_samples=1
        )

        next_token = torch.gather(indices, -1, sampled_index)

        token = tokenizer.itos[next_token.item()]

        # A newline means the bot has finished its line
        if "\n" in token:
            break

        reply_tokens.append(token)

        idx = torch.cat((idx, next_token), dim=1)

    return "".join(reply_tokens).strip()


# -------------------------
# Respond to one message
# -------------------------

def respond(user_message, history=()):
    """Return the bot's reply.

    history: previous (user, bot) message pairs, oldest first.
    Used by both the terminal chat and the web server.
    """

    # Newlines would break the "User: ... / Bot: ..." format
    user_message = " ".join(user_message.split())

    # Serious messages get a fixed, caring reply, never a joke
    answer = safety_reply(user_message)

    if answer is not None:
        return answer

    context = "".join(
        f"User: {user}\nBot: {bot}\n"
        for user, bot in list(history)[-HISTORY_TURNS:]
    )

    return reply(f"{context}User: {user_message}\nBot:")


# -------------------------
# Chat loop
# -------------------------

def main():

    # Replies contain emoji; make sure Windows terminals and pipes
    # don't crash trying to print them in a legacy encoding
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

    print("\nChat with your bot! Type 'quit' to exit.\n")

    history = []

    while True:

        try:
            user_message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_message:
            continue

        if user_message.lower() in {"quit", "exit"}:
            break

        answer = respond(user_message, history)

        print(f"Bot: {answer}")

        history.append((user_message, answer))


if __name__ == "__main__":
    main()
