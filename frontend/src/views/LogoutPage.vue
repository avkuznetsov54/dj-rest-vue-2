<template>
  <div class="log"></div>
</template>

<script>
// import { mapActions } from "vuex";
import { mapMutations } from "vuex";

export default {
  name: "LogoutPage",
  methods: {
    // ...mapActions("auth", ["logoutUser"])
    ...mapMutations("mods", ["destroyAPIData"]),
    ...mapMutations("cars", ["destroy_CARS_DATA"])
  },
  created() {
    this.$store.dispatch("logoutUser").then(() => {
      this.destroyAPIData();
      this.destroy_CARS_DATA();
      this.$router.push({ name: "login" });
    });

  }

  // created() {
  //   this.$store.dispatch("logoutUser").then(() => {
  //     this.$router.push({ name: "home" });
  //   });
  // }
};
</script>

<style scoped></style>
