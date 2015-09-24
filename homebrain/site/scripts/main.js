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
});

app.controller("AgentsCtrl", function($scope, $resource, $routeParams) {
    var Agents = $resource("/api/v0/agents");
    Agents.get("", function(agents){
        console.log(agents)
        $scope.agents = agents;
    })
});
