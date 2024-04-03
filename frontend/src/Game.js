import { v4 as uuidv4 } from 'uuid';

const sqrCnt = 64;
export class Checkers {
    pieces = {};
    board = [];
    turn = 0; //black is 0, red is 1

    constructor(board = [], pieces = {}) {
        if (board.length === 0) {
            let sqrs = [];
            for (let i = 0; i < sqrCnt; i++) {
                const isBlack = (Math.floor(i/8) % 2 === 0 && (i % 8) % 2 === 0) || (Math.floor(i/8) % 2 === 1 && (i % 8) % 2 === 1);
                let obj = {
                    id: i,
                    x: i % 8,
                    y: Math.floor(i / 8),
                    coord: `(${i % 8}, ${Math.floor(i / 8)})`,
                    space_color: isBlack ? 'black' : 'red',
                };
                if (obj.y < 3 && isBlack) {
                    obj.piece = this.createPiece(i % 8, Math.floor(i / 8), true);
                } else if (obj.y > 4 && isBlack) {
                    obj.piece = this.createPiece(i % 8, Math.floor(i / 8), false);
                }
                sqrs.push(obj);
            }
            this.board = sqrs;  
        } else {
            this.board = board;
            this.pieces = pieces;
        }
    }

    createPiece(x, y, isBlack=false) {
        const id = uuidv4();
        this.pieces[id] = {
          id,
          x,
          y,
          isBlack: isBlack,
          isKing: false,
        }
        return id;
    }

    checkSpace(x, y) {
        return Object.values(this.pieces).find((p) => p.x === x && p.y === y);
      }
    
    getValidMoves(id) {
        const p = this.pieces[id];
        let validMoves = new Set();
        let toCheck = p.isKing ? [{dx: 1, dy: 1}, {dx: -1, dy: -1}, {dx: 1, dy: -1}, {dx: -1, dy: -1}] : (p.isBlack ? [{dx: 1, dy: 1}, {dx: -1, dy: 1}] : [{dx: 1, dy: -1}, {dx: -1, dy: -1}]);
        toCheck.forEach((x) => {
          if (p.x + x.dx <= 7 && p.y + x.dy <= 7 && p.x + x.dx >= 0 && p.y + x.dy  >= 0) {
            const check = this.checkSpace(p.x + x.dx, p.y + x.dy);
            if (check != null) {
              if (check.isBlack !== p.isBlack) {
                if (p.x + (2 * x.dx) <= 7 && p.y + (2 * x.dy) <= 7 && p.x + (2 * x.dx) >= 0 && p.y + (2 * x.dy) >= 0) {
                  if (this.checkSpace(p.x + (2 * x.dx), p.y + (2 * x.dy)) === undefined) {
                    validMoves.add(`(${p.x + (2 * x.dx)}, ${p.y + (2 * x.dy)})`);
                  }
                }
              }
            } else {
              validMoves.add(`(${p.x + x.dx}, ${p.y + x.dy})`);
            }
          }
        });
        return validMoves
    }

    movePiece(space, id) {
        const piece = this.pieces[id];
        const lastSpace = this.board.find((x) => x.piece === id);
        lastSpace.piece = null;
        const dx = this.board[space].x - lastSpace.x;
        if (Math.abs(dx) === 2) {
            const dy = this.board[space].y - lastSpace.y;
        }
        this.board[space].piece = id;
        piece.x = this.board[space].x;
        piece.y = this.board[space].y;
        this.turn = this.turn === 0 ? 1 : 0;
    }

    pieceTurn(id) {
        const piece = this.pieces[id];
        return (piece.isBlack && this.turn === 0) || (!piece.isBlack && this.turn === 1);
    }
}