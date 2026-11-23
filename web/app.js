// ChatBot web UI: sends messages to /api/chat and shows the replies.

(function () {
  "use strict";

  var STORAGE_KEY = "chatbot.conversation.v1";
  var HISTORY_PAIRS = 3;      // previous exchanges sent as context
  var MIN_TYPING_MS = 450;    // feels more natural than an instant reply

  var WELCOME =
    "Yooo! I'm ChatBot, your new favorite chat buddy. 😎 Talk to me about " +
    "work, school, life, or ask me what any slang means. What's good?";

  var CHIPS = [
    ["👋 Say hi", "Hey!"],
    ["😂 Tell me a joke", "Tell me a joke"],
    ["🔥 Roast me", "Roast me"],
    ["🧠 Teach me slang", "Teach me some slang"],
    ["😩 Work was rough", "ugh work was so stressful today"],
    ["📚 Exam tomorrow", "I have an exam tomorrow"],
    ["🎲 Would you rather", "would you rather"],
    ["🤓 Fun fact", "tell me a fun fact"],
    ["😴 I'm bored", "I'm bored"]
  ];

  var messagesEl = document.getElementById("messages");
  var typingEl = document.getElementById("typing");
  var chipsEl = document.getElementById("chips");
  var form = document.getElementById("form");
  var input = document.getElementById("input");
  var sendBtn = document.getElementById("send");
  var newChatBtn = document.getElementById("new-chat");

  // Each message: {role: "user" | "bot", text: "...", error?: true}
  var conversation = load();
  var busy = false;

  // ---------- Storage ----------

  function load() {
    try {
      var saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
      if (Array.isArray(saved) && saved.length) return saved;
    } catch (e) {
      // ignore broken storage
    }
    return [{ role: "bot", text: WELCOME }];
  }

  function save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(conversation.slice(-100)));
    } catch (e) {
      // storage full or disabled: chat still works
    }
  }

  // ---------- Rendering ----------

  function renderMessage(msg) {
    var row = document.createElement("div");
    row.className = "row " + msg.role;

    if (msg.role === "bot") {
      var avatar = document.createElement("div");
      avatar.className = "avatar small";
      avatar.setAttribute("aria-hidden", "true");
      avatar.textContent = "😎";
      row.appendChild(avatar);
    }

    var bubble = document.createElement("div");
    bubble.className = "bubble " + msg.role + (msg.error ? " error" : "");
    bubble.textContent = msg.text;   // textContent: never inject HTML
    row.appendChild(bubble);

    messagesEl.appendChild(row);
  }

  function renderAll() {
    messagesEl.textContent = "";
    conversation.forEach(renderMessage);
    scrollToBottom();
  }

  function scrollToBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function addMessage(msg) {
    conversation.push(msg);
    renderMessage(msg);
    save();
    scrollToBottom();
  }

  function renderChips() {
    CHIPS.forEach(function (chip) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "chip";
      btn.textContent = chip[0];
      btn.addEventListener("click", function () {
        send(chip[1]);
      });
      chipsEl.appendChild(btn);
    });
  }

  function setBusy(value) {
    busy = value;
    typingEl.hidden = !value;
    sendBtn.disabled = value || !input.value.trim();
    if (value) scrollToBottom();
  }

  // ---------- Talking to the server ----------

  // Last few completed (user, bot) pairs, oldest first
  function recentHistory() {
    var pairs = [];
    for (var i = 0; i < conversation.length - 1; i++) {
      var a = conversation[i];
      var b = conversation[i + 1];
      if (a.role === "user" && b.role === "bot" && !b.error) {
        pairs.push([a.text, b.text]);
      }
    }
    return pairs.slice(-HISTORY_PAIRS);
  }

  function wait(ms) {
    return new Promise(function (resolve) {
      setTimeout(resolve, ms);
    });
  }

  function send(text) {
    text = (text || "").trim();
    if (!text || busy) return;

    var history = recentHistory();

    addMessage({ role: "user", text: text });
    input.value = "";
    autoGrow();
    setBusy(true);

    var request = fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history: history })
    }).then(function (res) {
      return res.json().then(function (data) {
        if (!res.ok || !data.reply) {
          throw new Error(data.error || "Server error");
        }
        return data.reply;
      });
    });

    Promise.all([request, wait(MIN_TYPING_MS)])
      .then(function (results) {
        addMessage({ role: "bot", text: results[0] });
      })
      .catch(function () {
        addMessage({
          role: "bot",
          error: true,
          text: "Oops, I lost connection. 😵 Is the ChatBot server still running?"
        });
      })
      .finally(function () {
        setBusy(false);
        input.focus();
      });
  }

  // ---------- Input handling ----------

  function autoGrow() {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 140) + "px";
    // Only show a scrollbar once the text is taller than the box
    input.style.overflowY = input.scrollHeight > 140 ? "auto" : "hidden";
    sendBtn.disabled = busy || !input.value.trim();
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    send(input.value);
  });

  input.addEventListener("keydown", function (event) {
    // Enter sends; Shift+Enter makes a new line
    if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
      event.preventDefault();
      send(input.value);
    }
  });

  input.addEventListener("input", autoGrow);

  newChatBtn.addEventListener("click", function () {
    if (busy) return;
    conversation = [{ role: "bot", text: WELCOME }];
    save();
    renderAll();
    input.focus();
  });

  // ---------- Start ----------

  renderChips();
  renderAll();
  autoGrow();
  input.focus();
})();
