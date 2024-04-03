import './App.css';
import { useState, useEffect} from "react";
import { Checkers } from './Game';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCrown } from '@fortawesome/free-solid-svg-icons'

const init = new Checkers();

function App() {
  const [active, setActive] = useState(null);

  const [game, setGame] = useState(init);

  const activePiece = (id) => {
    setActive({
      id,
      availableMoves: game.getValidMoves(id)
    })
  };

  useEffect(() => {
    // Update the component whenever game state changes
    setGame(new Checkers(game.board, game.pieces)); // Assuming Checkers has a constructor that accepts board and pieces
  }, []);

  const handleSquareClick = (coord, id) => {
    if (active && active.availableMoves.has(coord)) {
      game.movePiece(id, active.id);
      setActive(null); // Reset active state after the move
    }
  };


  return (
    <div className="App">
      <header className="App-header">
        <h2>Checkers</h2>
        <h6>({game.turn === 0 ? 'Black' : 'Red'} Turn)</h6>
        <div className="gameboard">
          {
            game.board.map((x) => {
              return (
                <div onMouseDown={() => {handleSquareClick(x.coord, x.id)}} className={"game-square " + x.space_color + (active?.availableMoves.has(x.coord) ? ' move' : '')} key={x.id}>
                  <span className='coord'>{x.coord}</span>
                  {
                    x.piece ? 
                    <div onMouseDown={(e) => {if(game.pieceTurn(x.piece)) activePiece(x.piece)}} className={"game-piece" + (game.pieceTurn(x.piece) ? ' movable' : '') + (game.pieces[x.piece].isBlack ? ' black' : '') + (active?.id === x.piece ? ' active' : '')}>
                      {game.pieces[x.piece].isKing ? <FontAwesomeIcon icon={faCrown} /> : ""}
                    </div> : ""
                  }
                </div>
              );
            })
          }
        </div>
      </header>
    </div>
  );
}

export default App;
