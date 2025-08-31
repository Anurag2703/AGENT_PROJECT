import React, { useState } from "react";

export default function TaskForm({ onStarted }){
  const [prompt, setPrompt] = useState("");

  async function startTask(){
    if(!prompt) return alert("Enter prompt");
    const res = await fetch("http://localhost:8000/api/start", {
      method: "POST",
      headers: { "Content-Type":"application/json" },
      body: JSON.stringify({ prompt, options: {} })
    });
    if(!res.ok) return alert("Failed to start");
    const data = await res.json();
    onStarted(data.task_id);
  }

  return (
    <div style={{ marginBottom: 16 }}>
      <textarea value={prompt} onChange={e=>setPrompt(e.target.value)} rows={4} style={{ width:"100%" }} placeholder="Describe the task..." />
      <div style={{ marginTop: 8 }}>
        <button onClick={startTask}>Start Task</button>
      </div>
    </div>
  );
}