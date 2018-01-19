import http from 'http';
import fs from 'fs';
import path from 'path';
import express from 'express';
import socketio from 'socket.io';
import {spawn} from 'child_process';
import c from '../config/config';
import { addLogRow, timeout, getClassStr } from './utils';
import initState, {dispatch, setState, getState} from './store';
import a from './actions';
import request from 'request';
import { StringDecoder } from 'string_decoder';
import chokidar from 'chokidar';


// const port = process.env.PORT || 8081;
const port = 8081;
const app = express();
const server = http.Server(app);
const io = socketio(server);
let subprocess = null;
let initStore = initState;

const textStream = fs.createWriteStream(c["textLogPath"], {flags: 'a'});
const htmlStream = fs.createWriteStream(c["htmlLogPath"], {flags: 'a'});

addLogRow()("Setting up server");
app.use('/statics', express.static(__dirname +  '/statics'));
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

chokidar.watch(c["tmpFilesFolder"], {ignoreInitial: true}).on("add", name => {
  const file_class = name.split(path.sep).reverse()[0].startsWith("Ostre") ? "0" : "1";
  const addLog = addLogRow(io);
  addLog('New file: ');
  addLog(name, 'yellow', true);

  request.post(c["featuresApi"], {body: name} , (err, res) => {
    request.post(c["classifierApi"], {json: {"features": JSON.parse(res.body)}}, (err, res) => {
      addLog("Real Class: ");
      addLog(file_class, null, true);
      addLog(". Predicted class: ", null, true);
      addLog(res.body, null, true);
      
      if (res.body === 1)
        dispatch("set_blunt_tool", io.sockets);
      else if (res.body === 0)
        dispatch("set_sharp_tool", io.sockets);
    });
  });
});

io.on('connection', socket => {
  const addLog = addLogRow(io);

  dispatch(
    "init_machine_state",
    subprocess !== null && subprocess !== undefined ? "running" : "stopped"
  );
  
  socket.emit('connected', {
    state: getState(),
    log: fs.readFileSync(c["htmlLogPath"], "utf-8")
  });
  addLog("New connection");
  
  
  socket.on("disconnect", () => {
    addLog("User diconnected.", 'red');
  })

  socket.on('start_machine', () => {
    addLog("Starting machine...", 'yellow');

    (async () => {
      await timeout(2000);
      subprocess = spawn('py', [c["rootFolder"] + 'run_emulator.py'], {detached: true});
      console.log(c["rootFolder"] + 'machine.py');
      subprocess.unref();
      addLog(`Subprocess ID: ${subprocess.pid}`);
      io.sockets.emit('start_machine_success');
      addLog("Machine started!", 'green');
    })();
  });

  socket.on('stop_machine', () => {
    addLog(`Killing subprocess: ${subprocess.pid}`);
    addLog("Stopping machine...", "yellow");

    (async () => {
      subprocess.kill();
      subprocess = null;
      await timeout(2000);
      initStore['tool_state'] = -1;
      addLog(`Subprocess killed`);
      io.sockets.emit('stop_machine_success');
      addLog("Machine stopped!", "green");
    })();
  });

  socket.on('add_log_row', (rawText, color, omitLine) => {
    addLogRow()(rawText, color, omitLine);
  });

  socket.on('clear_logs', () => {
    fs.writeFile(c['htmlLogPath'], "", () => {});
    fs.writeFile(c['textLogPath'], "", () => {});
    io.sockets.emit("clear_logs")
    addLog("Logs cleared");
  });
});


server.listen(port, function () {
  addLogRow()(`Listening on *:${port}`);
});

const fn = (err) => {
  process.stdin.resume();
  if(subprocess)
    subprocess.kill();
  addLogRow()("Turning off the server, code: " + err + "\r\n");
  process.exit();
}
process.on("exit", fn);
process.on("SIGINT", fn);
process.on("SIGUSR1", fn);
process.on("SIGUSR2", fn);
process.on("uncaughtException", fn);
