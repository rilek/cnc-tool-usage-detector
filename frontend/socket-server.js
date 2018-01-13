import http from 'http';
import fs from 'fs';
import express from 'express';
import socketio from 'socket.io';
import watch from 'node-watch';

const app = express();
const server = http.Server(app);
const io = socketio(server);
// const watcher = watch(__dirname,
//     { recursive: true,
//        filter: function(name) {
//          return !/node_modules/.test(name);
//     }});


const bufferWatcher = watch(__dirname + "/../tmp_files");

app.use('/statics', express.static(__dirname +  '/statics'));

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

let store = {
    machine_state: "stopped",
    tool_state: -1,
    buffer_state: 0
};

io.on('connection', socket => {
    console.log('a user connected');
    socket.emit('connected', store);

    socket.on('message', data => {
        socket.emit('response', data);
    });

    socket.on('reload', () => {
        socket.emit('reload');
    });

    socket.on('start_machine', () => {
        setTimeout(() => socket.emit('start_machine_success'), 2000);
        setTimeout(() => socket.emit('sharp_tool'), 4000);
    })

    socket.on('stop_machine', () => {
        setTimeout(() => socket.emit('stop_machine_success'), 2000);
    })

    // watcher.on('change', (evt, name) => {
    //   socket.emit('reload');
    // });

    bufferWatcher.on('change', (evt, name) => {
        socket.emit("tmp_file_change");
    });
});


const port = process.env.PORT || 3000;
server.listen(port, function () {
    console.log(`listening on *:${port}`);
});
