var dbUtils  = require("./dbUtils");

function sendJSONResp (res, value) {

  res.set('Content-Type', 'application/json')
     .set('Access-Control-Allow-Origin', "*")
     .send(JSON.stringify(value));
}

function sendErrResp (res, message, code) {

  code = code || 402;

  res.status(code)
     .send(message);
}

function getRoviIdsCtrlr(req, res) {

  var contentId = req.query.contentId;

  if (!contentId) {

    sendErrResp(res, "Invalid content id", 404);
    return;
  }

  var query = "select fd from rovi_fd_new where rovi_content_id="+contentId;

  dbUtils.makeQuery(query).done(function (resp){

    var roviIdRe = /rovi_id_2\.0#([^\<]+)\<?/g,
        roviIds = [];

    if (resp.length > 0) {

      resp = resp[0].fd;

      var matchArr = [];

      while ((matchArr = roviIdRe.exec(resp)) !== null) {

        roviIds.push(matchArr[1]);
      }

      resp = roviIds;
    }

    sendJSONResp(res, resp);
  }).fail(function () {

    sendErrResp(res, "Error occured while querying DB");
  });
}

function getRoviGroupIdCtrlr (req, res) {

  var contentId = req.query.contentId;

  if (!contentId) {

    sendErrResp(res, "Invalid content id", 404);
    return;
  }

  var query = "select group_id from rovi_fd_new where rovi_content_id="+contentId;

  dbUtils.makeQuery(query).done(function (resp) {

    var groupId = null;

    if (resp.length > 0) {

      groupId = resp[0].group_id;
    }

    sendJSONResp(res, {"result": groupId});
  }).fail(function () {

    sendErrResp(res, "Error occured while querying DB");
  });
}

module.exports = {"getRoviIdsCtrlr": getRoviIdsCtrlr,
                  "getRoviGroupIdCtrlr": getRoviGroupIdCtrlr};
