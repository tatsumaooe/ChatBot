# ChatBot
This is my first ChatBot

A small GPT-style language model built from scratch with PyTorch, trained to
greet people and make small talk.

## Usage

Run all commands from the project root.

```bash
# 1. Build the conversation dataset (data/chat.txt)
python data/build_chat_data.py

# 2. Train the model (saves checkpoints/mygpt.pt)
python -m model.train

# 3. Chat with it
python -m model.chat
```

## Training data

- `data/training.txt`: short general-knowledge text.
- `data/chat.txt`: generated `User:` / `Bot:` conversations. To teach the bot
  new replies, add an intent to `TOPICS` in `data/build_chat_data.py`, rebuild
  the data, and retrain.
