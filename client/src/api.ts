export type Figure = {
  positionX: number;
  positionY: number;
  colour: "white" | "black";
  name: "Bishop" | "King" | "Queen" | "Pawn" | "Rook" | "Knight";
  id: number;
};

export type Game = {
  id: number;
  inTurn: string;
  check: boolean;
  checkmate: boolean;
  stalemate: boolean;
};
