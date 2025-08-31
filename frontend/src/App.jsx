import React, { useState } from "react";
import StreamViewer from "./components/StreamViewer";
import AgentUI from "./components/AgentUI";

export default function App() {
  const [taskId, setTaskId] = useState(null);

  return (
    <div className="min-h-screen flex flex-col items-center justify-start bg-gray-50 p-6 font-sans">
      {/* Header */}
      <h1 className="text-3xl font-bold mb-6 text-gray-800">
        Graph Agent — Live Stream
      </h1>

      {/* Agent UI handles TaskForm and StreamViewer internally */}
      <div className="w-full max-w-4xl">
        <AgentUI />
      </div>
    </div>
  );
}