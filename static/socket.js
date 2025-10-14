
const HOST = "ws://localhost:62343";

const socket = new WebSocket(HOST);

socket.addEventListener("open", (event) => {
  console.log("Connected to the WebSocket server.");
});

socket.addEventListener("message", (event) => {
  console.log("Message received: ", event.data);

  // Update the chat UI in real-time (implement your logic here)
  const messageContainer = document.getElementById("messages");
  const newMessage = document.createElement("div");
  newMessage.textContent = event.data; // Server payload
  messageContainer.appendChild(newMessage);
});

socket.addEventListener("close", (event) => {
  console.log("Disconnected from WebSocket server.");
});

socket.addEventListener("error", (event) => {
  console.error("WebSocket error: ", event);
});

function sendMessage(message) {
  if (socket.readyState === WebSocket.OPEN) {
    console.log("Sending message: ", message);
    socket.send(message);
  } else {
    console.error("Socket is not open.");
  }
}

// You can bind the `sendMessage` function to UI input events