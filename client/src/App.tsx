import { useEffect, useState } from "react";
import { Game, Figure } from "./api";
import "./App.css";
import Chessboard from "./Chessboard";

function App() {
  const [game, setGame] = useState<Game | undefined>(undefined);
  const [figures, setFigures] = useState<Figure[]>([]);
  const [moveCounter, setMoveCounter] = useState(0);
  const [selectedCell, setSelectedCell] = useState<
    [number, number] | undefined
  >();
  const [moveProposals, setMoveProposals] = useState<[number, number][]>([]);

  async function createGame() {
    fetch("/game", {
      method: "POST",
    })
      .then((response) => response.json())
      .then((result) => setGame(result));
  }

  useEffect(() => {
    if (!game) return;
    fetch(`/game/${game.id}`)
      .then((response) => response.json())
      .then((result) => setGame(result));
  }, [moveCounter]);

  async function makeMove(target: [number, number]) {
    if (!game || !selectedCell) return;
    fetch(`/game/${game.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: {
          x: selectedCell[0],
          y: selectedCell[1],
        },
        to: {
          x: target[0],
          y: target[1],
        },
      }),
    }).then(() => {
      setSelectedCell(undefined);
      setMoveCounter((counter) => counter + 1);
    });
  }

  useEffect(() => {
    if (!game) return;
    fetch(`/game/${game.id}/figures`)
      .then((response) => response.json())
      .then((result) => setFigures(result));
  }, [game]);

  const selectedFigure = figures.find(
    (fig) =>
      selectedCell &&
      fig.positionX === selectedCell[0] &&
      fig.positionY === selectedCell[1]
  );

  useEffect(() => {
    if (!game || !selectedFigure) {
      setMoveProposals([]);
    } else {
      fetch(`/game/${game.id}/figures/${selectedFigure.id}`)
        .then((response) => response.json())
        .then((result) => setMoveProposals(result["validMoves"]));
    }
  }, [selectedFigure, game]);

  return (
    <div className="App">
      {!game && <button onClick={createGame}>Create Game</button>}
      {game && (
        <div>
          Id: {game.id}
          <br />
          In turn: {game.inTurn}
          <br />
          <Chessboard
            makeMove={makeMove}
            figures={figures}
            selectedCell={selectedCell}
            setSelectedCell={setSelectedCell}
            moveProposals={moveProposals}
          />
        </div>
      )}
    </div>
  );
}

export default App;
