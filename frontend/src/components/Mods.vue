<template>
  <div class="downloads">
    <div class="bod">
      <h1>Welcome to Download Hub</h1>
      <h2>Versions available:</h2>
      <h2 v-for="mod in APIData" :key="mod.id">{{ mod.name }}</h2>

    </div>
  </div>
</template>

<script>
import { getAPI } from "../api/mods/axios-mods";
import { mapState, mapMutations } from "vuex";
export default {
  name: "Mods",
  // data: () => ({
  //   modsCred: false
  // }),
  computed: {
    ...mapState("mods", ["APIData"]) // get APIData from store.state.
  },
  methods: {
    ...mapMutations("mods", ["SET_UPDATE_APIData"])
  },
  created() {
    getAPI
      .get("/api/v1/mods/", {
        headers: { Authorization: `Bearer ${this.$store.state.accessToken}` }
      }) // proof that your access token is still valid; if not the
      // axios getAPI response interceptor will attempt to get a new  access token from the server. check out ../api/axios-base.js getAPI instance response interceptor
      .then(response => {
        // console.log("GetAPI successfully got the mods");
        // console.log(response);
        this.SET_UPDATE_APIData(response.data); // store the response data in store
      })
      .catch(err => {
        // refresh token expired or some other error status
        // eslint-disable-next-line no-unused-vars
        const er = err;
        // console.log(err);
        // console.log("Не получилось");
      });
  }
};
</script>

<style scoped></style>
