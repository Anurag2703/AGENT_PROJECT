import React, { useEffect, useRef, useState } from "react";
import ResultCard from "./ResultCard";

export default function StreamViewer({ taskId }) {
  const [displayedText, setDisplayedText] = useState("");
  const [loading, setLoading] = useState(true);
  const wsRef = useRef(null);

  // Typewriter effect
  const typeWriter = (text, index = 0) => {
    if (index < text.length) {
      setDisplayedText((prev) => prev + text[index]);
      setTimeout(() => typeWriter(text, index + 1), 30);
    }
  };

  useEffect(() => {
    if (!taskId) return;

    const ws = new WebSocket(`ws://localhost:8000/ws/run/${taskId}`);
    wsRef.current = ws;

    let accumulatedText = "";

    ws.onopen = () => {
      console.log("WS Connected");
      ws.send("ping");
    };

    ws.onmessage = (evt) => {
      const data = evt.data;

      if (data === "[DONE]") {
        setLoading(false);
        typeWriter(accumulatedText); // Animate final text
        ws.close();
        return;
      }

      try {
        // Backend sends plain text stream
        accumulatedText += data;
      } catch (e) {
        console.error("Invalid message", e);
      }
    };

    ws.onclose = () => console.log("WS closed");
    ws.onerror = (e) => console.error("WS error", e);

    return () => ws.close();
  }, [taskId]);

  return (
    <div
      style={{
        border: "1px solid #ddd",
        padding: 16,
        borderRadius: 8,
        background: "#ffffff",
        color: "#000",
        marginTop: 16,
        maxWidth: "800px",
        width: "100%",
      }}
    >
      <h3 style={{ fontWeight: "bold", marginBottom: "8px" }}>
        Streaming: {taskId}
      </h3>
      <div
        style={{
          whiteSpace: "pre-wrap",
          fontFamily: "monospace",
          minHeight: "150px",
        }}
      >
        {displayedText || (loading ? "Streaming..." : "No content received")}
      </div>
    </div>
  );
}





// import React, { useEffect, useRef, useState } from "react";
// import ResultCard from "./ResultCard";

// export default function StreamViewer({ taskId }) {
//   const [messages, setMessages] = useState([]);
//   const [finalResult, setFinalResult] = useState(null);
//   const wsRef = useRef(null);

//   useEffect(() => {
//     if (!taskId) return;
//     const ws = new WebSocket(`ws://localhost:8000/ws/run/${taskId}`);
//     wsRef.current = ws;

//     ws.onopen = () => {
//       console.log("WS open");
//       ws.send("ping");
//     };

//     ws.onmessage = (evt) => {
//       try {
//         const data = JSON.parse(evt.data);
//         setMessages((prev) => [...prev, data]);
//         if (data.phase === "completed" || data.phase === "final") {
//           fetch(`http://localhost:8000/api/status/${taskId}`)
//             .then((r) => r.json())
//             .then((js) => {
//               if (js.result) setFinalResult(js.result.final || js.result);
//             })
//             .catch(() => {});
//         }
//       } catch {
//         setMessages((prev) => [...prev, { raw: evt.data }]);
//       }
//     };

//     ws.onclose = () => console.log("WS closed");
//     ws.onerror = (e) => console.error("WS error", e);

//     return () => ws.close();
//   }, [taskId]);

//   return (
//     <div style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
//       <h3>Streaming: {taskId}</h3>
//       <div style={{ maxHeight: 400, overflowY: "auto", background: "#f8f8f8", padding: 8 }}>
//         {messages.map((m, i) => (
//           <div key={i} style={{ padding: 6, borderBottom: "1px dashed #eee" }}>
//             <pre style={{ margin: 0, whiteSpace: "pre-wrap" }}>{JSON.stringify(m, null, 2)}</pre>
//           </div>
//         ))}
//       </div>

//       <ResultCard result={finalResult} />
//     </div>
//   );
// }