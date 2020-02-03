<template>
  <div id="app">
    <component :is="layout">
      <router-view />
    </component>
  </div>
</template>

<script>
import EmptyLayout from "./components/layouts/EmptyLayout";
import MainLayout from "./components/layouts/MainLayout";
import { mapActions } from "vuex";

export default {
  components: {
    EmptyLayout,
    MainLayout
  },
  computed: {
    layout() {
      return (this.$route.meta.layout || "empty") + "-layout";
    }
  },
  methods: {
    ...mapActions("user_info", ["FETCH_USER_INFO"]),
    get_user_info() {
      const refresh_token = localStorage.getItem("refresh_token");
      this.FETCH_USER_INFO(refresh_token);
    }
  },
  created() {
    this.get_user_info();
  }
};
</script>

<style lang="scss">

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
