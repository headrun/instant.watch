var express = require("express"),
    app     = express(),
    routes  = require("./routes");

var devPort = process.argv[2] || 8000;

/* Registering Routes */
for (var index in routes.routes) {

  var route  = routes.routes[index],
      method = route.length > 2? route.pop(): "get";

  app[method].apply(app, route);
}

app.use(routes.handle404);

var port = process.env.NODE_ENV == "production"? process.env.PORT: devPort;

app.listen(port, function () {

             console.log("Express running on port " + port);
           });
