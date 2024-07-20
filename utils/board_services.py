# Import necessary modules from FastAPI
from fastapi import FastAPI, HTTPException

# Import BaseModel from Pydantic for data validation
from pydantic import BaseModel

# Import the chess library
import chess
from chess import Board

# Import uvicorn for running the FastAPI application
import uvicorn

# Import logging for debugging
import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the FastAPI application
app = FastAPI()

# Define a Pydantic model to handle the board state input, using FEN notation
class BoardState(BaseModel):
    fen: str

# Function to assign a value to each chess piece
def piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT:
        return 3
    elif piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    elif piece.piece_type == chess.KING:
        return 0
    return 0

# Function to determine the best move for the AI (black)
def best_move(board, depth):
    # Check if it's black's turn
    if board.turn != chess.BLACK:
        logger.debug("It's not black's turn")
        return None  # Return None if it's not the AI's turn

    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    # Log the legal moves
    logger.debug(f"Legal moves: {list(board.legal_moves)}")

    # Evaluate each legal move
    for move in board.legal_moves:
        board.push(move)  # Make the move
        eval = minimax(board, depth - 1, alpha, beta, False)  # Evaluate the board
        board.pop()  # Undo the move
        logger.debug(f"Move: {move}, Evaluation: {eval}")
        if eval > best_value:
            best_value = eval
            best_move = move
        alpha = max(alpha, eval)

    # Check if a valid best move was found
    if best_move and best_move in board.legal_moves:
        logger.debug(f"Best move found: {best_move}")
        return best_move
    else:
        # If no valid best move was found, select a random legal move
        logger.debug("No valid best move found, selecting random legal move")
        random_move = next(iter(board.legal_moves), None)
        logger.debug(f"Random move selected: {random_move}")
        return random_move

# Minimax algorithm with alpha-beta pruning for evaluating board positions
def minimax(board, depth, alpha, beta, maximizing_player):
    # Check if the depth is 0 or the game is over
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)  # Evaluate the board

    if maximizing_player:  # If it's the maximizing player's turn (Black's turn)
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:  # If it's the minimizing player's turn (White's turn)
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval

# Function to evaluate the board
def evaluate_board(board):
    # Check if the game is in a checkmate state
    if board.is_checkmate():
        return 9999 if board.turn == chess.WHITE else -9999

    # Check for stalemate, insufficient material, 75 moves rule, or fivefold repetition
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0

    eval = 0
    # Loop through all squares on the board
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = piece_value(piece)
            if piece.color == chess.BLACK:
                eval += value
            else:
                eval -= value
    return eval
