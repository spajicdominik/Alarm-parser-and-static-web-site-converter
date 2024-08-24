const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const chokidar = require('chokidar');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: '*', 
        methods: ['GET', 'POST']
    }
});

const folderToWatch = './data';

chokidar.watch(folderToWatch).on('all', (event, path) => {
  console.log(`${event} detected in ${path}`);
  io.emit('folder-changed');
});

io.on('connection', (socket) => {
  console.log('New client connected');
  socket.on('disconnect', () => console.log('Client disconnected'));
});

server.listen(8080, () => console.log('Server is listening on port 8080'));
