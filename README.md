# Chat APP

Chat APP is a lightweight, server-based chat system built with **FastAPI**, **HTMX**, and local data persistence. It includes the following features:
- **Real-time communication** using WebSockets.
- **User authentication**.
- **Message handling**.
- Simple and efficient **local persistence** for chat history.

## Features
- **Socket Communication**: Enables real-time sending and receiving of messages.
- **FastAPI Backend**: A modern, fast (high-performance), and simple-to-use web framework.
- **HTMX Support**: For seamless front-end interactions without requiring a heavy JavaScript framework.
- **Local Storage**: Chat history is stored in a JSON file locally.

## Prerequisites
- **Python 3.8+** installed on your local machine.
- Virtual environment (recommended).
- Dependencies installed from `requirements.txt`.


### Command Run 
```bash
uvicorn main:app --reload
```
