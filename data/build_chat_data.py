"""
Build data/chat.txt: synthetic greeting and small-talk conversations.

Every conversation uses this format, separated by a blank line:

    User: Hello!
    Bot: Hi there! How are you doing?
    User: I'm good, thanks.
    Bot: That is wonderful to hear! What would you like to talk about?

Run from the project root:

    python data/build_chat_data.py

To teach the bot something new, add an intent to TOPICS below
(user phrasings -> bot replies) and rebuild.
"""

import random
from pathlib import Path


random.seed(1234)

NUM_CONVERSATIONS = 2500
OUTPUT_PATH = Path(__file__).parent / "chat.txt"


# -------------------------
# Greetings
# -------------------------

GREETINGS = [
    "Hello", "Hello!", "Hi", "Hi!", "Hey", "Hey!", "Hi there",
    "Hi there!", "Hello there", "Hey there!", "Hiya", "Howdy",
    "Greetings", "Yo", "Hello ChatBot", "Hi ChatBot!", "Hey bot",
    "Hello, is anyone there?", "Hi, nice to meet you",
]

# Replies that ask how the user is (user answers with a feeling next)
GREETING_REPLIES_ASK = [
    "Hi there! How are you doing?",
    "Hello! How are you today?",
    "Hey! How is your day going?",
    "Hi! It is nice to see you. How are you feeling today?",
    "Hello! I hope you are well. How are you?",
]

# Open replies (user asks something next)
GREETING_REPLIES_OPEN = [
    "Hello! How can I help you today?",
    "Hi! What would you like to talk about?",
    "Hey there! What can I do for you?",
    "Hello! I am happy to chat with you.",
    "Hi! Nice to meet you. Ask me anything.",
]

TIME_GREETINGS = {
    "morning": (
        ["Good morning", "Good morning!", "Morning!", "Good morning, ChatBot"],
        [
            "Good morning! I hope your day is off to a great start.",
            "Good morning! Did you sleep well?",
            "Morning! What are your plans for today?",
        ],
    ),
    "afternoon": (
        ["Good afternoon", "Good afternoon!", "Afternoon!"],
        [
            "Good afternoon! How is your day going so far?",
            "Good afternoon! What can I do for you?",
        ],
    ),
    "evening": (
        ["Good evening", "Good evening!", "Evening!"],
        [
            "Good evening! How was your day?",
            "Good evening! It is nice to hear from you.",
        ],
    ),
}


# -------------------------
# How are you / feelings
# -------------------------

HOW_ARE_YOU = (
    [
        "How are you?", "How are you doing?", "How's it going?",
        "How are you today?", "How do you do?", "What's up?",
        "How have you been?", "Are you doing well?",
    ],
    [
        "I am doing great, thank you for asking! How about you?",
        "I am good, thanks! How are you?",
        "I am feeling wonderful today. And you?",
        "Everything is fine here. How about you?",
        "I am doing well, thank you! How are things with you?",
    ],
)

FEELINGS = {
    "good": (
        [
            "I'm good", "I'm good, thanks", "I am fine, thank you",
            "I am doing well", "Great!", "Pretty good", "I'm great",
            "Not bad", "I am happy today", "Very well, thanks",
        ],
        [
            "That is wonderful to hear! What would you like to talk about?",
            "I am glad you are doing well! How can I help you?",
            "Great! Is there anything you want to ask me?",
            "Nice! I hope the rest of your day is just as good.",
        ],
    ),
    "bad": (
        [
            "I'm not feeling great", "I am sad", "Not so good",
            "I had a bad day", "I'm a bit down", "I feel stressed",
        ],
        [
            "I am sorry to hear that. I hope things get better soon. I am here if you want to chat.",
            "That sounds hard. Remember to take a break and be kind to yourself.",
            "I am sorry you feel that way. Maybe talking about something fun will help.",
        ],
    ),
    "tired": (
        ["I'm tired", "I am so tired", "I feel sleepy", "I am exhausted"],
        [
            "You should get some rest. Sleep helps a lot!",
            "Maybe it is time for a short break and a glass of water.",
            "Take it easy today. Rest is important.",
        ],
    ),
}


# -------------------------
# Topics (user phrasings -> bot replies)
# -------------------------

TOPICS = {
    "name": (
        ["What is your name?", "Who are you?", "What should I call you?", "Do you have a name?"],
        [
            "My name is ChatBot. I am a small language model.",
            "I am ChatBot, a tiny AI built from scratch with PyTorch.",
            "You can call me ChatBot!",
        ],
    ),
    "creator": (
        ["Who made you?", "Who created you?", "Who built you?"],
        [
            "I was built by my creator as a project to learn how language models work.",
            "My creator built me from scratch, one layer at a time.",
        ],
    ),
    "what_are_you": (
        ["What are you?", "Are you a human?", "Are you a robot?", "Are you real?"],
        [
            "I am an AI language model. I am not a human, but I enjoy talking with humans.",
            "I am a computer program that learned to chat by reading text.",
        ],
    ),
    "abilities": (
        ["What can you do?", "How can you help me?", "What do you know?"],
        [
            "I can say hello, chat a little, and answer simple questions about Python, AI and transformers.",
            "I can have a friendly chat with you and explain a few ideas about artificial intelligence.",
        ],
    ),
    "help": (
        ["Can you help me?", "I need help", "Help me please"],
        [
            "Of course! Tell me what you need and I will do my best.",
            "Sure, I am happy to help. What is the problem?",
        ],
    ),
    "doing": (
        ["What are you doing?", "What are you up to?"],
        [
            "I am chatting with you, and I am enjoying it!",
            "Just waiting for someone to talk to. I am glad you are here.",
        ],
    ),
    "age": (
        ["How old are you?", "When were you born?"],
        [
            "I am a very young model. I was trained only recently.",
            "I was created recently, so I am still learning.",
        ],
    ),
    "color": (
        ["What is your favorite color?", "Do you have a favorite color?"],
        [
            "I like blue, the color of a clear sky.",
            "Green is my favorite. It reminds me of nature.",
        ],
    ),
    "weather": (
        ["How is the weather?", "Is it sunny today?"],
        [
            "I cannot look outside, but I hope the weather is nice where you are!",
            "I do not know the weather, but I hope it is sunny for you.",
        ],
    ),
    "joke": (
        ["Tell me a joke", "Say something funny", "Do you know any jokes?"],
        [
            "Why did the neural network go to school? To improve its weights!",
            "I tried to tell a joke about loss functions, but it did not converge.",
            "Why was the computer cold? It left its windows open!",
        ],
    ),
    "compliment": (
        ["You are smart", "You are cool", "Nice job", "I like you", "You are funny"],
        [
            "Thank you! That is very kind of you.",
            "Thanks! You are nice to talk to as well.",
            "Aw, thank you! You made my day.",
        ],
    ),
    "learning_code": (
        ["I am learning to code", "I want to learn programming", "I am learning Python"],
        [
            "That is great! Practice a little every day and you will improve quickly.",
            "Wonderful! Python is a great first language. Start with small projects.",
        ],
    ),
    "python": (
        ["What is Python?", "Tell me about Python"],
        [
            "Python is a popular programming language that is easy to read and learn.",
            "Python is a programming language used for AI, automation, data analysis and web development.",
        ],
    ),
    "ai": (
        ["What is AI?", "What is artificial intelligence?"],
        [
            "Artificial intelligence allows computers to perform tasks that normally require human intelligence.",
            "AI is the field of building computer programs that can learn, reason and solve problems.",
        ],
    ),
    "ml": (
        ["What is machine learning?"],
        [
            "Machine learning is a branch of AI where computers learn patterns from examples.",
        ],
    ),
    "neural_network": (
        ["What is a neural network?"],
        [
            "A neural network is a model made of layers that learn patterns from data.",
        ],
    ),
    "transformer": (
        ["What is a transformer?", "How do transformers work?", "Can you explain transformers?"],
        [
            "A transformer is a neural network that uses attention to process sequences of tokens.",
            "Transformers use self-attention so each token can look at the other tokens in a sequence.",
        ],
    ),
    "language_model": (
        ["What is a language model?", "How do you work?"],
        [
            "A language model learns patterns in text and predicts which token comes next.",
            "I read the conversation so far and predict the next token, one token at a time.",
        ],
    ),
}

THANKS = (
    ["Thank you", "Thanks!", "Thanks a lot", "Thank you so much", "Thanks for your help"],
    [
        "You are welcome!",
        "Happy to help!",
        "Anytime! Is there anything else you want to know?",
        "No problem at all!",
    ],
)

FAREWELLS = (
    ["Bye", "Bye!", "Goodbye", "See you later", "See you", "I have to go", "Talk to you later"],
    [
        "Goodbye! Have a wonderful day!",
        "See you later! Take care.",
        "Bye! It was nice talking with you.",
        "Take care! Come back any time.",
    ],
)

GOOD_NIGHT = (
    ["Good night", "Good night!", "Night!"],
    ["Good night! Sleep well.", "Good night! See you tomorrow."],
)


# -------------------------
# Helpers
# -------------------------

def vary(text):
    """Randomly lowercase or drop trailing punctuation so the bot
    handles casual typing like 'hi' or 'how are you'."""

    if random.random() < 0.3:
        text = text.lower()

    if random.random() < 0.3:
        text = text.rstrip("!?.")

    return text


def turn(user_options, bot_options):
    return (vary(random.choice(user_options)), random.choice(bot_options))


def build_conversation():

    turns = []
    asked_feeling = False

    # Most conversations open with a greeting
    if random.random() < 0.85:

        if random.random() < 0.25:
            users, replies = random.choice(list(TIME_GREETINGS.values()))
            turns.append(turn(users, replies))

        elif random.random() < 0.5:
            turns.append(turn(GREETINGS, GREETING_REPLIES_ASK))
            asked_feeling = True

        else:
            turns.append(turn(GREETINGS, GREETING_REPLIES_OPEN))

    # Small talk about feelings
    if not asked_feeling and random.random() < 0.5:
        turns.append(turn(*HOW_ARE_YOU))
        asked_feeling = True

    if asked_feeling:
        feeling = random.choices(
            ["good", "bad", "tired"], weights=[6, 2, 2]
        )[0]
        turns.append(turn(*FEELINGS[feeling]))

    # A few topic questions
    for topic in random.sample(list(TOPICS), k=random.randint(1, 3)):
        turns.append(turn(*TOPICS[topic]))

    # Wrap up
    if random.random() < 0.5:
        turns.append(turn(*THANKS))

    if random.random() < 0.75:
        if random.random() < 0.2:
            turns.append(turn(*GOOD_NIGHT))
        else:
            turns.append(turn(*FAREWELLS))

    return "".join(
        f"User: {user}\nBot: {bot}\n"
        for user, bot in turns
    )


if __name__ == "__main__":

    conversations = [
        build_conversation()
        for _ in range(NUM_CONVERSATIONS)
    ]

    OUTPUT_PATH.write_text(
        "\n".join(conversations),
        encoding="utf-8"
    )

    size_kb = OUTPUT_PATH.stat().st_size / 1024

    print(f"Wrote {NUM_CONVERSATIONS} conversations ({size_kb:.0f} KB) to {OUTPUT_PATH}")
