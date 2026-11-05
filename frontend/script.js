const API = "http://127.0.0.1:8000";

let accessToken = "";
let history = [];
let sessionID = "";

// Elements
const authSection = document.getElementById("auth-section");
const appSection = document.getElementById("app-section");

const authEmail = document.getElementById("auth-email");
const authPassword = document.getElementById("auth-password");
const authStatus = document.getElementById("auth-status");

const fileInput = document.getElementById("pdf-file");
const uploadBtn = document.getElementById("upload-btn");
const uploadStatus = document.getElementById("upload-status");

const questionInput = document.getElementById("question");
const sendBtn = document.getElementById("send-btn");
const chatBox = document.getElementById("chat-box");
const resetBtn = document.getElementById("reset-btn");

const documentsList = document.getElementById("documents-list");


// Register
document.getElementById("register-btn").addEventListener("click", async () => {

    try {

        const response = await fetch(`${API}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: authEmail.value.trim(),
                password: authPassword.value
            })
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.detail);

        authStatus.textContent = "Registration successful. Please login.";

    } catch (error) {
        authStatus.textContent = error.message;
    }

});


// Login
document.getElementById("login-btn").addEventListener("click", async () => {

    try {

        const response = await fetch(`${API}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: authEmail.value.trim(),
                password: authPassword.value
            })
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.detail);

        accessToken = data.access_token;

        authSection.hidden = true;
        appSection.hidden = false;

        document.getElementById("user-email").textContent =
            authEmail.value.trim();

        authPassword.value = "";

        await loadDocuments();

    } catch (error) {
        authStatus.textContent = error.message;
    }

});


// Upload PDF
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

        const response = await fetch(`${API}/upload/`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${accessToken}`
            },
            body: formData
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.detail);

        sessionID = data.session_id;
        history = [];

        uploadStatus.textContent = "Document uploaded successfully!";
        fileInput.value = "";

        await loadDocuments();

    } catch (error) {
        uploadStatus.textContent = error.message;
    }

    uploadBtn.disabled = false;

});


// Load documents
async function loadDocuments() {

    try {

        const response = await fetch(`${API}/documents`, {
            headers: {
                "Authorization": `Bearer ${accessToken}`
            }
        });

        const documents = await response.json();

        if (!response.ok) throw new Error(documents.detail);

        documentsList.replaceChildren();

        if (documents.length === 0) {
            documentsList.textContent = "No documents uploaded.";
            return;
        }

        documents.forEach(doc => {

            const item = document.createElement("div");
            const name = document.createElement("span");
            name.textContent = doc.filename;

            const openBtn = document.createElement("button");
            openBtn.textContent = "Open";

            openBtn.onclick = () => {
                sessionID = doc.session_id;
                history = [];
                chatBox.textContent = "Document selected. Ask a question!";
            };

            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";

            deleteBtn.onclick = async () => {

                if (!confirm("Delete this document?")) return;

                try {

                    const result = await fetch(
                        `${API}/documents/${doc.session_id}`,
                        {
                            method: "DELETE",
                            headers: {
                                "Authorization": `Bearer ${accessToken}`
                            }
                        }
                    );

                    const data = await result.json();

                    if (!result.ok) throw new Error(data.detail);

                    if (sessionID === doc.session_id) {
                        sessionID = "";
                        history = [];
                    }

                    await loadDocuments();

                    uploadStatus.textContent = data.message;

                } catch (error) {
                    uploadStatus.textContent = error.message;
                }

            };

            item.append(name, openBtn, deleteBtn);
            documentsList.appendChild(item);

        });

    } catch (error) {
        documentsList.textContent = error.message;
    }

}


// Chat
async function sendMessage() {

    const question = questionInput.value.trim();

    if (!question) return;

    if (!sessionID) {
        alert("Upload or select a document first.");
        return;
    }

    const userMessage = document.createElement("p");
    userMessage.textContent = "You: " + question;
    chatBox.appendChild(userMessage);

    questionInput.value = "";

    const aiMessage = document.createElement("p");
    aiMessage.textContent = "AI: Generating...";
    chatBox.appendChild(aiMessage);

    sendBtn.disabled = true;

    try {

        const response = await fetch(`${API}/chat/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                query: question,
                history: history,
                session_id: sessionID
            })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let answer = "";
        let firstChunk = true;

        while (true) {

            const { done, value } = await reader.read();

            if (done) break;

            answer += decoder.decode(value, { stream: true });

            if (firstChunk) {
                aiMessage.textContent = "AI: ";
                firstChunk = false;
            }

            aiMessage.textContent = "AI: " + answer;

            chatBox.scrollTop = chatBox.scrollHeight;

        }

        answer += decoder.decode();

        history.push({
            question: question,
            answer: answer
        });

    } catch (error) {

        aiMessage.textContent = "AI: " + error.message;

    }

    sendBtn.disabled = false;

}


// Send message
sendBtn.addEventListener("click", sendMessage);

questionInput.addEventListener("keypress", event => {
    if (event.key === "Enter") sendMessage();
});


// Reset conversation
resetBtn.addEventListener("click", async () => {

    if (!sessionID) {
        alert("Select a document first.");
        return;
    }

    try {

        const response = await fetch(
            `${API}/reset/?session_id=${encodeURIComponent(sessionID)}`,
            {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${accessToken}`
                }
            }
        );

        const data = await response.json();

        if (!response.ok) throw new Error(data.detail);

        history = [];

        chatBox.textContent = "Conversation cleared!";

        uploadStatus.textContent = data.message;

    } catch (error) {
        uploadStatus.textContent = error.message;
    }

});


// Logout
document.getElementById("logout-btn").addEventListener("click", () => {

    accessToken = "";
    sessionID = "";
    history = [];

    authSection.hidden = false;
    appSection.hidden = true;

    authEmail.value = "";
    authPassword.value = "";

    documentsList.replaceChildren();

    uploadStatus.textContent = "";
    authStatus.textContent = "Logged out successfully.";

    chatBox.textContent = "Upload a document to begin.";

});
