# Import BaseModel from Pydantic for data validation
from pydantic import BaseModel

# Import the chess library
import chess

# Import logging for debugging
import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define a Pydantic model to handle the board state input, using FEN notation
class BoardState(BaseModel):
    fen: str  # FEN string representing the board's position

# Function to assign a value to each chess piece
def piece_value(piece):
    """
    Returns the value of a chess piece based on its type.
    
    Args:
        piece (chess.Piece): The chess piece whose value is to be determined.
    
    Returns:
        int: The value of the piece. Pawns are worth 1, Knights and Bishops are worth 3,
              Rooks are worth 5, Queens are worth 9, and Kings are worth 0.
    """
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
    """
    Determines the best move for the AI (black) using the minimax algorithm with alpha-beta pruning.
    
    Args:
        board (chess.Board): The current state of the chess board.
        depth (int): The depth of the search tree to explore.
    
    Returns:
        chess.Move or None: The best move found for the AI. If no valid move is found, a random legal move is returned.
    """
    # Check if it's black's turn
    if board.turn != chess.BLACK:
        logger.debug("It's not black's turn")
        return None  # Return None if it's not the AI's turn

    best_move = None  # Stores the best move found
    best_value = float('-inf')  # Tracks the highest evaluation value of all moves
    alpha = float('-inf')  # The best value that the maximizing player can guarantee
    beta = float('inf')  # The best value that the minimizing player can guarantee

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
    """
    Minimax algorithm with alpha-beta pruning to evaluate board positions and determine the best move.
    
    Args:
        board (chess.Board): The current state of the chess board.
        depth (int): The depth of the search tree to explore.
        alpha (float): The best value that the maximizing player can guarantee.
        beta (float): The best value that the minimizing player can guarantee.
        maximizing_player (bool): True if the current player is the maximizing player (black), False if minimizing (white).
    
    Returns:
        float: The best evaluation score for the current position.
    """
    # Check if the depth is 0 or the game is over
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)  # Evaluate the board

    if maximizing_player:  # If it's the maximizing player's turn (Black's turn)
        max_eval = float('-inf')  # Tracks the maximum evaluation score for the maximizing player
        for move in board.legal_moves:
            board.push(move)  # Simulates the legal move
            eval = minimax(board, depth - 1, alpha, beta, False)  # Recursively evaluate the board
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:  # If it's the minimizing player's turn (White's turn)
        min_eval = float('inf')  # Tracks the minimum evaluation score for the minimizing player
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
    """
    Evaluates the board position and returns a score based on various factors.
    
    Args:
        board (chess.Board): The current state of the chess board.
    
    Returns:
        int: The evaluation score of the board position. Positive values indicate an advantage for black, 
              negative values indicate an advantage for white. Special cases include checkmate and stalemate.
    """
    # Check if the game is in a checkmate state
    if board.is_checkmate():
        return 9999 if board.turn == chess.WHITE else -9999

    # Check for stalemate, insufficient material, 75 moves rule, or fivefold repetition
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0

    eval = 0  # Accumulates the evaluation score of the board position
    # Loop through all squares on the board
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = piece_value(piece)
            if piece.color == chess.BLACK:
                eval += value  # Add value for black pieces
            else:
                eval -= value  # Subtract value for white pieces
    return eval
