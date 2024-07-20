let board = null;
let game = new Chess();

function renderBoard() {
    const boardElement = document.getElementById('board');
    boardElement.innerHTML = '';
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const square = document.createElement('div');
            square.className = `square ${(i + j) % 2 === 0 ? 'white' : 'black'}`;
            square.dataset.square = String.fromCharCode(97 + j) + (8 - i);
            square.onclick = onSquareClick;
            
            const piece = game.get(square.dataset.square);
            if (piece) {
                const pieceElement = document.createElement('div');
                pieceElement.className = 'piece';
                pieceElement.style.backgroundImage = `url(https://lichess1.org/assets/_PllZgR/piece/cburnett/${piece.color}${piece.type.toUpperCase()}.svg)`;
                square.appendChild(pieceElement);
            }
            
            boardElement.appendChild(square);
        }
    }
    updateGameStatus();
}

function updateGameStatus() {
    const statusElement = document.getElementById('status');
    let status = '';

    if (game.in_checkmate()) {
        status = `Checkmate! ${game.turn() === 'w' ? 'Black' : 'White'} wins.`;
    } else if (game.in_stalemate()) {
        status = 'Game over. Stalemate!';
    } else if (game.in_threefold_repetition()) {
        status = 'Game over. Draw by threefold repetition.';
    } else if (game.insufficient_material()) {
        status = 'Game over. Draw due to insufficient material.';
    } else if (game.in_draw()) {
        status = 'Game over. Draw.';
    } else if (game.in_check()) {
        status = `${game.turn() === 'w' ? 'White' : 'Black'} is in check.`;
    } else {
        status = `Current turn: ${game.turn() === 'w' ? 'White' : 'Black'}`;
    }

    statusElement.innerText = status;
}

let selectedSquare = null;

async function makeAIMove() {
    console.log("Current FEN:", game.fen());
    console.log("Legal moves:", game.moves({ verbose: true }));

    try {
        const response = await fetch('http://localhost:8000/best-move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fen: game.fen() })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        if (data.move) {
            console.log("Received AI move:", data.move);
            
            // Check if the move is legal
            const legalMoves = game.moves({ verbose: true });
            const isLegal = legalMoves.some(m => m.from + m.to === data.move);
            
            if (isLegal) {
                // Try applying the move in two different ways
                let move = game.move(data.move);
                if (!move) {
                    console.log("Trying to apply move as an object");
                    move = game.move({
                        from: data.move.substring(0, 2),
                        to: data.move.substring(2, 4),
                        promotion: 'q' // default to queen promotion if needed
                    });
                }
                
                if (move) {
                    console.log("AI move applied successfully:", move);
                    renderBoard();
                    updateGameStatus();
                } else {
                    console.error('Failed to apply AI move:', data.move);
                    console.log("Current board state:", game.board());
                    console.log("Is it black's turn?", game.turn() === 'b');
                }
            } else {
                console.error('Received illegal move from AI:', data.move);
                console.log("Legal moves:", legalMoves.map(m => m.from + m.to));
            }
        } else {
            console.log('No valid moves available for AI');
            updateGameStatus();
        }
    } catch (error) {
        console.error('Error making AI move:', error);
    }
}




function onSquareClick(event) {
    // Only allow clicks when it's white's turn
    if (game.turn() !== 'w') return;

    const square = event.target.closest('.square');
    if (!square) return;

    const piece = game.get(square.dataset.square);

    if (!selectedSquare && (!piece || piece.color !== 'w')) {
        return;
    }

    document.querySelectorAll('.square').forEach(sq => sq.classList.remove('selected'));

    if (selectedSquare) {
        const move = game.move({
            from: selectedSquare,
            to: square.dataset.square,
            promotion: 'q'
        });
        
        if (move) {
            renderBoard();
            updateGameStatus();
            if (!game.game_over()) {
                setTimeout(makeAIMove, 300);
            }
        } else {
            square.classList.add('selected');
            selectedSquare = square.dataset.square;
        }
        
        selectedSquare = null;
    } else {
        square.classList.add('selected');
        selectedSquare = square.dataset.square;
    }
}

function newGame() {
    game.reset();
    renderBoard();
}

renderBoard();

window.onload = newGame;