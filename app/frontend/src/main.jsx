import React from "react";
import ReactDOM from "react-dom";
import App from "./App.jsx";

// Make sure your index.html has: <div id="root"></div>
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);
