# TailServe - AI Chat Application with Advanced Conversation Understanding

A next-generation AI chat application built with FastAPI that revolutionizes human-AI interaction through intelligent conversation understanding. Features advanced intent clarification, adaptive style matching, and enhanced context retention for truly personalized AI conversations.

## 🆕 Latest Update: Advanced Conversation Understanding Protocol

**Just launched!** A groundbreaking conversation understanding system that makes AI interactions more natural, contextual, and personalized than ever before.

## ✨ Revolutionary Features

### 🧠 Advanced Conversation Understanding Protocol
- **🎯 Intent Clarification Engine**: Automatically detects ambiguous requests and asks for clarification
- **📊 Real-time Clarity Analysis**: Every message gets a clarity score (0.0-1.0) with smart suggestions
- **🔄 Interactive Clarification Flow**: Seamless UI prompts when messages need clarification
- **💡 Context-Aware Analysis**: Uses conversation history to resolve pronouns and references

### 🎭 Adaptive Communication Style Matching  
- **📈 Dynamic Style Learning**: Analyzes formality, enthusiasm, technical depth, and brevity preferences
- **🎨 Personalized Response Adaptation**: AI responses automatically match your communication style
- **📝 Continuous Profile Building**: User preferences improve with every interaction
- **🔧 Multi-dimensional Analysis**: Tracks 4+ style dimensions for nuanced adaptation

### � Enhanced Context Management
- **🏷️ Smart Entity Tracking**: Automatically extracts and remembers important entities (names, files, concepts)
- **⭐ Importance-Based Context**: Messages ranked by relevance, not just recency
- **🎪 Conversation Stage Awareness**: Tracks opening, developing, clarifying, and concluding phases
- **🎯 Intelligent Context Selection**: Most relevant history selected for each response

### 🚀 Core Chat Features
- **⚡ Real-time Streaming**: Get AI responses as they're generated
- **💬 Multiple Chat Sessions**: Create and manage unlimited conversations
- **🖼️ Vision Capabilities**: Upload and analyze images with AI
- **🔧 Integrated Tools**: Built-in web search and file operations
- **📱 Responsive Design**: Perfect on desktop, tablet, and mobile

## Screenshots

The application features a modern, dark-themed interface with:
- Sidebar for chat management
- Tabbed interface (Chat, Tools, History)
- Real-time message streaming
- Image upload capabilities
- Tool integration panel

## 🏗️ Technical Implementation

### Conversation Understanding Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Intent         │    │  Context         │    │  Style          │
│  Analyzer       │    │  Manager         │    │  Adapter        │
│                 │    │                  │    │                 │
│ • Clarity Score │    │ • Entity Track   │    │ • Style Analysis│
│ • Ambiguity Det │    │ • Importance     │    │ • Response Adapt│
│ • Clarification │    │ • Stage Tracking │    │ • Profile Learn │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │   Enhanced Chat         │
                    │   Endpoint              │
                    │                         │
                    │ • Integrated Analysis   │
                    │ • Smart Context Select  │
                    │ • Adaptive Responses    │
                    └─────────────────────────┘
```

### Core Modules

| Module | Purpose | Key Features |
|--------|---------|--------------|
| `intent_analyzer.py` | Message clarity analysis | Ambiguity detection, clarification generation, context resolution |
| `context_manager.py` | Conversation state management | Entity extraction, importance scoring, stage tracking |
| `style_adapter.py` | Communication style adaptation | Style analysis, response adaptation, profile learning |
| `conversation_models.py` | Enhanced data models | ConversationState, UserProfile, IntentClarity, EnhancedMessage |

## Prerequisites

- Python 3.8+
- OpenAI API key OR Llama API key
- Modern web browser with JavaScript enabled

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd tailserve
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root or set environment variables:
   ```env
   # Option 1: OpenAI API (recommended for compatibility)
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Option 2: Llama API
   LLAMA_API_KEY=your_llama_api_key_here
   LLAMA_BASE_URL=https://api.llama-api.com/v1
   
   # Optional: Custom API endpoint
   LLAMA_BASE_URL=your_custom_endpoint_here
   ```

5. **Run the application**
   ```bash
   python main.py
   # Or using uvicorn directly
   uvicorn main:app --host 0.0.0.0 --port 3001
   ```

6. **Open your browser**
   Navigate to `http://localhost:3001`

> **🚀 Quick Start**: The application runs in development mode without an API key, showcasing all conversation understanding features with mock responses!

## 🎬 Quick Demo

### Intent Clarification in Action
```
👤 User: "Can you help me with this?"
🤖 AI: "I want to make sure I understand correctly. What specifically would you like help with?"

👤 User: "Fix the code"  
🤖 AI: "Could you specify what exactly you're referring to?"

👤 User: "Create a Python function that calculates the factorial of a number"
🤖 AI: "I'll create a factorial function for you..." ✨ (proceeds immediately - no clarification needed)
```

### Style Adaptation Examples
```
🔹 Formal User: "Could you please assist me with creating a database schema?"
🤖 AI: "I would be pleased to help you design a database schema. Please provide the requirements..."

🔹 Casual User: "yo can u help me make a db?"  
🤖 AI: "Sure! I can help you create a database. What kind of data are you working with?"
```

## Conversation Understanding Features

### Intent Clarification System
The system automatically analyzes each message for clarity and intent:

- **Ambiguity Detection**: Identifies vague references, incomplete requests, and uncertain language
- **Clarity Scoring**: Each message receives a clarity score from 0.0 (very ambiguous) to 1.0 (crystal clear)
- **Interactive Clarification**: When clarity score < 0.6, users get clarification prompts
- **Context Awareness**: Uses conversation history to resolve pronouns and references

**Example:**
```
User: "Can you help me with this?"
System: "I want to make sure I understand correctly. What specifically would you like help with?"
```

### Enhanced Context Retention
Smart conversation management that remembers what matters:

- **Entity Tracking**: Automatically extracts and tracks important entities (names, files, concepts)
- **Importance Scoring**: Messages are scored based on relevance and clarity
- **Conversation Stages**: Tracks whether conversation is opening, developing, clarifying, or concluding
- **Smart Context Selection**: Most relevant messages are selected for context, not just recent ones

### Adaptive Style Matching
The system learns and adapts to your communication style:

- **Style Analysis**: Detects formality level, enthusiasm, technical depth, and preferred brevity
- **Response Adaptation**: Adjusts responses to match your communication patterns
- **Learning Over Time**: User profiles improve with each interaction
- **Personalized Experience**: Same question, different style based on who's asking

**Style Indicators:**
- **Formality**: "Could you please..." vs "can u..."
- **Enthusiasm**: Use of exclamation marks and positive language
- **Technical Depth**: Technical terminology and code references
- **Brevity**: Preference for short vs detailed responses

## API Endpoints

### Core Endpoints
- `POST /chat` - Enhanced chat with conversation understanding
- `POST /clarify` - Check message clarity and get suggestions
- `GET /list_chats` - List all chat sessions
- `GET /get_chat?chat={name}` - Get chat history
- `POST /create_chat` - Create new chat session
- `POST /upload_image` - Upload images for vision capabilities

### Enhanced Chat Flow
1. **Message Analysis**: Intent clarity is automatically analyzed
2. **Clarification Check**: Ambiguous messages trigger clarification prompts  
3. **Context Update**: Conversation state and user profile are updated
4. **Enhanced Response**: LLM receives enriched context and style information
5. **Style Adaptation**: Response is adapted to match user's communication style

## Project Structure

```
tailserve/
├── main.py                          # FastAPI application entry point
├── endpoints.py                     # Enhanced API route handlers with conversation understanding
├── models.py                        # Core Pydantic data models
├── conversation_models.py           # NEW: Conversation understanding models
├── intent_analyzer.py               # NEW: Intent clarity analysis engine
├── context_manager.py               # NEW: Context and conversation state management
├── style_adapter.py                 # NEW: Communication style adaptation
├── utils.py            # Utility functions and API client
├── tools.py            # Tool implementations (search, file ops)
├── requirements.txt    # Python dependencies
├── package.json        # Project metadata
├── chats/             # Chat storage directory (auto-created)
├── static/            # Frontend assets
│   ├── index.html     # Main HTML page
│   ├── app.js         # Frontend JavaScript
│   ├── style.css      # Styling
│   └── profiles.js    # Model configuration profiles
└── tests/             # Test files
    ├── test_main.py
    └── test_tools.py
```

## API Endpoints

### Chat Management
- `GET /list_chats` - List all available chats
- `POST /create_chat` - Create a new chat session
- `GET /get_chat?chat={name}` - Retrieve chat history

### Chat Interaction
- `POST /chat` - Send message and get streaming response
- `POST /upload_image` - Upload image for chat

### Frontend
- `GET /` - Serve the main chat interface
- `GET /static/*` - Serve static assets

## Configuration

### Model Profiles

The application includes several pre-configured model profiles in `static/profiles.js`:

- **Ultra Fast**: Low temperature, 256 tokens, optimized for speed
- **Balanced**: Default settings for general conversation
- **Creative Genius**: High temperature, 1024 tokens for creative tasks
- **Ultra Long Context**: Lower temperature, 2048 tokens for detailed responses

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `LLAMA_API_KEY` | Your Llama API key | Yes |

## Usage

### Basic Chat
1. Open the application in your browser
2. Create a new chat or select an existing one
3. Type your message and press Enter
4. Watch as the AI response streams in real-time

### Image Upload
1. Click the camera icon (📷) in the chat input
2. Select an image file
3. The icon will change to 🖼️ indicating an image is loaded
4. Send your message - the image will be included

### Tools
The application supports several built-in tools:

- **Web Search (`ddgs`)**: Search the web using DuckDuckGo
- **File Operations (`save_file`)**: Save content to files

To use tools programmatically, include them in your chat request.

## Development

### Running Tests
```bash
python -m pytest test_main.py
python -m pytest test_tools.py
```

### Code Structure

- **Frontend**: Vanilla JavaScript with modern ES6+ features
- **Backend**: FastAPI with async/await patterns
- **Styling**: Custom CSS with dark theme and responsive design
- **State Management**: Simple client-side state management

### Adding New Tools

1. Implement your tool function in `tools.py`
2. Add the tool handler in `utils.py` `run_tool()` function
3. Update the frontend tool selector if needed

Example tool implementation:
```python
def my_custom_tool(input_data: str) -> str:
    # Your tool logic here
    return "Tool result"
```

## Troubleshooting

### Common Issues

1. **404 Errors on API calls**
   - Ensure the server is running on the correct port
   - Check that all endpoints are properly defined

2. **API Key Issues**
   - Verify your `LLAMA_API_KEY` is set correctly
   - Check that the API key is valid and has sufficient credits

3. **Frontend Errors**
   - Clear browser cache and reload
   - Check browser console for JavaScript errors
   - Ensure all static files are being served correctly

4. **Chat Not Loading**
   - Check that the `chats/` directory exists and is writable
   - Verify chat files are valid JSON

### Logs and Debugging

- Server logs are printed to the console when running
- Browser developer tools show frontend errors
- Check network tab for failed API requests

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Llama API](https://www.llama-api.com/)
- Search functionality via [DuckDuckGo Search](https://github.com/deedy5/duckduckgo_search)
- Modern UI inspired by popular chat applications

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the existing issues in the repository
3. Create a new issue with detailed information about your problem

---

**Happy chatting with AI! 🦙✨**
