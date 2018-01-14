

var store = Store();
store.initReactors(
  machineStateReactor(),
  toolStateReactor()
);

var ssocket = $.Deferred();


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
  // store.setState({machine_state: "waiting"})
});

store.registerAction("stop_machine", function() {
  socket.emit('stop_machine');
  // store.setState({machine_state: "waiting"});
});

store.registerAction("toggle_machine_state", function() {
  machine_state = store.getState("machine_state");
  if(machine_state === "running")
    store.dispatch("stop_machine");
  else if(machine_state === "stopped")
    store.dispatch("start_machine");
});

store.registerAction("log_history", function(logs) {
  var $log = $('#log');
  $log.html(logs + $log.html());
  $log.scrollTop($log[0].scrollHeight);
});

store.registerAction("clear_logs", function() {
  $('#log').html("");
  socket.emit("clear_logs");
});

store.registerAction("add_log_row", function(rawText, color, omitLine) {
  ssocket.promise().then(function(socket) {
    socket.emit("add_log_row", rawText, color, omitLine);
  })
});


$(document).ready(function () {
  u = Utilities();

  // u.addLogRow("==================== New Session ====================");
  socket = initSockets(u);
  initEventListeners(u, socket);
});



function initSockets(u) {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  ssocket.resolve(socket);

  socket.on('connect', function () {
    console.log("connected!");
    // u.addLogRow("Client connected to server!", "green");
  });

  socket.on('connected', function(data) {
    store.dispatch("new_state", data.state);
    store.dispatch("log_history", data.log);
  });

  socket.on('disconnect', function () {
    // u.addLogRow('Client disconnected from server', "red");
    store.dispatch("change_machine_state", "stopped");
    store.dispatch("change_tool_state", -1)
  });

  socket.on('tmp_file_change', function (name) {
  });

  socket.on('reload', function() {
    location.reload();
  });

  socket.on('new_log', function(log) {
    $log = $('#log');
    $log.append(log);
    $log.scrollTop($log[0].scrollHeight);
  });

  socket.on('start_machine_success', function() {
    store.dispatch("change_machine_state", "running");
  });

  socket.on('start_machine_fail', function() {
    // u.addLogRow("Machine failed to start!", "red");
    store.dispatch("change_machine_state", "stopped");
  });

  socket.on('stop_machine_success', function() {
    store.dispatch("change_machine_state", "stopped");
    store.dispatch("change_tool_state", -1);
  });

  socket.on('stop_machine_fail', function() {
    // u.addLogRow("Machine failed to stop!", "red");
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
    store.dispatch("toggle_machine_state");
  });

  $('#test').on("click", function() {
    // u.addLogRow("dupa");
  });

  $('#clear-log').on('click', function() {
    store.dispatch("clear_logs");
  });
}



function Store() {
  var state = {
    machine_state: null,
    tool_state: null,
    buffer_state: null
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
      var _reactors = reactors[prop];
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

      switch(newval) {
        case "running":
          $(".power-button").addClass("on").removeClass("loading");
          $('.machine-state-text').text("Wyłącz");
          break;

        case "stopped":
          $(".power-button").removeClass("on").removeClass("loading");
          $('.machine-state-text').text("Włącz");
          break;

        case "waiting":
          $(".power-button").removeClass("on").addClass("loading");
          break;
      }
    }
  ];
}


function toolStateReactor() {
  return [
    'tool_state',
    function(prop, action, newval, oldval) {
      // u.addLogRow("Changed tool state! New state: ");

      switch(newval) {
        case 1:
          // u.addLogRow("Blunt", "red", true);
          $('.tool-status').removeClass("sharp").addClass("blunt");
          $('.tool-status i').removeClass().addClass("far fa-times-circle");
          $('.tool-state-text').text("Tępe");
          break;

        case 0:
          // u.addLogRow("Sharp", "green", true);
          $('.tool-status i').removeClass().addClass("far fa-check-circle");
          $('.tool-status').removeClass("blunt").addClass("sharp");
          $('.tool-state-text').text("Ostre");
          break;

        case -1:
          // u.addLogRow("N/A", "gray", true);
          $('.tool-status i').removeClass().addClass("far fa-question-circle");
          $('.tool-status').removeClass("blunt sharp");
          $('.tool-state-text').text("N/A");
          break;
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

    return function(rawText, color, omitLine) {
      var $log = $('#log');
      var timestamp = omitLine !== true ? "[" + new Date().toISOString() + "]: " : "";
      var linebreak = omitLine !== true ? "\r\n" : "";
      var coloredText = typeof color !== 'undefined' && color !== null ? setColor(rawText, color) : rawText;
      var logRow = linebreak + (timestamp ? setColor(timestamp, "gray") : coloredText);


      $log.append(logRow);
      $log.scrollTop($log[0].scrollHeight);
      store.dispatch("add_log_row", rawText, color, omitLine);
      return true;
    }
  };

  return {
    setColor: setColor,
    addLogRow: addLogRow()
  };
}
