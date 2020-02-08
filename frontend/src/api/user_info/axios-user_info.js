import axios from "axios";
import store from "../../store";
import { APIUrl } from "../axios-base";
import user_info from "../../store/modules/user_info/user_info";

const getAPI_user_info = axios.create({
  baseURL: APIUrl
});

// Когда протухает refresh_token нам не нужно делать повторный запрос через interceptors !!!
// Мы редиректим на страницу logout чтоб сбросить все token'ы !!!

getAPI_user_info.interceptors.response.use(undefined, function(err) {
  // if error response status is 401, it means the request was invalid due to expired access token
  if (err.config && err.response && err.response.status === 401) {
    // console.log(err.config);
    // console.log([...pr.entries()]);
    store
      .dispatch("refreshToken") // attempt to obtain new access token by running 'refreshToken' action
      .then(access => {
        // console.log(access);
        // if successful re-send the request to get the data from server
        axios
          .request({
            baseURL: APIUrl,
            method: "post",
            data: err.config.data,
            headers: {
              Authorization: `Bearer ${access}`
            }, // the new access token is attached to the authorization header
            url: err.config.url
          })
          // .post(APIUrl + err.config.url, err.config.data, {
          //   headers: { Authorization: `Bearer ${access}` }
          // })
          .then(response => {
            // if successfully received the data store it in store.state.APIData so that 'Downloads' component can grab the
            // data from it and display to the client.
            // console.log(
            //   "[axios-user_info] Success getting the getAPI_user_info"
            // );
            const data = response.data[0];
            user_info.state.USER_INFO_DATA = data;
          })
          .catch(err => {
            // console.log(
            //   "[axios-user_info] Got the new access token but error while trying to fetch data from the API using it"
            // );
            return Promise.reject(err);
          });
      })
      .catch(err => {
        // console.log("[axios-user_info] catch err");
        return Promise.reject(err);
      });
  }
});

export { getAPI_user_info };
