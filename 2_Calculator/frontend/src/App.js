import React, { useState } from 'react';
import './App.css';

function App() {

  // state to manage the user input "expression"
  const [expression, setExpression] = useState('');
  // store the result
  const [result, setResult] = useState('');

  const handleButtonClick = (value) => {
    setExpression((prev) => prev + value);
  }

  const clear = () => { 
    const newExpression = expression.slice(0, -1);
    setExpression(newExpression);
  }

  const clearAll = () => { 
    setExpression('');
  }

  const handleCalculate = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/calculate/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ expression }),
      });

      // parse the await response and update the result state
      const data = await response.json();
      setResult(data.result);
    } catch(error) {
      console.error("Error Calculating", error);
    }
  };

  return (
    <div className="App max-w-3xl mx-auto">
      <div>
        <h1 className="mt-4 mb-4">Django + React + TailwindCSS Calculator</h1>
        <div className="border border-b-2 p-12 relative rounded-md shadow-sm">
          {/* input field to display the expression */}
          <input 
              type="text" 
              value={expression} 
              className="absolute focus:outline-none left-10 text-lg" 
          />
          {/* Button for clear and clear all */}
          <div className="flex space-x-4 absolute bottom-4 right-4">
            <button onClick={clear} className="bg-red-400 text-sm text-white border rounded-full px-4 py-2">Clear</button>
            <button onClick={clearAll} className="bg-red-400 text-sm text-white border rounded-full px-4 py-2">Clear All</button>
          </div>
          {/* display the result */}
          <div className="absolute top-3 right-6">
            <h1>{result}</h1>
          </div>
        </div>
      </div>
      {/* grid layout for the calculator buttons */}
      <div className="grid grid-cols-4 gap-10 border bg-gray-300 rounded-md p-12 shadow-xl">
        {/* map the buttons */}
        {
          [7, 8, 9, "/"].map((value) => (
            <button className="border p-4 bg-white rounded-full" key={value} onClick={() => handleButtonClick(value)}>
              {value}
            </button>
        ))}
        {
          [4, 5, 6, "*"].map((value) => (
            <button className="border p-4 bg-white rounded-full" key={value} onClick={() => handleButtonClick(value)}>
              {value}
            </button>
        ))}
        {
          [1, 2, 3, "-"].map((value) => (
            <button className="border p-4 bg-white rounded-full" key={value} onClick={() => handleButtonClick(value)}>
              {value}
            </button>
        ))}
        {
          [0, ".", "=", "+"].map((value) => (
            <button className={`${value === "=" && 'border-red-300 border-8'} border p-4 bg-white rounded-full`}
              key={value} 
              onClick={value === "=" ? handleCalculate : () => handleButtonClick(value)}
            >
              {value}
            </button>
        ))}
      </div>
    </div>
  );
}

export default App;
