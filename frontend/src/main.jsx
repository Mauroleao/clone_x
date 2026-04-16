import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx"; // Note que removi a linha do index.css

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);