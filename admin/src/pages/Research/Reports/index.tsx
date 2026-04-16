import React from "react";
import { Navigate } from "react-router-dom";

const Reports: React.FC = () => {
  return <Navigate to="/research/reports/manage" replace />;
};

export default Reports;
