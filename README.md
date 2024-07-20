# AI Chess Game

This project is an interactive chess game where you can play against an AI opponent. The game features a web-based interface and a server-side AI that calculates the best moves using Alpha Beta Pruning and MinMax algorithms.

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
- Play as White against an AI opponent (black)
- AI uses minimax algorithm with alpha-beta pruning
- Real-time move validation
- Game state tracking (checkmate, stalemate, etc.)

## Requirements (check requirements.txt)

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
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1. Start the FastAPI server:
    ```bash
    uvicorn app:app --reload
    ```

2. Open `templates/index.html` in your web browser.

Start playing! You'll be playing as White, and the AI will respond as Black.

## How It Works

### Frontend

The frontend is built using HTML, CSS, and JavaScript. It uses the chess.js library for game logic and move validation. The chessboard is rendered using HTML and CSS, with piece images loaded from lichess.org.

### Backend

The backend is a FastAPI server that handles AI move calculation. It uses the Python chess library for game state management and the minimax algorithm with alpha-beta pruning for move selection.

### AI Logic

The AI uses the minimax algorithm with alpha-beta pruning to search through possible moves and select the best one. 

## Project Structure

Chess Agent/
│
├── static/                     # Static files (CSS, JS)
│   ├── css/
│   │   └── styles.css          # CSS styles
│   └── js/
│       └── chess-game.js       # Script for rendering frontend and making API calls
│
├── templates/                  # HTML templates
│   └── index.html              # Main HTML file
│
├── utils/                      # Utility modules
│   └── board_services.py       # Chess logic and AI services
│
├── .gitignore                  # Git ignore file
├── app.py                      # FastAPI server
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies






## Code Overview

- `app.py`: Contains the FastAPI server setup and endpoint for AI move calculation.
- `board_services.py`: Implements the game logic and AI using the Python chess library and has the minmax algorithm.
- `templates/index.html`: The main HTML file for the web interface.
- `static/`: Contains static files for the CSS, JS.

## Troubleshooting

Check the console for error messages.

