import { connectWebSocket, sendWebSocketMessage, disconnectWebSocket } from './websocket.js';

// Pass a task ID when connecting
connectWebSocket("12345",
  (msg) => console.log("Received:", msg), // onMessage
  () => console.log("Socket is open!"),   // onOpen
  () => console.log("Socket closed!")     // onClose
);

// Later, you can send messages like:
sendWebSocketMessage("ping");

export { 
  connectWebSocket, 
  sendWebSocketMessage, 
  disconnectWebSocket 
} from './websocket.js';