import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
from pathlib import Path

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Conversation history
conversation_history = []

# System prompt for the AI assistant
SYSTEM_PROMPT = """
You are a helpful terminal assistant with full access to the user's computer.
You can:
- Remember conversation history
- Create/edit/delete files (when user approves)
- Execute system commands (when user approves)
Always:
- Prefix commands with CMD:
- Ask for confirmation before file modifications
- Never suggest harmful commands
"""

def get_ai_response(prompt):
    try:
        # Build context with history
        context = SYSTEM_PROMPT
        if conversation_history:
            context += "\n\nPrevious conversation:"
            for msg in conversation_history[-5:]:  # Keep last 5 messages
                context += f"\n{msg['role']}: {msg['content']}"
        
        context += f"\n\nUser: {prompt}\nAssistant:"
        
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

def execute_command(command):
    try:
        if command.startswith('file '):
            return handle_file_operation(command[5:])
        output = os.popen(command).read()
        return output if output else "Command executed successfully"
    except Exception as e:
        return f"Error: {str(e)}"

def handle_file_operation(operation):
    try:
        parts = operation.split()
        if len(parts) < 2:
            return "Invalid file operation format"
            
        action = parts[0].lower()
        path = ' '.join(parts[1:])
        
        if action == 'read':
            with open(path, 'r') as f:
                return f.read()
        elif action == 'write':
            content = input(f"Enter content for {path}: ")
            with open(path, 'w') as f:
                f.write(content)
            return f"File {path} updated"
        elif action == 'delete':
            os.remove(path)
            return f"File {path} deleted"
        elif action == 'create':
            Path(path).touch()
            return f"File {path} created"
        else:
            return "Invalid file operation"
    except Exception as e:
        return f"File Error: {str(e)}"

if __name__ == "__main__":
    print("Terminal AI Assistant - Ready (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        # Add user message to history
        conversation_history.append({"role": "User", "content": user_input})
        
        response = get_ai_response(user_input)
        
        # Add AI response to history
        conversation_history.append({"role": "AI", "content": response})
        
        if response.startswith("CMD:"):
            command = response[4:].strip()
            print(f"Executing: {command}")
            result = execute_command(command)
            print(f"Result: {result}")
        else:
            print(f"AI: {response}")
