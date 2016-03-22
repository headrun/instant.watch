var mysql    = require("mysql"),
    utils    = require("./utils"),
    Deferred = require("deferred-js");

var pool  = mysql.createPool({

  connectionLimit : 10,
  host            : "host",
  user            : "username",
  password        : "password",
  database        : "DBName"
});

function releaseConnAndReject (connection, error, d) {

  if (connection) {

    connection.release();
  }

  d.reject(error);
}

function makeQuery(query, customPool) {

  var d = new Deferred();

  if (!query || typeof query !== "string") {

    return releaseConnAndReject(connection,
                                new Error("Invalid Query"),
                                d);
  }

  customPool = customPool || pool;

  customPool.getConnection(function (error, connection) {

    if (error) {

      return releaseConnAndReject(connection, error, d);
    }

    connection.query(query, function (error, results) {

      if (error) {

        return releaseConnAndReject(connection, error, d);
      }

      connection.release();

      d.resolve(results);
    });
  });

  return d.promise();
}

module.exports = {"makeQuery": makeQuery};
