import axios from "axios";
import store from "../../store";
import { APIUrl } from "../axios-base";
import mortgages from "../../store/modules/mortgages/mortgages";

const getAPI = axios.create({
  baseURL: APIUrl
});
const getBANKS = axios.create({
  baseURL: APIUrl
});
const get_TARGET_CREDITS = axios.create({
  baseURL: APIUrl
});
const editBANKS = axios.create({
  baseURL: APIUrl
});

// [Список ипотечных программ]
// Если response пришел с ошибкой то обновляем token и заапрашиваем данные снова
getAPI.interceptors.response.use(undefined, function(err) {
  // if error response status is 401, it means the request was invalid due to expired access token
  if (err.config && err.response && err.response.status === 401) {
    // const pr = err.config.params;
    // console.log([...pr.entries()]);
    store
      .dispatch("refreshToken") // attempt to obtain new access token by running 'refreshToken' action
      .then(access => {
        // if successful re-send the request to get the data from server
        axios
          .request({
            baseURL: APIUrl,
            method: "get",
            headers: { Authorization: `Bearer ${access}` }, // the new access token is attached to the authorization header
            url: "/api/v1/mortgages/all/",
            params: err.config.params // параметры урла с которого пришла ошибка
          })
          .then(response => {
            // if successfully received the data store it in store.state.APIData so that 'Downloads' component can grab the
            // data from it and display to the client.
            // console.log("[axios-mortgages] Success getting the mortgages");
            // console.log(response.data.results);
            mortgages.state.MORTGAGES_DATA = response.data.results;
          })
          .catch(err => {
            // console.log(
            //   "[axios-mortgages] Got the new access token but error while trying to fetch data from the API using it"
            // );
            return Promise.reject(err);
          });
      })
      .catch(err => {
        // console.log("[axios-mortgages] catch err");
        return Promise.reject(err);
      });
  }
});

getBANKS.interceptors.response.use(undefined, function(err) {
  // if error response status is 401, it means the request was invalid due to expired access token
  if (err.config && err.response && err.response.status === 401) {
    store
      .dispatch("refreshToken") // attempt to obtain new access token by running 'refreshToken' action
      .then(access => {
        // if successful re-send the request to get the data from server
        axios
          .request({
            baseURL: APIUrl,
            method: "get",
            headers: { Authorization: `Bearer ${access}` }, // the new access token is attached to the authorization header
            url: "/api/v1/mortgages/banks/"
          })
          .then(response => {
            // if successfully received the data store it in store.state.APIData so that 'Downloads' component can grab the
            // data from it and display to the client.
            // console.log("[axios-mortgages] Success getting the getBANKS");
            // console.log(response.data);
            const names_banks = response.data.reduce((total, item) => {
              total.push(item.bank_name);
              return total;
            }, []);
            mortgages.state.BANKS_NAME_DATA = names_banks;
            mortgages.state.BANKS_ALL_DATA = response.data;
          })
          .catch(err => {
            // console.log(
            //   "[axios-mortgages] Got the new access token but error while trying to fetch data from the API using it"
            // );
            return Promise.reject(err);
          });
      })
      .catch(err => {
        // console.log("[axios-mortgages] catch err getBANKS");
        return Promise.reject(err);
      });
  }
});

get_TARGET_CREDITS.interceptors.response.use(undefined, function(err) {
  // if error response status is 401, it means the request was invalid due to expired access token
  if (err.config && err.response && err.response.status === 401) {
    store
      .dispatch("refreshToken") // attempt to obtain new access token by running 'refreshToken' action
      .then(access => {
        // if successful re-send the request to get the data from server
        axios
          .request({
            baseURL: APIUrl,
            method: "get",
            headers: { Authorization: `Bearer ${access}` }, // the new access token is attached to the authorization header
            url: "/api/v1/mortgages/target-credits/"
          })
          .then(response => {
            // if successfully received the data store it in store.state.APIData so that 'Downloads' component can grab the
            // data from it and display to the client.
            // console.log("Success getting the get_TARGET_CREDITS");
            const names_target_credits = response.data.reduce((total, item) => {
              total.push(item.target_name);
              return total;
            }, []);
            mortgages.state.TARGET_CREDITS_NAME_DATA = names_target_credits;
            mortgages.state.TARGET_CREDITS_ALL_DATA = response.data;
          })
          .catch(err => {
            // console.log(
            //   "[axios-mortgages] Got the new access token but error while trying to fetch data from the API using it"
            // );
            return Promise.reject(err);
          });
      })
      .catch(err => {
        // console.log("[axios-mortgages] catch err get_TARGET_CREDITS");
        return Promise.reject(err);
      });
  }
});

// editBANKS.interceptors.response.use(
//   function(response) {
//     console.log(response);
//     return response;
//   },
//   function(err) {
//     // if error response status is 401, it means the request was invalid due to expired access token
//     if (err.config && err.response && err.response.status === 401) {
//       store
//         .dispatch("refreshToken") // attempt to obtain new access token by running 'refreshToken' action
//         // eslint-disable-next-line no-unused-vars
//         .then(access => {
//           // if successful re-send the request to get the data from server
//           axios
//             .request({
//               baseURL: APIUrl,
//               method: "patch",
//               data: err.config.data,
//               headers: {
//                 "Content-Type": "multipart/form-data",
//                 Authorization: `Bearer ${access}`
//               }, // the new access token is attached to the authorization header
//               url: err.config.url
//             })
//             // eslint-disable-next-line no-unused-vars
//             .then(response => {
//               // if successfully received the data store it in store.state.APIData so that 'Downloads' component can grab the
//               // data from it and display to the client.
//               console.log("(axios-mortgages) Success getting the editBANKS");
//               // mortgages.state.BANKS_NAME_DATA = response.data;
//               console.log(response);
//               // return Promise.resolve(response);
//             })
//             .catch(err => {
//               console.log(
//                 "[axios-mortgages] Got the new access token but error while trying to fetch data from the API using it"
//               );
//               return Promise.reject(err);
//             });
//           // console.log(err.config);
//         })
//         .catch(err => {
//           console.log("[axios-mortgages] catch err editBANKS");
//           return Promise.reject(err);
//         });
//     }
//   }
// );

export { getAPI, getBANKS, get_TARGET_CREDITS, editBANKS };
