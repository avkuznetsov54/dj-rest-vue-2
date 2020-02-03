import Vue from "vue";
import Vuex from "vuex";
import router from "../router";
import { axiosBase } from "../api/axios-base";
import cars from "./modules/cars/cars";
import mods from "./modules/mods/mods";
import mortgages from "./modules/mortgages/mortgages";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    accessToken: localStorage.getItem("access_token") || null, // makes sure the user is logged in even after
    // refreshing the page
    refreshToken: localStorage.getItem("refresh_token") || null
  },
  getters: {
    //* getters - простые ф-ции для получения данных из state
    //* на getters подписаны components, чтоб получать данных из state
    //* использовать только синхронные ф-ции !!!
    loggedIn(state) {
      return state.accessToken != null;
    },
    GET_accessToken(state) {
      return state.accessToken;
    }
  },
  mutations: {
    //* mutations - переопределяем state только здесь !!!!
    updateLocalStorage(state, { access, refresh }) {
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);
      state.accessToken = access;
      state.refreshToken = refresh;
    },
    updateAccess(state, access) {
      localStorage.setItem("access_token", access);
      state.accessToken = access;
    },
    destroyToken(state) {
      state.accessToken = null;
      state.refreshToken = null;
    }
  },
  actions: {
    //* actions - выполняем бизнес логику
    //* actions -> mutations -> state -> getters -> components
    // run the below action to get a new access token on expiration
    refreshToken(context) {
      return new Promise((resolve, reject) => {
        //* resolve - ф-ция которая скажет что Promise выполнился успешно
        //* reject - не успешно
        axiosBase
          .post("/api/v1/token/refresh/", {
            refresh: context.state.refreshToken
          }) // send the stored refresh token to the backend API
          .then(response => {
            // if API sends back new access and refresh token update the store
            console.log("New access successfully generated");
            context.commit("updateAccess", response.data.access);
            resolve(response.data.access);
          })
          .catch(err => {
            console.log("error in refreshToken Task");
            router.push({ name: "logout" }); // если refreshToken истек, то перенаправляем
            reject(err); // ошибка при создании нового маркера доступа и обновления, поскольку срок действия маркера обновления истек
          });
      });
    },
    registerUser(context, data) {
      // console.log(data);
      return new Promise((resolve, reject) => {
        axiosBase
          .post("/auth/users/", {
            first_name: data.name,
            email: data.email,
            username: data.username,
            password: data.password
            // confirm: data.confirm
          })
          .then(response => {
            resolve(response);
          })
          .catch(error => {
            reject(error);
          });
      });
    },
    logoutUser(context) {
      if (context.getters.loggedIn) {
        // eslint-disable-next-line no-unused-vars
        return new Promise((resolve, reject) => {
          axiosBase
            .post("/api/v1/token/logout/", {
              refresh_token: localStorage.getItem("refresh_token")
              // Отправляем refresh_token в django чтоб удалить из БД
            })
            // eslint-disable-next-line no-unused-vars
            .then(response => {
              // console.log(response.status);
              localStorage.removeItem("access_token");
              localStorage.removeItem("refresh_token");
              context.commit("destroyToken");
              resolve(response);
            })
            .catch(err => {
              localStorage.removeItem("access_token");
              localStorage.removeItem("refresh_token");
              context.commit("destroyToken");
              console.log("logoutUser catch");
              reject(err);
            });
        });
      }
    },
    loginUser(context, credentials) {
      return new Promise((resolve, reject) => {
        // send the username and password to the backend API:
        axiosBase
          .post("/api/v1/token/", {
            username: credentials.username,
            password: credentials.password
          })
          // if successful update local storage:
          .then(response => {
            console.log(response.data);
            context.commit("updateLocalStorage", {
              access: response.data.access,
              refresh: response.data.refresh
            }); // store the access and refresh token in localstorage
            resolve();
          })
          .catch(err => {
            reject(err);
          });
      });
    }
  },
  modules: {
    cars,
    mods,
    mortgages
  }
});
