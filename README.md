# AI Chess Game

This project is an interactive chess game where you can play against an AI opponent. The game features a web-based interface and a server-side AI that calculates the best moves.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [How to Run](#how-to-run)
5. [How It Works](#how-it-works)
6. [Project Structure](#project-structure)
7. [Code Overview](#code-overview)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)

## Features

- Web-based chess board interface
- Play as White against an AI opponent
- AI uses minimax algorithm with alpha-beta pruning
- Real-time move validation
- Game state tracking (checkmate, stalemate, etc.)

## Requirements

- Python 3.7+
- FastAPI
- chess (Python chess library)
- uvicorn (ASGI server)
- A modern web browser

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-chess-game.git
cd ai-chess-game
Install the required Python packages:
bash
Copy code
pip install -r requirements.txt
How to Run
Start the FastAPI server:
bash
Copy code
uvicorn app:app --reload
Open templates/index.html in your web browser.

Start playing! You'll be playing as White, and the AI will respond as Black.

How It Works
Frontend
The frontend is built using HTML, CSS, and JavaScript. It uses the chess.js library for game logic and move validation. The chessboard is rendered using HTML and CSS, with piece images loaded from lichess.org.

Backend
The backend is a FastAPI server that handles AI move calculation. It uses the Python chess library for game state management and the minimax algorithm with alpha-beta pruning for move selection.

AI Logic
The AI uses the minimax algorithm with alpha-beta pruning to search through possible moves and select the best one. The evaluation function considers material balance and basic positional factors.

Project Structure
csharp
Copy code
Chess Agent/
│
├── __pycache__/       # Compiled Python files
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
│   └── index.html     # Main HTML file
├── utils/             # Utility modules
├── venv/              # Virtual environment
├── .gitignore         # Git ignore file
├── app.py             # FastAPI server and AI logic
├── chess_game.py      # Game logic
├── README.md          # This file
└── requirements.txt   # Python dependencies
Code Overview
app.py: Contains the FastAPI server setup and endpoint for AI move calculation.
chess_game.py: Implements the game logic and AI using the Python chess library.
templates/index.html: The main HTML file for the web interface.
static/: Contains static files like CSS, JS, and images.
