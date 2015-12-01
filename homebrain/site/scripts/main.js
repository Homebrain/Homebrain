app = angular.module('HomeBrain', ["ngResource", "ngRoute"]);


app.config(function($routeProvider, $locationProvider) {
    $routeProvider.when("/", {
        templateUrl: "templates/dashboard.html",
        controller: "HomeCtrl"
    });

    $routeProvider.when("/nodes", {
        templateUrl: "templates/nodes.html",
        controller: "NodesCtrl"
    });

    $routeProvider.when("/nodes/:id", {
        templateUrl: "templates/node.html",
        controller: "NodeCtrl"
    });

    $routeProvider.when("/agents", {
        templateUrl: "templates/agents.html",
        controller: "AgentsCtrl"
    });

    $routeProvider.when("/agents/:id", {
        templateUrl: "templates/agent.html",
        controller: "AgentCtrl"
    });

    $locationProvider.html5Mode(true);
});

app.controller("MainCtrl", function($scope, $route, $routeParams, $location) {
    $scope.$route = $route;
    $scope.$routeParams = $routeParams;
    $scope.$location = $location;
});

app.controller("LogWindowCtrl", function($scope, $route, $routeParams, $location) {
    $scope.$route = $route;
    $scope.$routeParams = $routeParams;
    $scope.$location = $location;
    $scope.messages = [];
    $scope.showLog = false;

    var wsSocket = new WebSocket("ws://127.0.0.1:20445");

    wsSocket.onopen = function (event) {
        console.info("Websocket opened!");
        msg1 = {"type": "log", "data": {"level": "info", "msg": "Hello Homebrain! I am a WebUI log websocket!"}};
        wsSocket.send(JSON.stringify(msg1));
        msg2 = {"type": "subscribe", "data": "log"};
        wsSocket.send(JSON.stringify(msg2));
    };

    wsSocket.onclose = function (eventObj) {
        console.warn("Connection to websocket lost");
        var event = {"data": {"level": "warning", "msg": "Disconnected from websocket"}};
        insertLogEvent(event);
    };

    wsSocket.onmessage = function (eventObj) {
        var event = JSON.parse(eventObj.data);
        insertLogEvent(event);
    };

    /**
     * Events should follow the format
     *   {"data": {"level": (one in ["info", "warning", "error"]),
     *             "msg": "message to log")}}
     * Add timestamps later!
     */
    function insertLogEvent(event){
        // TODO: Move logic to AngularJS controller
        $scope.messages.push(event["data"]);
        // Scroll to bottom
        var logbody = document.getElementById('logbody');
        logbody.scrollTop = logbody.scrollHeight;
    }
});

app.controller("HomeCtrl", function($scope, $resource) {
    var Agents = $resource("/api/v0/agents");
    Agents.get("", function(agents){
        $scope.agents = agents;
        $scope.agentsenabled = Object.keys($scope.agents).length-2;
        // Get running agents count
        var c = 0
        for (node in $scope.agents) {
            if ($scope.agents[node].status == "True")
                c++;
        }
        $scope.agentsrunning = c;
    });
    var Nodes = $resource("/api/v0/nodes");
    Nodes.get("", function(nodes){
        $scope.nodes = nodes;
        $scope.nodec = Object.keys($scope.nodes).length-2;
    });
});

function capitalize(s) {
    return s.substr(0, 1).toUpperCase() + s.substr(1);
}

app.controller("BreadcrumbCtrl", function($scope, $location) {
});

app.controller("AgentListCtrl", function($scope, $resource, $routeParams) {
});

app.controller("NodesCtrl", function($scope, $resource, $routeParams) {
    var Nodes = $resource("/api/v0/nodes");
    Nodes.get("", function(nodes){
        console.log(nodes)
        $scope.nodes = nodes;
    })
});

app.controller("NodeCtrl", function($scope, $resource, $routeParams) {
    var Node = $resource("/api/v0/nodes/"+$routeParams.id);

    console.log($routeParams)
    Node.get("", function(node){
        console.log(node)
        $scope.node = node;
    })
});

app.controller("AgentCtrl", function($scope, $resource, $routeParams) {
    var Agents = $resource("/api/v0/agents");
    Agents.get("", function(agents){
        agent = agents[$routeParams.id];
        console.log(agent);
        $scope.agent = agent;
    })
});

app.controller("AgentsCtrl", function($scope, $resource, $routeParams) {
    var Agents = $resource("/api/v0/agents");
    Agents.get("", function(agents){
        console.log(agents)
        $scope.agents = agents;
    })
});
