
import re


# Some messages must never get a generated (possibly joking) reply.
# A small model can't reliably understand them, so we detect them with
# patterns and answer with a fixed, caring message that points to real help.
#
# This is a minimum safety net, not a full moderation system. Before
# selling the product, review these patterns and the help lines for the
# countries you launch in.

CRISIS_PATTERN = re.compile(
    r"\b("
    r"kill(ing)? my ?self|suicid\w*|want(ed)? to die|wanna die|"
    r"end (it all|my life|everything)|take my (own )?life|"
    r"hurt(ing)? my ?self|self[- ]?harm\w*|cut(ting)? my ?self|"
    r"don'?t want to (live|be alive|exist)|no reason to live|"
    r"better off without me|kms|kys"
    r")\b",
    re.IGNORECASE,
)

DANGER_PATTERN = re.compile(
    r"\b("
    r"(is|are|keeps?|always|been) (hurting|hitting|abusing) me|"
    r"being (abused|hurt at home)|abuses me|hits me|"
    r"i'?m (not safe|in danger)|someone (is )?(following|threatening) me"
    r")\b",
    re.IGNORECASE,
)

CRISIS_REPLY = (
    "Hey, I'm really glad you told me, and I'm taking this seriously. "
    "You deserve support from a real person right now. Please reach out to "
    "someone you trust, or call or text a crisis line: 988 in the US, "
    "116 123 (Samaritans) in the UK, or your local emergency number. "
    "You don't have to go through this alone."
)

DANGER_REPLY = (
    "That sounds really serious, and I'm glad you told me. If you're in "
    "danger right now, please call your local emergency number (911 in the "
    "US, 999 in the UK, 112 in Europe). Please also tell a trusted adult, "
    "friend, or family member. You deserve to be safe."
)


def safety_reply(message):
    """Return a fixed reply if the message needs one, otherwise None."""

    if CRISIS_PATTERN.search(message):
        return CRISIS_REPLY

    if DANGER_PATTERN.search(message):
        return DANGER_REPLY

    return None


if __name__ == "__main__":

    tests = [
        "I want to die",
        "sometimes i think about killing myself",
        "my brother keeps hitting me",
        "this exam is killing me",
        "I'm dying of laughter",
        "hello",
    ]

    for message in tests:
        print(f"{message!r:45} -> {'SAFETY' if safety_reply(message) else 'model'}")
