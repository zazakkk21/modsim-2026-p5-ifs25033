const axios = require("axios");

async function callAxios(method, url) {
  try {
    const response = await axios({
      method: method,
      url: url
    });
    return response;
  } catch (error) {
    return error.response;
  }
}

module.exports = { callAxios };