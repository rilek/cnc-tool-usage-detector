import { registerAction, setState } from './store';
import {addLogRow} from './utils';

registerAction("set_sharp_tool", (state, sockets) => {
  setState({'tool_state': 0});
  sockets.emit('sharp_tool');
  addLogRow(sockets)("Tool state: ");
  addLogRow(sockets)("Sharp", "green", true);
});

registerAction("set_blunt_tool", (state, sockets) => {
  setState({'tool_state': 1});
  sockets.emit('blunt_tool');
  addLogRow(sockets)("Tool state: ");
  addLogRow(sockets)("Blunt", "red", true);
});

registerAction("init_machine_state", (state, machine_state) => {
  setState({'machine_state': machine_state});
});

export default {}
