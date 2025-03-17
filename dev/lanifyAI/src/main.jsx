import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { BrowserRouter, Routes, Route } from "react-router";
import MainLayout from "./layouts/MainLayout";
import LaneDepartureMonitoring from "./features/Lane-departure-monitoring/LaneDepartureMonitoring.jsx";
import DrivingReportDashboard from "./features/Driving-report-dashboard/DrivingReportDashboard.jsx";
import DrivingReport from "./features/Driving-report-dashboard/Driving-Report/DrivingReport.jsx";
import About from "./features/about/About.jsx";

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
      <Route
        path="/driving-report-dashboard"
        element={
          <MainLayout>
            <DrivingReportDashboard />
          </MainLayout>
        }
      />
      <Route
        path="/driving-report/:vehicleId"
        element={
          <MainLayout>
            <DrivingReport />
          </MainLayout>
        }
      />
      <Route
        path="/road-assessment"
        element={
          <MainLayout>
            <DrivingReportDashboard />
          </MainLayout>
        }
      />
      <Route
        path="/road-assessment/:locationId"
        element={
          <MainLayout>
            <DrivingReport />
          </MainLayout>
        }
      />
      <Route
        path="/about"
        element={
          <MainLayout>
            <About />
          </MainLayout>
        }
      />
    </Routes>
  </BrowserRouter>
);
