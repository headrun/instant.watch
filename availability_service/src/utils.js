function getCtrlr (deferredFunc) {

  function ctrlr (req, res) {

    // Response to be served
    var resp = {},
        d1 = new Date();

    deferredFunc(req).done(function (data) {

        // Make the response the result
        resp = data;
    }).fail(function (error) {

        // Make the response the error
        resp = {"status": 500, "error": error};
    }).always(function () {

        d2 = new Date();

        resp.timeTook = (d2 - d1);

        // Serve the response
        res.send(JSON.stringify(resp));
    });
  }

  return ctrlr;
}
