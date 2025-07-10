const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");

chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const msg = input.value.trim();
    if (!msg) return;

    appendMessage("user", msg);
    input.value = "";

    appendMessage("bot", "Typing...");

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    });

    const data = await res.json();
    replaceLastBotMessage(data.reply);
});

function appendMessage(sender, text) {
    const div = document.createElement("div");
    div.classList.add(`${sender}-msg`);
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function replaceLastBotMessage(text) {
    const msgs = document.querySelectorAll(".bot-msg");
    if (msgs.length) msgs[msgs.length - 1].innerText = text;
}