let history = [];

let sessionID = "";

const fileInput = document.getElementById("pdf-file");
const uploadBtn = document.getElementById("upload-btn");

const questionInput = document.getElementById("question");
const sendBtn = document.getElementById("send-btn");

const chatBox = document.getElementById("chat-box");

const resetBtn = document.getElementById("reset-btn");

const uploadStatus = document.getElementById("upload-status");


uploadBtn.addEventListener("click", async () => {

    const file = fileInput.files[0];

    if (!file) {
        alert("Please choose a PDF first.");
        return;
    }

    uploadBtn.disabled = true;

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch(
            "https://harman1010-rag-backend.hf.space/upload",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if(!response.ok) {
            throw new Error(data.detail || "Upload Failed!")
        }

        sessionID = data.session_id;

        history = [];

        uploadStatus.textContent =
            "Document uploaded successfully!";

        fileInput.value = "";

    }

    catch (error) {

        uploadStatus.textContent = error.message;

    }

    uploadBtn.disabled = false;

});


async function sendMessage() {

    const question = questionInput.value.trim();

    if (question === "") {
        return;
    }

    if (chatBox.querySelector(".bot-message")) {
        chatBox.innerHTML = "";
    }

    const userMessage = document.createElement("p");
    userMessage.innerHTML = `<strong>You:</strong> ${question}`;
    chatBox.appendChild(userMessage);

    questionInput.value = "";

    const aiMessage = document.createElement("p");

    const aiLabel = document.createElement("strong");
    aiLabel.textContent = "AI: ";

    const aiText = document.createElement("span");

    aiMessage.appendChild(aiLabel);
    aiMessage.appendChild(aiText);

    chatBox.appendChild(aiMessage);

    chatBox.scrollTop = chatBox.scrollHeight;

    let firstChunk = false;

    const generatingTimer = setTimeout(() => {

        if (!firstChunk) {

            aiText.textContent = "Generating...";

        }

    }, 500);

    try {

        const response = await fetch(
            "https://harman1010-rag-backend.hf.space/chat/",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    query: question,
                    history: history,
                    session_id: sessionID
                })

            }
        );

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Chat request failed");
        }

        const reader = response.body.getReader();

        const decoder = new TextDecoder();

        let responseText = "";

        while (true) {

            const { done, value } = await reader.read();

            if (done) {
                break;
            }

            const chunk = decoder.decode(value);

            if (!firstChunk) {

                firstChunk = true;

                clearTimeout(generatingTimer);

                aiText.textContent = "";

            }

            responseText += chunk;
            aiText.innerHTML = marked.parse(responseText);

            chatBox.scrollTop = chatBox.scrollHeight;

        }

        clearTimeout(generatingTimer);

        history.push({ question: question, answer: responseText });

    }

    catch (error) {

        clearTimeout(generatingTimer);

        aiText.textContent = error.message || "Something went wrong";

    }

}


sendBtn.addEventListener(
    "click",
    sendMessage
);


questionInput.addEventListener(
    "keypress",
    function (event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);


resetBtn.addEventListener("click", () => {

    chatBox.innerHTML =
        `<p class="bot-message">
            👋 Conversation cleared! You can continue asking about your uploaded PDF.
        </p>`;

    uploadStatus.textContent = "";

    history = [];


});