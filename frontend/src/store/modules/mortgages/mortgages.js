import store from "@/store";
import { getAPI, getBANKS } from "@/api/mortgages/axios-mortgages";

const mortgagesModule = {
  namespaced: true,
  state: {
    BANKS_DATA: null,
    MORTGAGES_DATA: null,
    TARGET_CREDITS_DATA: null
  },
  getters: {},
  mutations: {
    SET_UPDATE_BANKS_DATA(state, data) {
      state.BANKS_DATA = data;
    },
    SET_UPDATE_TARGET_CREDITS_DATA(state, data) {
      state.TARGET_CREDITS_DATA = data;
    },
    SET_UPDATE_MORTGAGES_DATA(state, data) {
      state.MORTGAGES_DATA = data;
    },
    destroy_MORTGAGES_DATA(state) {
      state.MORTGAGES_DATA = null;
    }
  },
  actions: {
    FETCH_MORTGAGES(context, params) {
      // console.log(url);
      return new Promise((resolve, reject) => {
        getAPI
          .get("api/v1/mortgages/all/", {
            headers: {
              Authorization: `Bearer ${store.state.accessToken}`
            },
            params: params
          }) // proof that your access token is still valid; if not the
          // axios getAPI response interceptor will attempt to get a new  access token from the server. check out ../api/axios-base.js getAPI instance response interceptor
          .then(response => {
            // console.log("GetAPI successfully got the mods");
            // console.log(response);
            context.commit("SET_UPDATE_MORTGAGES_DATA", response.data.results); // store the response data in store
            resolve(response);
          })
          .catch(err => {
            // refresh token expired or some other error status
            // eslint-disable-next-line no-unused-vars
            const er = err; // просто чтоб ошибку в консоли не показывало
            // console.log(err);
            console.log("[mortgages] Не получилось");
            reject(err);
          });
      });
    },
    FETCH_BANKS(context) {
      return new Promise((resolve, reject) => {
        getBANKS
          .get("api/v1/mortgages/banks/", {
            headers: {
              Authorization: `Bearer ${store.state.accessToken}`
            }
          }) // proof that your access token is still valid; if not the
          // axios getAPI response interceptor will attempt to get a new  access token from the server. check out ../api/axios-base.js getAPI instance response interceptor
          .then(response => {
            // console.log("GetAPI successfully got the mods");
            // console.log(response);
            const names_banks = response.data.reduce((total, item) => {
              total.push(item.bank_name);
              return total;
            }, []);
            context.commit("SET_UPDATE_BANKS_DATA", names_banks); // store the response data in store
            resolve(response);
          })
          .catch(err => {
            // refresh token expired or some other error status
            // eslint-disable-next-line no-unused-vars
            const er = err; // просто чтоб ошибку в консоли не показывало
            // console.log(err);
            console.log("[FETCH_BANKS] Не получилось");
            reject(err);
          });
      });
    },
    FETCH_TARGET_CREDITS(context) {
      return new Promise((resolve, reject) => {
        getBANKS
          .get("api/v1/mortgages/target-credits/", {
            headers: {
              Authorization: `Bearer ${store.state.accessToken}`
            }
          }) // proof that your access token is still valid; if not the
          // axios getAPI response interceptor will attempt to get a new  access token from the server. check out ../api/axios-base.js getAPI instance response interceptor
          .then(response => {
            // console.log("GetAPI successfully got the mods");
            // console.log(response);
            const names_target_credits = response.data.reduce((total, item) => {
              total.push(item.target_name);
              return total;
            }, []);
            context.commit(
              "SET_UPDATE_TARGET_CREDITS_DATA",
              names_target_credits
            ); // store the response data in store
            resolve(response);
          })
          .catch(err => {
            // refresh token expired or some other error status
            // eslint-disable-next-line no-unused-vars
            const er = err; // просто чтоб ошибку в консоли не показывало
            // console.log(err);
            console.log("[FETCH_TARGET_CREDITS] Не получилось");
            reject(err);
          });
      });
    }
  }
};

export default mortgagesModule;
