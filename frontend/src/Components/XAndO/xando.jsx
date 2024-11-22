import React, { useRef, useState } from "react";
import "./xando.css";
import circle_icon from "../Assets/circle.png";
import cross_icon from "../Assets/cross.png";

let data = ["", "", "", "", "", "", "", "", ""];
let playerMoves = { X: [], O: [] }; 

const XAndO = () => {
  let [count, setCount] = useState(0);
  let [lock, setLock] = useState(false);
  let titleRef = useRef(null);

  let box0 = useRef(null);
  let box1 = useRef(null);
  let box2 = useRef(null);
  let box3 = useRef(null);
  let box4 = useRef(null);
  let box5 = useRef(null);
  let box6 = useRef(null);
  let box7 = useRef(null);
  let box8 = useRef(null);
  let box_array = [box0, box1, box2, box3, box4, box5, box6, box7, box8];

  const toggle = (e, num) => {
    if (lock || data[num] !== "") {
      return;
    }

    let player = count % 2 === 0 ? "X" : "O";

    e.target.innerHTML = `<img src='${player === "X" ? cross_icon : circle_icon}'>`;
    data[num] = player;
    playerMoves[player].push(num);

    setCount(++count);

    // Handle removal logic for every fourth move
    if (playerMoves[player].length > 3) {
      const removedIndex = playerMoves[player].shift(); // Remove first move
      data[removedIndex] = ""; // Clear data for that move
      box_array[removedIndex].current.innerHTML = ""; // Clear board UI for that move
    }

    checkWin();
  };

  const checkWin = () => {
    const winningCombinations = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6],
    ];

    for (let combination of winningCombinations) {
      const [a, b, c] = combination;
      if (data[a] === data[b] && data[b] === data[c] && data[a] !== "") {
        won(data[a]);
        return;
      }
    }
  };

  const won = (winner) => {
    setLock(true);
    titleRef.current.innerHTML = `Congratulations: <img src='${
      winner === "X" ? cross_icon : circle_icon
    }'>`;
  };

  const reset = () => {
    setLock(false);
    data = ["", "", "", "", "", "", "", "", ""];
    playerMoves = { X: [], O: [] }; // Reset moves history
    titleRef.current.innerHTML = "XAndO Game in React";
    box_array.forEach((box) => {
      box.current.innerHTML = "";
    });
    setCount(0); // Reset count
  };

  return (
    <div className="container">
      <h1 className="title" ref={titleRef}>
        XAndO Game in React
      </h1>

      <div className="board">
        <div className="row1">
          <div
            className="boxes"
            ref={box0}
            onClick={(e) => {
              toggle(e, 0);
            }}
          ></div>
          <div
            className="boxes"
            ref={box1}
            onClick={(e) => {
              toggle(e, 1);
            }}
          ></div>
          <div
            className="boxes"
            ref={box2}
            onClick={(e) => {
              toggle(e, 2);
            }}
          ></div>
        </div>
        <div className="row2">
          <div
            className="boxes"
            ref={box3}
            onClick={(e) => {
              toggle(e, 3);
            }}
          ></div>
          <div
            className="boxes"
            ref={box4}
            onClick={(e) => {
              toggle(e, 4);
            }}
          ></div>
          <div
            className="boxes"
            ref={box5}
            onClick={(e) => {
              toggle(e, 5);
            }}
          ></div>
        </div>
        <div className="row3">
          <div
            className="boxes"
            ref={box6}
            onClick={(e) => {
              toggle(e, 6);
            }}
          ></div>
          <div
            className="boxes"
            ref={box7}
            onClick={(e) => {
              toggle(e, 7);
            }}
          ></div>
          <div
            className="boxes"
            ref={box8}
            onClick={(e) => {
              toggle(e, 8);
            }}
          ></div>
        </div>
      </div>

      <button className="reset" onClick={reset}>
        Reset
      </button>
    </div>
  );
};

export default XAndO;
