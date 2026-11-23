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

# 3. Chat with it in your browser
python -m model.server --open

# ...or in the terminal
python -m model.chat
```

On Windows you can also just double-click `start_chatbot.bat`, which starts the
server and opens the chat page.

## Web chat

`python -m model.server` starts a small web server (Python standard library
only, nothing extra to install) at http://localhost:8000.

- `web/` holds the chat page: message bubbles, typing indicator, quick-reply
  buttons, light/dark mode, works on phones. The conversation is saved in the
  browser, and "New chat" clears it.
- `POST /api/chat` with `{"message": "...", "history": [["user", "bot"], ...]}`
  returns `{"reply": "..."}`. Any other app (mobile, Discord bot, etc.) can
  use the same endpoint.
- `--host 0.0.0.0` makes it reachable from other devices on your network;
  `--port` changes the port.
- Set `CHATBOT_CHECKPOINT` to load a different model file.

## Training data

- `data/training.txt`: short general-knowledge text.
- `data/slang.json`: 664 family-friendly slang terms (Gen Z, internet and
  gaming, millennial, retro, and regional UK/Australia/etc.), each with a
  meaning, a funny example, and spelling aliases. Meanings and examples are
  original writing; terms that are sexual, drug-related, profane, or insult a
  group of people were left out on purpose.
- `data/friend_chat.json`: 166 conversation topics across work, study, daily
  life and hobbies (about 2,000 ways users open a topic and 500 follow-up
  branches), so the bot can chat like a friend: it reacts, asks a question,
  and responds to the answer.
- `data/chat.txt`: generated `User:` / `Bot:` conversations built from all of
  the above plus the small-talk intents in `data/build_chat_data.py`.

To teach the bot something new, add a term to `data/slang.json`, a topic to
`data/friend_chat.json`, or an intent to `TOPICS` in
`data/build_chat_data.py`, then rebuild the data and retrain.

## Safety

`model/safety.py` catches messages about self-harm, suicide, abuse or danger
and answers them with a fixed, caring reply that points to real help (crisis
lines, emergency numbers) instead of a generated reply. Review the patterns and
help lines for every country you launch in. Run `python -m model.safety` to
test it.
Training saves a checkpoint every 250 steps, so an interrupted run keeps its
progress.
