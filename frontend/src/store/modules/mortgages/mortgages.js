import store from "@/store";
import {
  getAPI,
  getBANKS,
  get_TARGET_CREDITS,
  crudBANKS,
  crudTargetCredits,
  crudMortgageProgramm
} from "@/api/mortgages/axios-mortgages";

const mortgagesModule = {
  namespaced: true,
  state: {
    BANKS_NAME_DATA: null,
    BANKS_ALL_DATA: null,
    MORTGAGES_DATA: null,
    TARGET_CREDITS_NAME_DATA: null,
    TARGET_CREDITS_ALL_DATA: null
  },
  getters: {
    GET_BANKS_ALL_DATA: state => {
      return state.BANKS_ALL_DATA;
    },
    GET_TARGET_CREDITS_ALL_DATA: state => {
      return state.TARGET_CREDITS_ALL_DATA;
    },
    GET_MORTGAGES_DATA: state => {
      return state.MORTGAGES_DATA;
    }
  },
  mutations: {
    SET_UPDATE_BANKS_NAME_DATA(state, data) {
      state.BANKS_NAME_DATA = data;
    },
    SET_UPDATE_BANKS_ALL_DATA(state, data) {
      state.BANKS_ALL_DATA = data;
    },
    SET_UPDATE_TARGET_CREDITS_NAME_DATA(state, data) {
      state.TARGET_CREDITS_NAME_DATA = data;
    },
    SET_UPDATE_TARGET_CREDITS_ALL_DATA(state, data) {
      state.TARGET_CREDITS_ALL_DATA = data;
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
            // console.log("[mortgages] Не получилось");
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
            context.commit("SET_UPDATE_BANKS_NAME_DATA", names_banks); // store the response data in store
            context.commit("SET_UPDATE_BANKS_ALL_DATA", response.data);
            resolve(response);
          })
          .catch(err => {
            // refresh token expired or some other error status
            // eslint-disable-next-line no-unused-vars
            const er = err; // просто чтоб ошибку в консоли не показывало
            // console.log(err);
            // console.log("[FETCH_BANKS] Не получилось");
            reject(err);
          });
      });
    },
    FETCH_TARGET_CREDITS(context) {
      return new Promise((resolve, reject) => {
        get_TARGET_CREDITS
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
              "SET_UPDATE_TARGET_CREDITS_NAME_DATA",
              names_target_credits
            ); // store the response data in store
            context.commit("SET_UPDATE_TARGET_CREDITS_ALL_DATA", response.data); // store the response data in store

            resolve(response);
          })
          .catch(err => {
            // refresh token expired or some other error status
            // eslint-disable-next-line no-unused-vars
            const er = err; // просто чтоб ошибку в консоли не показывало
            // console.log(err);
            // console.log("[FETCH_TARGET_CREDITS] Не получилось");
            reject(err);
          });
      });
    },

    // eslint-disable-next-line no-unused-vars
    FETCH_EDIT_BANKS(context, payload) {
      return new Promise((resolve, reject) => {
        crudBANKS
          .patch(
            "api/v1/mortgages/banks/" + payload["id_bank"] + "/",
            payload["formData"],
            {
              headers: {
                "Content-Type": "multipart/form-data",
                Authorization: `Bearer ${store.state.accessToken}`
              }
            }
          ) // proof that your access token is still valid; if not the
          // axios getAPI response interceptor will attempt to get a new  access token from the server. check out ../api/axios-base.js getAPI instance response interceptor
          .then(response => {
            // console.log("GetAPI successfully got the mods");
            // console.log(response.data);
            // const names_banks = response.data.reduce((total, item) => {
            //   total.push(item.bank_name);
            //   return total;
            // }, []);
            // context.commit("SET_UPDATE_BANKS_NAME_DATA", names_banks); // store the response data in store
            // context.commit("SET_UPDATE_BANKS_ALL_DATA", response.data);
            // console.log("SUCCESS!!");
            // console.log(response);
            resolve(response);
          })
          .catch(err => {
            // refresh token expired or some other error status
            // eslint-disable-next-line no-unused-vars
            const er = err; // просто чтоб ошибку в консоли не показывало
            // console.log(err);
            // console.log("[FETCH_EDIT_BANKS] Не получилось");
            reject(err);
          });
      });
    },
    FETCH_DELETE_BANKS(context, payload) {
      return new Promise((resolve, reject) => {
        crudBANKS
          .delete("api/v1/mortgages/banks/" + payload["id_bank"] + "/", {
            headers: {
              Authorization: `Bearer ${store.state.accessToken}`
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(err => {
            reject(err);
          });
      });
    },
    // eslint-disable-next-line no-unused-vars
    FETCH_CREATE_BANKS(context, payload) {
      return new Promise((resolve, reject) => {
        crudBANKS
          .post("api/v1/mortgages/banks/", payload["formData"], {
            headers: {
              "Content-Type": "multipart/form-data",
              Authorization: `Bearer ${store.state.accessToken}`
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(err => {
            reject(err);
          });
      });
    },

    FETCH_EDIT_TARGET_CREDITS(context, payload) {
      return new Promise((resolve, reject) => {
        crudTargetCredits
          .patch(
            "api/v1/mortgages/target-credits/" +
              payload["id_target_name"] +
              "/",
            payload["formData"],
            {
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${store.state.accessToken}`
              }
            }
          )
          .then(response => {
            resolve(response);
          })
          .catch(err => {
            // refresh token expired or some other error status
            // eslint-disable-next-line no-unused-vars
            const er = err; // просто чтоб ошибку в консоли не показывало
            reject(err);
          });
      });
    },
    FETCH_DELETE_TARGET_CREDITS(context, payload) {
      return new Promise((resolve, reject) => {
        crudTargetCredits
          .delete(
            "api/v1/mortgages/target-credits/" +
              payload["id_target_name"] +
              "/",
            {
              headers: {
                Authorization: `Bearer ${store.state.accessToken}`
              }
            }
          )
          .then(response => {
            resolve(response);
          })
          .catch(err => {
            reject(err);
          });
      });
    },
    FETCH_CREATE_TARGET_CREDITS(context, payload) {
      return new Promise((resolve, reject) => {
        crudTargetCredits
          .post("api/v1/mortgages/target-credits/", payload["formData"], {
            headers: {
              Authorization: `Bearer ${store.state.accessToken}`
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(err => {
            reject(err);
          });
      });
    },

    FETCH_MORTGAGES_CRUD(context, params) {
      // console.log(url);
      return new Promise((resolve, reject) => {
        getAPI
          .get("api/v1/mortgages/crud/", {
            headers: {
              Authorization: `Bearer ${store.state.accessToken}`
            },
            params: params
          }) // proof that your access token is still valid; if not the
          // axios getAPI response interceptor will attempt to get a new  access token from the server. check out ../api/axios-base.js getAPI instance response interceptor
          .then(response => {
            // console.log("GetAPI successfully got the mods");
            // console.log(response);
            context.commit("SET_UPDATE_MORTGAGES_DATA", response.data); // store the response data in store
            resolve(response);
          })
          .catch(err => {
            // refresh token expired or some other error status
            // eslint-disable-next-line no-unused-vars
            // const er = err; // просто чтоб ошибку в консоли не показывало
            // console.log(err.status);
            // console.log("[mortgages] Не получилось");
            reject(err);
          });
      });
    },
    FETCH_EDIT_MORTGAGES(context, payload) {
      return new Promise((resolve, reject) => {
        crudMortgageProgramm
          .patch(
            "api/v1/mortgages/crud/" + payload["id_programs_name"] + "/",
            payload["formData"],
            {
              headers: {
                Authorization: `Bearer ${store.state.accessToken}`
              }
            }
          )
          .then(response => {
            resolve(response);
          })
          .catch(err => {
            // refresh token expired or some other error status
            // eslint-disable-next-line no-unused-vars
            const er = err; // просто чтоб ошибку в консоли не показывало
            reject(err);
          });
      });
    },
    FETCH_DELETE_MORTGAGES(context, payload) {
      return new Promise((resolve, reject) => {
        crudMortgageProgramm
          .delete("api/v1/mortgages/crud/" + payload["id_programs_name"] + "/", {
            headers: {
              Authorization: `Bearer ${store.state.accessToken}`
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(err => {
            reject(err);
          });
      });
    },
    FETCH_CREATE_MORTGAGES(context, payload) {
      return new Promise((resolve, reject) => {
        crudMortgageProgramm
          .post("api/v1/mortgages/crud/", payload["formData"], {
            headers: {
              Authorization: `Bearer ${store.state.accessToken}`
            }
          })
          .then(response => {
            resolve(response);
          })
          .catch(err => {
            reject(err);
          });
      });
    }
  }
};

export default mortgagesModule;
