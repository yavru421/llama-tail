# TailServe - AI Chat Application

A modern, responsive AI chat application built with FastAPI and the Llama API. Features real-time streaming responses, multiple chat sessions, image uploads, and tool integration.

## Features

- 🚀 **Real-time Streaming**: Get AI responses as they're generated
- 💬 **Multiple Chats**: Create and manage multiple chat sessions
- 🖼️ **Image Support**: Upload and send images to the AI
- 🔧 **Tool Integration**: Built-in web search and file operations
- 📱 **Responsive Design**: Works great on desktop and mobile
- 🎨 **Modern UI**: Clean, dark-themed interface with tabbed layout

## Screenshots

The application features a modern, dark-themed interface with:
- Sidebar for chat management
- Tabbed interface (Chat, Tools, History)
- Real-time message streaming
- Image upload capabilities
- Tool integration panel

## Prerequisites

- Python 3.8+
- Llama API key from [Llama API](https://www.llama-api.com/)

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
   Create a `.env` file in the project root:
   ```env
   LLAMA_API_KEY=your_llama_api_key_here
   ```

5. **Run the application**
   ```bash
   python main.py
   # Or using uvicorn directly
   uvicorn main:app --host 0.0.0.0 --port 3001
   ```

6. **Open your browser**
   Navigate to `http://localhost:3001`

## Project Structure

```
tailserve/
├── main.py              # FastAPI application entry point
├── endpoints.py         # API route handlers
├── models.py           # Pydantic data models
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
