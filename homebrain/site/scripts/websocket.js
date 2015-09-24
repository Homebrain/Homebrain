var wsSocket = new WebSocket("ws://127.0.0.1:9091");

wsSocket.onopen = function (event) {
  //exampleSocket.send("Here's some text that the server is urgently awaiting!");
  msg1 = {"type": "log", "data": {"level": "info", "msg": "Hello Homebrain! I am a WebUI log websocket!"}};
  wsSocket.send(JSON.stringify(msg1));
  msg2 = {"type": "subscribe", "data": "log"};
  wsSocket.send(JSON.stringify(msg2));
};

wsSocket.onmessage = function (eventObj) {
    var event = JSON.parse(eventObj.data)
    insertLogEvent(event);
}

function insertLogEvent(event){
    table = document.getElementById('logtable');
    row = table.insertRow(-1);
    row.insertCell(0).innerHTML = event["data"]["level"];
    row.insertCell(1).innerHTML = event["data"]["msg"];
    // Scroll to bottom
    logbody = document.getElementById('logbody')
    logbody.scrollTop = logbody.scrollHeight;
}
