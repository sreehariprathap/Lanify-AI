import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { BrowserRouter, Routes, Route } from "react-router";
import MainLayout from "./layouts/MainLayout";
import LaneDepartureMonitoring from "./features/Lane-departure-monitoring/LaneDepartureMonitoring.jsx";

createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
      <Route
        path="/"
        element={
          <MainLayout>
            <App />
          </MainLayout>
        }
      />
      <Route
        path="/lane-departure-monitoring"
        element={
          <MainLayout>
            <LaneDepartureMonitoring />
          </MainLayout>
        }
      />
    </Routes>
  </BrowserRouter>
);
