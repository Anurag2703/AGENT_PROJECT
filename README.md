# **Graph Agent — Live Streaming with LangGraph**

## **1️⃣ What is the Project?**

This project is a **real-time AI agent execution and streaming system** built with:

* **Frontend**: React (Vite) + Tailwind CSS
* **Backend**: FastAPI + LangGraph + WebSockets
* **Model**: Google Gemini API

The system enables users to send a **prompt to the backend**, which is processed by a LangGraph-based agent. The **response is streamed in real-time** to the frontend using WebSocket connections, providing a **smooth typewriter animation** for better interactivity and visualization. No explicit A2A layer implemented — just single-agent streaming, but multiple agents can be added to the workflow due the A2A pipeline.

---

## **2️⃣ Purpose of the Project**

The purpose of this project is to **demonstrate a scalable AI agent pipeline** with **real-time streaming capabilities**. It solves key issues in modern AI applications, such as:

* Reducing latency by **streaming outputs** instead of waiting for the entire result.
* Supporting **dynamic agent workflows** with LangGraph for complex reasoning tasks.
* Creating a **developer-friendly and user-friendly UI** for testing and interacting with prompts.

This makes the project suitable for **AI demos, research, or production-grade agents** that need responsive output delivery.

---

## **3️⃣ Scope of the Project**

### **Frontend**

* A **React-based UI** that:

  * Accepts prompts from users.
  * Establishes **WebSocket connections** to listen for backend streaming.
  * Displays outputs in a **smooth, typewriter animation style**.

---

### **Backend**

* **FastAPI application** with:

  * REST APIs for task creation and status checks.
  * WebSocket endpoints for **real-time streaming** of responses.
  * Integration with **LangGraph** for multi-step reasoning agents.
  * Support for **Google Gemini API** for language generation.

---

### **Use Cases**

* AI assistant demos.
* Streaming conversational AI applications.
* Workflow automation agents.
* Educational tools for demonstrating real-time AI response streaming.

---

### **Future Enhancements**

* Add support for **multiple AI models** (OpenAI, Claude, etc.).
* Database integration for **persistent chat history**.
* Enhanced error handling and retry mechanisms.
* Deploy backend to a cloud service for remote usage with the hosted frontend.

---

Would you like me to include **installation and usage instructions** in this `README.md`?
