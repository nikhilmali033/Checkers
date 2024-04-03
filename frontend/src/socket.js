import { io } from "socket.io-client";

const socket = io('http://localhost:6969', {
    withCredentials: true,
    autoConnect: false,
});
  
socket.onAny((event, ...args) => {
    console.log(event, args);
});

export { io, socket };