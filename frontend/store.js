
let state = {
  machine_state: "stopped",
  tool_state: -1,
  buffer_state: 0
};

let actions = {};
let reactors = {};


const setState = (data) => {
  Object.assign(state, data);
};

const getState = (prop) => {
  return prop !== undefined ? state[prop] : state;
};

const dispatch = function(name, ...args) {
  if(actions[name])
    return actions[name](state, ...args);
  else
    return false;
};

const registerAction = function(name, action) {
  Object.assign(actions, {[name]: action});
}

const initReactors = function(...args) {
  args.forEach(function([name, fn]) {
    if(reactors[name] === undefined)
      reactors[name] = [];
    reactors[name].push(fn);
  });
};


export default state;
export {
  setState,
  getState,
  dispatch,
  registerAction,
  initReactors
};
