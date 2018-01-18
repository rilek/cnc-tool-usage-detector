import http from 'http';
import fs from 'fs';
import express from 'express';
import socketio from 'socket.io';
import watch from 'node-watch';
import {spawn} from 'child_process';
import c from '../config/config';
import { addLogRow, timeout, getClassStr } from './utils';
import initState, {dispatch, setState, getState} from './store';
import a from './actions';
import request from 'request';
import { StringDecoder } from 'string_decoder';

// const port = process.env.PORT || 8081;
const port = 8081;
const app = express();
const server = http.Server(app);
const io = socketio(server);
let subprocess = null;
let initStore = initState;

const textStream = fs.createWriteStream(c["textLogPath"], {flags: 'a'});
const htmlStream = fs.createWriteStream(c["htmlLogPath"], {flags: 'a'});

app.use('/statics', express.static(__dirname +  '/statics'));
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});


// let obj = fs.readFile('train/Ostre1_165.mat', (err, data) => {
//   console.log(data.toString())
// })

// jbinary.load('train/Ostre1_165.mat', MAT).then(binary => {
//   let mat = binary.read('mat');
//   console.log(mat);
// })



addLogRow()("Setting up server");
io.on('connection', socket => {
  const addLog = addLogRow(io);

  dispatch(
    "init_machine_state",
    subprocess !== null && subprocess !== undefined ? "running" : "stopped"
  );

  addLogRow()("New connection");
  socket.emit('connected', {
    state: getState(),
    log: fs.readFileSync(c["htmlLogPath"], "utf-8")
  });

  socket.on("diconnect", () => {
    addLog("Diconnected");
  })

  socket.on('start_machine', () => {
    addLog("Starting machine...", 'yellow');

    (async () => {
      await timeout(2000);
      subprocess = spawn('python', [c["rootFolder"] + 'machine.py'], {detached: true});
      console.log(c["rootFolder"] + 'machine.py');
      subprocess.unref();
      addLog(`Subprocess ID: ${subprocess.pid}`);
      io.sockets.emit('start_machine_success');
      addLog("Machine started!", 'green');

      // await timeout(2000);
      // dispatch('set_sharp_tool', io.sockets);
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
  });

  watch(__dirname + "/../tmp_files", (evt, name) => {
    if(evt === "update") {
      addLog('New file: ');
      addLog(name, 'yellow', true);

      const proc = spawn("python3", [c["rootFolder"] + "features.py", "train/Ostre1_165.mat"]);
      var decoder = new StringDecoder('utf8');
      proc.stdout.on('data', async(data) => {
        const _data = await decoder.write(data);
        const __data = JSON.parse(_data)
        console.log(__data)
        // const _data = data.toString();
        const cl = __data.class;
        request.post("http://localhost:8080", {json: __data}, (err, response) => {
          addLog("Real Class: ");
          addLog(cl, null, true);
          addLog(". Predicted class: ", null, true);
          addLog(response.body, null, true);
          if(response.body === "0")
            io.sockets.emit("sharp_tool");
          else if(response.body === "1")
            io.sockets.emit("blunt_tool");
        });
      });

    }
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
