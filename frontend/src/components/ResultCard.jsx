import React from "react";

export default function ResultCard({ result }) {
  if (!result) return null;
  const final = result.final || result;
  return (
    <div style={{
      border: "1px solid #e6e6e6",
      padding: 12,
      borderRadius: 8,
      background: "#fff",
      marginTop: 12
    }}>
      <h4>Result</h4>
      <div style={{ whiteSpace: "pre-wrap" }}>{final}</div>
    </div>
  );
}