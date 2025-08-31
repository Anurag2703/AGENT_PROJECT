import React, { useState } from "react";
import TaskForm from "./TaskForm";
import StreamViewer from "./StreamViewer";

export default function AgentUI() {
  const [taskId, setTaskId] = useState(null);

  return (
    <div style={{ padding: 20 }}>
      <h2>🤖 Agent Execution UI</h2>
      {/* Input Form to start a new task */}
      <TaskForm onStarted={setTaskId} />

      {/* Live Stream Display */}
      {taskId && <StreamViewer taskId={taskId} />}
    </div>
  );
}




// import { useEffect, useState } from "react";
// import {
//   connectWebSocket,
//   sendWebSocketMessage,
//   disconnectWebSocket,
// } from "../api";

// export default function AgentUI() {
//     const [messages, setMessages] = useState([]);
//     const [input, setInput] = useState("");

//     // Connect WebSocket on mount and cleanup on unmount
//     useEffect(() => {
//     const taskId = "12345"; // or dynamically set this ID
//     connectWebSocket(
//         taskId,
//         (msg) => setMessages((prev) => [...prev, msg]),
//         () => setMessages((prev) => [...prev, "✅ Connected to Agent"]),
//         () => setMessages((prev) => [...prev, "❌ Disconnected from Agent"])
//     );

//     return () => disconnectWebSocket();
//     }, []);

//     // Send message to backend
//     const handleSend = () => {
//         if (input.trim()) {
//         sendWebSocketMessage(input);
//         setMessages((prev) => [...prev, `📝 Sent: ${input}`]);
//         setInput("");
//         }
//     };

//     return (
//         <div className="flex flex-col items-center p-4 bg-gray-100 rounded-xl shadow-md w-full">
//         <div className="w-full max-w-lg bg-white rounded-xl shadow p-4">
//             <h2 className="text-xl font-semibold mb-3 text-gray-800 text-center">
//             🤖 Agent Live Stream
//             </h2>

//             {/* Message Display */}
//             <div className="bg-gray-50 h-64 overflow-y-auto border border-gray-300 rounded-md p-2 text-sm mb-3">
//             {messages.length > 0 ? (
//                 messages.map((msg, idx) => (
//                 <div key={idx} className="mb-1">
//                     {msg}
//                 </div>
//                 ))
//             ) : (
//                 <p className="text-gray-500 text-center">No messages yet...</p>
//             )}
//             </div>

//             {/* Input and Send Button */}
//             <div className="flex gap-2">
//             <input
//                 type="text"
//                 className="flex-grow border border-gray-300 rounded-lg p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
//                 placeholder="Type a message..."
//                 value={input}
//                 onChange={(e) => setInput(e.target.value)}
//                 onKeyDown={(e) => e.key === "Enter" && handleSend()}
//             />
//             <button
//                 onClick={handleSend}
//                 className="bg-blue-500 text-white px-4 rounded-lg text-sm hover:bg-blue-600 transition"
//             >
//                 Send
//             </button>
//             </div>
//         </div>
//         </div>
//     );
// }