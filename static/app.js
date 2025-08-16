

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
    if (data.chats.length > 0) {
        currentChat = data.chats[0];
        chatList.value = currentChat;
        loadChatHistory();
    } else {
        // No chats exist, create a default one
        currentChat = null;
        showError('No chats found. Please create a new chat.');
    }
}
chatList.addEventListener('change', e => {
    currentChat = e.target.value;
    loadChatHistory();
});
newChatBtn.addEventListener('click', async () => {
    const chat_name = prompt('New chat name:');
    if (!chat_name) return;
    try {
        await fetch('/create_chat', { method: 'POST', body: new URLSearchParams({ chat_name }) });
        await refreshChats();
        showError('');
    } catch (err) {
        showError('Failed to create chat: ' + err.message);
    }
});


// --- Chat History ---
async function loadChatHistory() {
    chatWindow.innerHTML = '';
    if (!currentChat) return;
    const res = await fetch(`/get_chat?chat=${encodeURIComponent(currentChat)}`);
    if (!res.ok) {
        showError('Failed to load chat history.');
        return;
    }
    const data = await res.json();
    if (!data.messages) return;
    data.messages.forEach(msg => {
        appendMessage(msg.role || 'assistant', msg.content || msg.output || '');
    });
}

// --- Image Upload ---
imageBtn.addEventListener('click', () => imageInput.click());
imageInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch('/upload_image', { method: 'POST', body: formData });
    const data = await res.json();
    imageBase64 = data.base64;
    imageBtn.textContent = '🖼️';
});

// --- Tool Use ---
applyToolBtn.addEventListener('click', async () => {
    if (!currentChat) {
        showError('Select a chat.');
        return;
    }
    const tool = toolSelect.value;
    const tool_input = toolInput.value;
    appendMessage('tool', `[Tool:${tool}] ${tool_input}`);
    showError('');
    reasoningTrace.textContent = 'Running tool...';
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
    appendMessage('user', message);
    userInput.value = '';
    appendMessage('assistant', '...');
    const lastMsg = chatWindow.querySelector('.message.assistant:last-child');
    lastMsg.textContent = '';
    if (reasoningTrace) reasoningTrace.textContent = 'Thinking...';
    try {
        const requestBody = {
            message,
            chat: currentChat,
            history: [] // Add empty history for now
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
                lastMsg.textContent += decoder.decode(value);
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
});

// --- Initial load ---
refreshChats();
