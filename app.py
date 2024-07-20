from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from chess import Board
import uvicorn
from utils.board_services import best_move
from fastapi.middleware.cors import CORSMiddleware
import logging
import chess

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



app.mount("/static", StaticFiles(directory="static"), name="static")

class Move(BaseModel):
    san: str

class BoardState(BaseModel):
    fen: str





@app.post("/move/")
async def make_move(move: Move, board_state: BoardState):
    board = chess.Board(board_state.fen)
    board.push_san(move.san)
    return {"fen": board.fen()}


@app.post("/best-move")
async def get_best_move(board_state: BoardState):
    try:
        board = chess.Board(board_state.fen)
        logger.debug(f"Received FEN: {board_state.fen}")
        logger.debug(f"Current turn: {'Black' if board.turn == chess.BLACK else 'White'}")
        
        move = best_move(board, depth=3)  # You can adjust the depth as needed
        
        if move:
            logger.debug(f"AI move: {move.uci()}")
            return {"move": move.uci()}
        else:
            logger.error("No valid move found")
            raise HTTPException(status_code=400, detail="No valid move found")
    except Exception as e:
        logger.error(f"Error in ai_move: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/best-move/")
# async def get_best_move(board_state: BoardState, depth: int = 3):
#     board = chess.Board(board_state.fen)
#     move = best_move(board, depth)
#     if move is not None:
#         board.push(move)
#         return {"move": board.san(move), "fen": board.fen()}
#     return {"move": None, "fen": board.fen()}

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Chess API!"}


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())