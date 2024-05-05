import { v4 as uuidv4 } from "uuid";
import { socket } from "./socket";

const sqrCnt = 64;
export class Checkers {
  pieces = {};
  board = [];
  turn = 0; //black is 0, red is 1

  constructor(board = [], pieces = {}, turn = 0) {
    if (board.length === 0) {
      let sqrs = [];
      for (let i = 0; i < sqrCnt; i++) {
        const isBlack =
          (Math.floor(i / 8) % 2 === 0 && (i % 8) % 2 === 0) ||
          (Math.floor(i / 8) % 2 === 1 && (i % 8) % 2 === 1);
        let obj = {
          id: i,
          x: i % 8,
          y: Math.floor(i / 8),
          coord: `(${i % 8}, ${Math.floor(i / 8)})`,
          space_color: isBlack ? "black" : "red",
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
      this.turn = turn;
    }
  }

  createPiece(x, y, isBlack = false) {
    const id = uuidv4();
    this.pieces[id] = {
      id,
      x,
      y,
      isBlack: isBlack,
      isKing: false,
    };
    return id;
  }

  checkSpace(x, y) {
    let spaceId = x + y * 8;
    let pieceId = this.board[spaceId].piece;
    if (pieceId) return this.pieces[pieceId];
    return undefined;
  }

  inBound(x, y) {
    return x <= 7 && x >= 0 && y >= 0 && y <= 7;
  }

  getValidUpdated(
    id,
    x0 = null,
    y0 = null,
    validMoves = new Set(),
    moveInfo = {},
    from = null,
    capturedPieces = []
  ) {
    const p = this.pieces[id];
    const x = x0 === null ? p.x : x0;
    const y = y0 === null ? p.y : y0;
    let toCheck = p.isKing
      ? [
          { dx: 1, dy: 1 },
          { dx: -1, dy: -1 },
          { dx: 1, dy: -1 },
          { dx: -1, dy: 1 },
        ]
      : p.isBlack
      ? [
          { dx: 1, dy: 1 },
          { dx: -1, dy: 1 },
        ]
      : [
          { dx: 1, dy: -1 },
          { dx: -1, dy: -1 },
        ];
    toCheck.forEach((d) => {
      const x1 = x + d.dx;
      const y1 = y + d.dy;
      if (this.inBound(x1, y1)) {
        const check = this.checkSpace(x1, y1);
        if (check != null) {
          if (
            check.isBlack !== p.isBlack &&
            !capturedPieces.includes(check.id)
          ) {
            const x2 = x + d.dx * 2;
            const y2 = y + d.dy * 2;
            if (this.inBound(x2, y2)) {
              //If next diagonal space is empty
              if (this.checkSpace(x2, y2) === undefined) {
                const move = `(${x2}, ${y2})`;
                validMoves.add(move);
                moveInfo[move] = {
                  captures: [...capturedPieces, check.id],
                };
                this.getValidUpdated(
                  id,
                  x2,
                  y2,
                  validMoves,
                  moveInfo,
                  { x: x2, y: y2 },
                  [...capturedPieces, check.id]
                );
              }
            }
          }
        } else if (from === null) {
          const move = `(${x1}, ${y1})`;
          validMoves.add(move);
          moveInfo[move] = {
            captures: [],
          };
        }
      }
    });
    return { validMoves, moveInfo };
  }

  getValidMoves(id) {
    const p = this.pieces[id];
    let validMoves = new Set();
    let moveInfo = {};
    let toCheck = p.isKing
      ? [
          { dx: 1, dy: 1 },
          { dx: -1, dy: -1 },
          { dx: 1, dy: -1 },
          { dx: -1, dy: -1 },
        ]
      : p.isBlack
      ? [
          { dx: 1, dy: 1 },
          { dx: -1, dy: 1 },
        ]
      : [
          { dx: 1, dy: -1 },
          { dx: -1, dy: -1 },
        ];
    toCheck.forEach((x, ind) => {
      if (
        p.x + x.dx <= 7 &&
        p.y + x.dy <= 7 &&
        p.x + x.dx >= 0 &&
        p.y + x.dy >= 0
      ) {
        const check = this.checkSpace(p.x + x.dx, p.y + x.dy);
        if (check != null) {
          //If is opponents piece
          if (check.isBlack !== p.isBlack) {
            if (
              p.x + 2 * x.dx <= 7 &&
              p.y + 2 * x.dy <= 7 &&
              p.x + 2 * x.dx >= 0 &&
              p.y + 2 * x.dy >= 0
            ) {
              //If next diagonal space is empty
              if (
                this.checkSpace(p.x + 2 * x.dx, p.y + 2 * x.dy) === undefined
              ) {
                const move = `(${p.x + 2 * x.dx}, ${p.y + 2 * x.dy})`;
                validMoves.add(move);
                moveInfo[move] = {
                  captures: [check.id],
                };
              }
            }
          }
        } else {
          const move = `(${p.x + x.dx}, ${p.y + x.dy})`;
          validMoves.add(move);
          moveInfo[move] = {
            captures: [],
          };
        }
      }
    });
    return { validMoves, moveInfo };
  }

  movePiece(space, id, info) {
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
    if (piece.isBlack && piece.y === 7) piece.isKing = true;
    else if (!piece.isBlack && piece.y === 0) piece.isKing = true;
    this.turn = this.turn === 0 ? 1 : 0;
    if (info.captures.length !== 0) {
      info.captures.forEach((x) => {
        const space = this.board.find((s) => s.piece === x);
        if (space) space.piece = null;
        this.pieces[x].captured = true;
      });
    }
    const processed = this.processBoard();
    console.log(processed);
    socket.emit("game_status", processed);
  }

  pieceTurn(id) {
    const piece = this.pieces[id];
    return (
      (piece.isBlack && this.turn === 0) || (!piece.isBlack && this.turn === 1)
    );
  }

  processBoard() {
    let arr = [];
    this.board.forEach((e, i) => {
      const x = Math.floor(i / 8);
      if (x === i / 8) arr.push([]);
      if (this.pieces[e.piece] != null)
        arr[x].push(
          (this.pieces[e.piece].isBlack ? "B" : "R") +
            (this.pieces[e.piece].isKing ? "K" : "")
        );
      else arr[x].push("");
    });
    return arr;
  }
}
