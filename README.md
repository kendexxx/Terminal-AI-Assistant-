# Terminal AI Assistant

A text-based AI assistant powered by Google Gemini that can execute PC commands via terminal conversation.

## Features
- Text-based interaction with Gemini 1.5 Flash
- Safe command execution
- Context-aware conversations
- Error handling for commands and AI responses

## Setup
1. Install Python 3.10+ if not already installed
2. Clone this repository (or just download this all as a ZIP file)
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create a `.env` file(or edit the already exiting one) and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage
Locate the folder:
cd (installed location of the folder) 
  then
Run the assistant:
```bash
python main.py
```

### Example Interactions
```
You: list files in this directory
AI: CMD: dir
Executing: dir
Result: [list of files]

You: what's the weather today?
AI: I can't check the weather directly, but you could use:
CMD: curl wttr.in

You: tell me a joke
AI: Why don't programmers like nature? It has too many bugs!
```

## Command Safety
- The assistant will only suggest safe commands
- Commands are prefixed with "CMD:" before execution
- You can review commands before execution

## Troubleshooting
- `AI Error: ...` - The Gemini API may be unavailable
- `Error: ...` - A command failed to execute
- Make sure your API key is valid and has access to Gemini 1.5 Flash
