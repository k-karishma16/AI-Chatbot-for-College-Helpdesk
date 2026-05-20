function appendMessage(message, sender) {
    const chatBox = document.getElementById("chat-box");

    const msgDiv = document.createElement("div");
    msgDiv.className = sender === "user" ? "user-message" : "bot-message";
    msgDiv.innerText = message;

    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}


// Typing animation
function showTyping() {
    const chatBox = document.getElementById("chat-box");

    const typingDiv = document.createElement("div");
    typingDiv.className = "typing-message";
    typingDiv.id = "typing";
    typingDiv.innerText = "Typing...";

    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
}


// Browser voice output
function speakText(text) {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
}


// Send message
function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();

    if (message === "") return;

    appendMessage(message, "user");
    input.value = "";

    showTyping();

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        removeTyping();

        appendMessage(data.response, "bot");

        // Speak bot reply
        speakText(data.response);
    })
    .catch(error => {
        removeTyping();

        appendMessage("Error connecting to chatbot.", "bot");
        console.error(error);
    });
}


// Voice input
function startVoice() {
    if (!("webkitSpeechRecognition" in window)) {
        alert("Speech recognition not supported in this browser.");
        return;
    }

    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";

    recognition.start();

    recognition.onresult = function(event) {
        const voiceText = event.results[0][0].transcript;
        document.getElementById("user-input").value = voiceText;
        sendMessage();
    };

    recognition.onerror = function(event) {
        console.error("Voice recognition error:", event.error);
    };
}


// Clear chat
function clearChat() {
    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML = `
        <div class="bot-message">
            Hello! 👋 I am your AI college assistant. Ask me anything.
        </div>
    `;
}


// Enter key support
document.getElementById("user-input").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});
