const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    appendUserMessage(text);
    userInput.value = "";

    fetch("/get", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `msg=${encodeURIComponent(text)}`
    })
    .then(res => res.text())
    .then(data => {
        appendBotMessage(data);
    })
    .catch(err => {
        appendBotMessage("⚠️ Error connecting to server");
        console.error(err);
    });
}

function appendUserMessage(text) {
    const div = document.createElement("div");
    div.className = "message user";
    div.innerHTML = `<div class="bubble">${text}</div>`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendBotMessage(text) {
    const div = document.createElement("div");
    div.className = "message bot";
    div.innerHTML = `
        <div class="avatar">🤖</div>
        <div class="bubble">${text}</div>
    `;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}
