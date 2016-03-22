var query = require("./src/query");

/* Routes */
var routes = [

  ["/getroviids", query.getRoviIdsCtrlr],
  ["/rovi_group_id", query.getRoviGroupIdCtrlr],
];

res404 = "Oops!, 404 Not found\n\n" +
         "You can try the following URLS:\n";

for (var index in routes) {

  var route = routes[index],
      method = route[2]?route[2]:"get";

  res404 += method.toUpperCase() + " " + route[0] + "\n";
}

function handle404 (req, res) {

  res.append("Content-Type", "text/plain");
  res.status(404).send(res404);
}

module.exports = {"routes": routes,
                  "handle404": handle404};

