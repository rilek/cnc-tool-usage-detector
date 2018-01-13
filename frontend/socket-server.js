import http from 'http';
import fs from 'fs';
import express from 'express';
import socketio from 'socket.io';
import watch from 'node-watch';
import cp from 'child_process';
import mem from 'amnesia';


const port = process.env.PORT || 8081;
let subprocess = null;
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

let initStore = {
    machine_state: "stopped",
    tool_state: -1,
    buffer_state: 0
}

io.on('connection', socket => {
    console.log('a user connected');
    initStore['machine_state'] = subprocess !== null && subprocess !== undefined ? "running" : "stopped";
    socket.emit('connected', initStore);

    socket.on('message', data => {
        socket.emit('response', data);
    });

    socket.on('reload', () => {
        socket.emit('reload');
    });

    socket.on('start_machine', () => {
        setTimeout(() => {
            // subprocess = 1;
            subprocess = cp.spawn('python3', [__dirname + '/../machine.py'], {detached: true});
            subprocess.unref();
            console.log(`Subprocess ID: ${subprocess.pid}`);
            socket.emit('start_machine_success');
        }, 2000);
        setTimeout(() => {
            initStore['tool_state'] = 0;
            socket.emit('sharp_tool')
        }, 4000);
    })

    socket.on('stop_machine', () => {
        subprocess.kill();
        subprocess = null;
        setTimeout(() => socket.emit('stop_machine_success'), 2000);
    })

    // watcher.on('change', (evt, name) => {
    //   socket.emit('reload');
    // });

    bufferWatcher.on('change', (evt, name) => {
        if(evt === "update") {
        socket.emit("tmp_file_change", name);
        }

    });
});


server.listen(port, function () {
    console.log(`listening on *:${port}`);
});

const fn = () => {
    if(subprocess)
        subprocess.kill();
    process.exit();
}
process.stdin.resume();
process.on("exit", fn);
process.on("SIGINT", fn);
process.on("SIGUSR1", fn);
process.on("SIGUSR2", fn);
process.on("uncaughtException", fn);
