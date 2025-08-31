// websocket.js
let socket;

export function connectWebSocket(taskId, onMessage, onOpen, onClose) {
  socket = new WebSocket(`ws://127.0.0.1:8000/ws/run/${taskId}`);

  socket.onopen = () => {
    console.log(`✅ WebSocket connected for task: ${taskId}`);
    if (onOpen) onOpen();
  };

  socket.onmessage = (event) => {
    console.log("📩 Message:", event.data);
    if (onMessage) onMessage(event.data);
  };

  socket.onclose = () => {
    console.log("❌ WebSocket closed");
    if (onClose) onClose();
  };

  socket.onerror = (err) => console.error("⚠️ WebSocket error:", err);
}

export function sendWebSocketMessage(message) {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(message);
  } else {
    console.warn("WebSocket not connected.");
  }
}

export function disconnectWebSocket() {
  if (socket) socket.close();
}