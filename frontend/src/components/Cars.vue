<template>
  <div>
    <v-container fluid>
      <v-row align="center" justify="center">
        <table>
          <thead>
            <tr>
              <th>vin</th>
              <th>color</th>
              <th>brand</th>
              <th>car_type</th>
              <th>user</th>
              <th>year</th>
              <th>volume</th>
              <th>Remove</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="car in CARS_DATA" v-bind:key="car.id">
              <td>{{ car.vin }}</td>
              <td>{{ car.color }}</td>
              <td>{{ car.brand }}</td>
              <td>{{ car.car_type }}</td>
              <td>{{ car.user }}</td>
              <td>{{ car.year }}</td>
              <td>{{ car.volume }}</td>
              <td><button @click="removeCar(car)">-</button></td>
            </tr>
          </tbody>
        </table>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { getAPI } from "../api/cars/axios-cars";
import { mapState, mapMutations } from "vuex";

export default {
  name: "Cars",
  computed: {
    ...mapState("cars", ["CARS_DATA"]) // get APIData from store.state.
  },
  methods: {
    ...mapMutations("cars", ["SET_UPDATE_CARS_DATA"])
  },
  created() {
    getAPI
      .get("api/v1/cars/all/", {
        headers: { Authorization: `Bearer ${this.$store.state.accessToken}` }
      }) // proof that your access token is still valid; if not the
      // axios getAPI response interceptor will attempt to get a new  access token from the server. check out ../api/axios-base.js getAPI instance response interceptor
      .then(response => {
        // console.log("GetAPI successfully got the mods");
        // console.log(response);
        this.SET_UPDATE_CARS_DATA(response.data); // store the response data in store
      })
      .catch(err => {
        // refresh token expired or some other error status
        // eslint-disable-next-line no-unused-vars
        const er = err; // просто чтоб ошибку в консоли не показывало
        // console.log(err);
        console.log("Не получилось");
      });
  }
};
</script>

<style scoped></style>
