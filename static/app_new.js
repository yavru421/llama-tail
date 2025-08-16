// --- Mobile-first, feature-rich chat app logic ---
const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const imageInput = document.getElementById('image-input');
const imageBtn = document.getElementById('image-btn');
const chatList = document.getElementById('chat-list');
const newChatBtn = document.getElementById('new-chat-btn');
const toolSelect = document.getElementById('tool-select');
const toolInput = document.getElementById('tool-input');
const applyToolBtn = document.getElementById('apply-tool');

const errorPanel = document.getElementById('error-panel');
const reasoningTrace = document.getElementById('reasoning-trace');

let currentChat = null;
let imageBase64 = null;
let pendingClarification = null;
let clarificationMode = false;

// --- Utility Functions ---
function showError(msg) {
    if (!errorPanel) return;
    if (!msg) {
        errorPanel.style.display = 'none';
        errorPanel.textContent = '';
    } else {
        errorPanel.style.display = 'block';
        errorPanel.textContent = msg;
    }
}

function appendMessage(role, text) {
    const msg = document.createElement('div');
    msg.className = 'message ' + role;
    msg.textContent = text;
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// --- Clarification Support ---
async function checkForClarification(message) {
    try {
        const response = await fetch('/clarify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                chat: currentChat,
                history: [] // Add actual history if needed
            })
        });

        const data = await response.json();

        if (data.needs_clarification) {
            return {
                needsClarification: true,
                suggestions: data.suggested_clarifications,
                clarityScore: data.clarity_score
            };
        }

        return { needsClarification: false };
    } catch (error) {
        console.warn('Clarification check failed:', error);
        return { needsClarification: false };
    }
}

function showClarificationDialog(suggestions) {
    const dialog = document.createElement('div');
    dialog.className = 'clarification-dialog';
    dialog.innerHTML = `
        <div class="clarification-content">
            <h3>Let me clarify</h3>
            <p>Your request could be interpreted in multiple ways. Could you help me understand:</p>
            <ul>
                ${suggestions.map(s => `<li>${s}</li>`).join('')}
            </ul>
            <div class="clarification-buttons">
                <button id="clarify-proceed">Proceed anyway</button>
                <button id="clarify-modify">Let me rephrase</button>
            </div>
        </div>
    `;

    document.body.appendChild(dialog);

    document.getElementById('clarify-proceed').onclick = () => {
        document.body.removeChild(dialog);
        clarificationMode = false;
        // Proceed with original message
        sendMessageToChatEndpoint(pendingClarification.message);
    };

    document.getElementById('clarify-modify').onclick = () => {
        document.body.removeChild(dialog);
        clarificationMode = false;
        userInput.value = pendingClarification.message;
        userInput.focus();
    };
}

// --- Chat Management ---
async function refreshChats() {
    const res = await fetch('/list_chats');
    const data = await res.json();
    chatList.innerHTML = '';
    data.chats.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.textContent = c;
        chatList.appendChild(opt);
    });
}

async function loadChat(chatName) {
    if (!chatName) return;
    currentChat = chatName;
    chatWindow.innerHTML = '';
    try {
        const res = await fetch(`/get_chat?chat=${encodeURIComponent(chatName)}`);
        const data = await res.json();
        data.messages.forEach(msg => {
            appendMessage(msg.role, msg.content || '[Tool Result]');
        });
        showError('');
    } catch (err) {
        showError('Failed to load chat: ' + err.message);
    }
}

// --- Event Listeners ---
chatList.addEventListener('change', (e) => {
    loadChat(e.target.value);
});

newChatBtn.addEventListener('click', async () => {
    const name = prompt('Enter chat name:');
    if (!name) return;
    try {
        const formData = new FormData();
        formData.append('chat_name', name);
        const res = await fetch('/create_chat', {
            method: 'POST',
            body: formData
        });
        if (res.ok) {
            await refreshChats();
            chatList.value = name;
            loadChat(name);
        } else {
            throw new Error('Failed to create chat');
        }
        showError('');
    } catch (err) {
        showError('Failed to create chat: ' + err.message);
    }
});

imageInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    try {
        const res = await fetch('/upload_image', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        imageBase64 = data.base64;
        imageBtn.textContent = '✅';
        showError('');
    } catch (err) {
        showError('Image upload failed: ' + err.message);
    }
});

imageBtn.addEventListener('click', () => {
    imageInput.click();
});

applyToolBtn.addEventListener('click', async () => {
    const tool = toolSelect.value;
    const tool_input = toolInput.value;
    if (!tool || !currentChat) {
        showError('Please select a tool and chat first.');
        return;
    }
    const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            tool,
            tool_input,
            chat: currentChat
        })
    });
    let result = '';
    if (res.body) {
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let done = false;
        while (!done) {
            const { value, done: doneReading } = await reader.read();
            done = doneReading;
            if (value) {
                const chunk = decoder.decode(value);
                result += chunk;
                reasoningTrace.textContent = chunk;
            }
        }
    }
    appendMessage('assistant', result);
    reasoningTrace.textContent = '';
});

// --- Chat Send ---
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!currentChat) {
        showError('Please select or create a chat first.');
        return;
    }

    const message = userInput.value.trim();
    if (!message) return;

    // Check for clarification need (unless we're already in clarification mode)
    if (!clarificationMode) {
        const clarificationResult = await checkForClarification(message);

        if (clarificationResult.needsClarification) {
            pendingClarification = { message: message };
            clarificationMode = true;
            showClarificationDialog(clarificationResult.suggestions);
            return;
        }
    }

    // Proceed with normal message sending
    await sendMessageToChatEndpoint(message);
    userInput.value = '';
    clarificationMode = false;
});

// Extract message sending logic to separate function
async function sendMessageToChatEndpoint(message) {
    appendMessage('user', message);
    appendMessage('assistant', '...');
    const lastMsg = chatWindow.querySelector('.message.assistant:last-child');
    lastMsg.textContent = '';

    if (reasoningTrace) reasoningTrace.textContent = 'Thinking...';

    try {
        const requestBody = {
            message,
            chat: currentChat,
            history: [] // Add actual history if needed
        };

        if (imageBase64) {
            requestBody.image_base64 = imageBase64;
        }

        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });

        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }

        if (!res.body) throw new Error('No response body');

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let done = false;

        while (!done) {
            const { value, done: doneReading } = await reader.read();
            done = doneReading;
            if (value) {
                const chunk = decoder.decode(value);
                lastMsg.textContent += chunk;
                chatWindow.scrollTop = chatWindow.scrollHeight;
            }
        }

        if (reasoningTrace) reasoningTrace.textContent = '';
        imageBase64 = null;
        imageBtn.textContent = '📷';
        showError('');

    } catch (err) {
        lastMsg.textContent = '[Error: ' + err.message + ']';
        if (reasoningTrace) reasoningTrace.textContent = '';
        showError('Failed to send message: ' + err.message);
    }
}

// --- Initialize ---
refreshChats();
