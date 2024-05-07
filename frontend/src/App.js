import "./App.css";
import { useState, useEffect } from "react";
import { Checkers } from "./Game";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCrown } from "@fortawesome/free-solid-svg-icons";
import { io, socket } from "./socket";

const init = new Checkers();
//socket.connect();

function App() {
  const [active, setActive] = useState(null);

  const [game, setGame] = useState(init);

  const activePiece = (id) => {
    if (active && active.id === id) {
      setActive(null);
      return;
    }
    const moves = game.getValidUpdated(id);
    setActive({
      id,
      availableMoves: moves ? moves.validMoves : new Set(),
      moveInfo: moves ? moves.moveInfo : {},
    });
  };

  useEffect(() => {
    // Update the component whenever game state changes
    setGame(new Checkers(game.board, game.pieces)); // Assuming Checkers has a constructor that accepts board and pieces
  }, []);

  const handleSquareClick = (coord, id) => {
    if (active && active.availableMoves.has(coord)) {
      game.movePiece(id, active.id, active.moveInfo[coord]);
      setActive(null); // Reset active state after the move
    }
  };

  socket.on("game_status", (data) => {});

  return (
    <div className="App">
      <header className="App-header">
        <h2>Checkers</h2>
        <h6>({game.turn === 0 ? "Black" : "Red"} Turn)</h6>
        <div className="gameboard">
          {game.board.map((x) => {
            return (
              <div
                onMouseDown={() => {
                  handleSquareClick(x.coord, x.id);
                }}
                className={
                  "game-square " +
                  x.space_color +
                  (active?.availableMoves.has(x.coord) ? " move" : "")
                }
                key={x.id}
              >
                <span className="coord">{x.coord}</span>
                {x.piece ? (
                  <div
                    onMouseDown={(e) => {
                      if (game.pieceTurn(x.piece)) activePiece(x.piece);
                    }}
                    className={
                      "game-piece" +
                      (game.pieceTurn(x.piece) ? " movable" : "") +
                      (game.pieces[x.piece].isBlack ? " black" : "") +
                      (active?.id === x.piece ? " active" : "")
                    }
                  >
                    {game.pieces[x.piece].isKing ? (
                      <FontAwesomeIcon icon={faCrown} />
                    ) : (
                      ""
                    )}
                  </div>
                ) : (
                  ""
                )}
              </div>
            );
          })}
          <div className="moves-cont">
            <div className="move-header">Move History</div>
            <div className="move-list">
              {game.moveHistory.map((x) => {
                return (
                  <div className="move-item" key={x.move}>
                    <div>{x.move}</div>
                    <div>{x.captured} Pieces Captured</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
