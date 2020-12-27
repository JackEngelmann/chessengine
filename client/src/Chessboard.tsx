import React from "react";
import { Figure } from "./api";
import "./Chessboard.css";
import FigureRenderer from "./FigureRenderer";

type Props = {
  figures: Figure[];
  selectedCell: [number, number] | undefined;
  setSelectedCell(selectedCell: [number, number] | undefined): void;
  moveProposals: [number, number][];
  makeMove(target: [number, number]): Promise<any>;
};

function Chessboard(props: Props) {
  const { selectedCell, setSelectedCell } = props;
  const cellRange = Array.from({ length: 8 }, (x, i) => i);
  const rowRange = Array.from({ length: 8 }, (x, i) => 7 - i);

  function renderRow(y: number) {
    return (
      <div className="chessboard__row" key={`row-${y}`}>
        {cellRange.map((x) => renderCell(x, y))}
      </div>
    );
  }

  function renderCell(x: number, y: number) {
    const color = (x + y) % 2 === 0 ? "white" : "black";
    const isMovePropsal = Boolean(
      props.moveProposals.find(
        (proposal) => proposal[0] === x && proposal[1] === y
      )
    );
    const figure = props.figures.find(
      (fig) => fig.positionX === x && fig.positionY === y
    );
    const isSelected =
      selectedCell && x === selectedCell[0] && y === selectedCell[1];

    let classNames = ["chessboard__cell", `chessboard__cell--${color}`];
    if (figure) {
      classNames.push("chessboard__cell--clickable");
    }
    if (isSelected) {
      classNames.push("chessboard__cell--selected");
    }

    function onClick() {
      if (isMovePropsal) {
        props.makeMove([x, y]);
      } else if (isSelected) {
        setSelectedCell(undefined);
      } else {
        setSelectedCell([x, y]);
      }
    }
    return (
      <div
        className={classNames.join(" ")}
        key={`cell-${x}-${y}`}
        onClick={onClick}
      >
        {figure && <FigureRenderer figure={figure} />}
        {isMovePropsal && <div className="chessboard__move-proposal" />}
      </div>
    );
  }

  return <div>{rowRange.map((y) => renderRow(y))}</div>;
}

export default Chessboard;
