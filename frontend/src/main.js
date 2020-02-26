import "babel-polyfill";
import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store/index";
// import auth from "./store/modules/auth/auth";
import vuetify from "./plugins/vuetify";

Vue.config.productionTip = false;

router.beforeEach((to, from, next) => {
  // if any of the routes in ./router.js has a meta named 'requiresAuth: true'
  // then check if the user is logged in before routing to this path:
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.loggedIn) {
      next({ name: "login" });
    } else {
      next();
    }
  }
  // else if any of the routes in ./router.js has a meta named 'requiresLogged: true'
  // then check if the user is logged in; if true continue to home page else continue routing to the destination path
  // this comes to play if the user is logged in and tries to access the login/register page
  else if (to.matched.some(record => record.meta.requiresLogged)) {
    if (store.getters.loggedIn) {
      next({ name: "mortgage-search" });
    } else {
      next();
    }
  } else {
    next();
  }
});

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
