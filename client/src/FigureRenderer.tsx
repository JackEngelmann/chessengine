import { Figure } from "./api";

type Props = {
  figure: Figure;
};

function FigureRenderer(props: Props) {
  return <span>{getFigure(props.figure.colour, props.figure.name)}</span>;
}

export default FigureRenderer;

function getFigure(colour: Figure["colour"], name: Figure["name"]) {
  if (colour === "black") {
    if (name === "Bishop") return "♝";
    if (name === "King") return "♚";
    if (name === "Queen") return "♛";
    if (name === "Pawn") return "♟";
    if (name === "Rook") return "♜";
    if (name === "Knight") return "♞";
  }
  if (name === "Bishop") return "♗";
  if (name === "King") return "♔";
  if (name === "Queen") return "♕";
  if (name === "Pawn") return "♙";
  if (name === "Rook") return "♖";
  if (name === "Knight") return "♘";
}
