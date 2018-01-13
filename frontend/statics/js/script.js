store = Store();
store.initReactors(
  machineStateReactor(),
  toolStateReactor()
);

store.registerAction("new_state", function(state) {
  store.setState(state);
});

store.registerAction("change_tool_state", function(x) {
  store.setState({tool_state: x});
});

store.registerAction("change_machine_state", function(x) {
  store.setState({machine_state: x});
});

store.registerAction("start_machine", function() {
  socket.emit('start_machine');
  store.setState({machine_state: "waiting"})
});

store.registerAction("stop_machine", function() {
  socket.emit('stop_machine');
  store.setState({machine_state: "waiting"});
});

store.registerAction("toggle_machine_state", function() {
  machine_state = store.getState("machine_state");
  if(machine_state === "running"){
      store.dispatch("stop_machine");
    } else if(machine_state === "stopped") {
      store.dispatch("start_machine");
    }
})

$(document).ready(function () {
  u = Utilities();

  u.addLogRow(" ==================== New Session ==================== ");
  socket = initSockets(u);
  initEventListeners(u, socket);
});



function initSockets(u) {
  var socket = io.connect('http://' + document.domain + ':' + location.port);

  socket.on('connect', function () {
    console.log("connected!");
    u.addLogRow(u.setColor("Connected to server!", "green"));
  });

  socket.on('connected', function(data) {
    store.dispatch("new_state",data);
  });

  socket.on('disconnect', function () {
    u.addLogRow(u.setColor('Disconnected', "red"));
    store.dispatch("change_machine_state", "stopped");
    store.dispatch("change_tool_state", -1)
  });

  socket.on('tmp_file_change', function () {
    u.addLogRow(u.setColor('Changed file', "yellow"));
  });

  socket.on('reload', function() {
    location.reload();
  });

  socket.on('start_machine_success', function() {
    u.addLogRow(u.setColor("Machine started!", "green"));
    store.dispatch("change_machine_state", "running");
  });

  socket.on('start_machine_fail', function() {
    u.addLogRow(u.setColor("Machine failed to start!", "red"));
    store.dispatch("change_machine_state", "stopped");
  });

  socket.on('stop_machine_success', function() {
    u.addLogRow(u.setColor("Machine stopped!", "green"));
    store.dispatch("change_machine_state", "stopped");
    store.dispatch("change_tool_state", -1);
  });

  socket.on('stop_machine_fail', function() {
    u.addLogRow(u.setColor("Machine failed to stop!", "red"));
    store.dispatch("change_machine_state", "running");
  });

  socket.on('sharp_tool', function() {
    store.dispatch("change_tool_state", 0);
  });

  socket.on('blunt_tool', function() {
    store.dispatch("change_tool_state", 1);
  });


  return socket;
}



function initEventListeners(u, socket) {

  $(".power-button").on('click', function () {
    store.dispatch("toggle_machine_state")
  });

  $('#test').on("click", function() {
    u.addLogRow("dupa");
  });

  $('#clear-log').on('click', function() {
    $('#log').text('');
    localStorage.setItem("log", "");
  });
}



function Store() {
  var state = {
    machine_state: "stopped",
    tool_state: -1,
    buffer_state: 0
  };
  var reactors = {};
  var actions = {};
  var setState = function(data) {
    Object.assign(state, data);
  };
  var getState = function(prop) {
    return prop !== undefined ? state[prop] : state;
  };

  watch(state, function(prop, action, newval, oldval) {
    if(oldval !== newval) {
      _reactors = reactors[prop];
      if(Array.isArray(_reactors))
        _reactors.forEach(function(fn) {
          fn(prop,action,newval, oldval);
        });
    }
  });


  var registerAction = function(name, action) {
    Object.assign(actions, {[name]: action});
  }

  var dispatch = function(name, ...args) {
    actions[name](...args);
  }

  var initReactors = function(...args) {
    args.forEach(function([name, fn]) {
      if(reactors[name] === undefined)
        reactors[name] = [];
      reactors[name].push(fn);
    });
  };

  return {
    setState: setState,
    getState: getState,
    dispatch: dispatch,
    registerAction: registerAction,
    initReactors: initReactors
  };
}

function machineStateReactor() {
  return [
    'machine_state',
    function(prop, action, newval, oldval) {
      if(newval === "running") {
        $(".power-button").addClass("on").removeClass("loading");
        $('.machine-state-text').text("Wyłącz")
      } else if (newval === "stopped") {
        $(".power-button").removeClass("on").removeClass("loading");
        $('.machine-state-text').text("Włącz")
      } else if (newval === "waiting") {
        $(".power-button").removeClass("on").addClass("loading");
        if(oldval === "running") {
          u.addLogRow(u.setColor("Stopping machine...", "yellow"));
        } else if (oldval === "stopped") {
          u.addLogRow(u.setColor("Setting up machine...", "yellow"));
        }
      }
    }
  ];
}

function toolStateReactor() {
  return [
    'tool_state',
    function(prop, action, newval, oldval) {
      u.addLogRow("Changed tool state! New state: ");
      if(newval === 1) {
        u.addLogRow(u.setColor("Blunt", "red"), true);
        $('.tool-status').removeClass("sharp").addClass("blunt");
        $('.tool-status i').removeClass().addClass("far fa-times-circle");
        $('.tool-state-text').text("Tępe");
      } else if (newval === 0) {
        u.addLogRow(u.setColor("Sharp", "green"), true);
        $('.tool-status i').removeClass().addClass("far fa-check-circle");
        $('.tool-status').removeClass("blunt").addClass("sharp");
        $('.tool-state-text').text("Ostre");
      } else if (newval === -1) {
        u.addLogRow("N/A", true);
        $('.tool-status i').removeClass().addClass("far fa-question-circle");
        $('.tool-status').removeClass("blunt sharp");
        $('.tool-state-text').text("N/A");
      }
    }
  ];
}




function Utilities() {
  var setColor = function (){
    var colors = {
      green: "green",
      red: "red",
      gray: "gray",
      blue: "blue",
      yellow: "rgb(214, 193, 49)"
    };

    return function(text, color) {
      return '<span style="color: ' + colors[color] + '">' + text + '</span>';
    }}();

  var addLogRow = function() {
    var $log = $('#log');
    $log.html(localStorage.getItem("log"));

    return function(text, omitLine) {
      var timestamp = omitLine !== true ? "[" + new Date().toISOString() + "]: " : "";
      var linebreak = omitLine !== true ? "<br/>" : "";

      $log.append(linebreak, setColor(timestamp, "gray"), text);
      $log.scrollTop($log[0].scrollHeight);
      localStorage.setItem("log", $log.html());
      return true;
    }
  };

  return {
    setColor: setColor,
    addLogRow: addLogRow()
  };
}
