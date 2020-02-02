<template>
  <v-app id="inspire">
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="elevation-12">
              <v-toolbar color="primary" dark flat>
                <v-toolbar-title>Регистрация</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <form @submit.prevent="registerUserForm">
                  <v-text-field
                    v-model="name"
                    :error-messages="nameErrors"
                    :counter="10"
                    label="Name"
                    required
                    @blur="$v.name.$touch()"
                  ></v-text-field>
                  <v-text-field
                    v-model="email"
                    :error-messages="emailErrors"
                    label="E-mail"
                    required
                    @blur="$v.email.$touch()"
                  ></v-text-field>

                  <v-text-field
                    v-model="username"
                    :error-messages="usernameErrors"
                    :counter="10"
                    label="Username"
                    required
                    @blur="$v.username.$touch()"
                  ></v-text-field>
                  <v-text-field
                    v-model="password"
                    :error-messages="passwordErrors"
                    :counter="8"
                    label="Password"
                    required
                    @blur="$v.password.$touch()"
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPassword ? 'text' : 'password'"
                    @click:append="showPassword = !showPassword"
                  ></v-text-field>
                  <v-text-field
                    v-model="confirmPass"
                    :error-messages="confirmPassErrors"
                    :counter="8"
                    label="Confirm Password"
                    required
                    @blur="$v.confirmPass.$touch()"
                    :append-icon="showConfirmPass ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showConfirmPass ? 'text' : 'password'"
                    @click:append="showConfirmPass = !showConfirmPass"
                  ></v-text-field>
                  <div v-if="errorMsgFromApi">
                    <p
                      class="text-sm-left red--text text--lighten-1"
                      v-for="error in errorMsgFromApi"
                      v-bind:key="error"
                    >
                      {{ error }}
                    </p>
                  </div>
                  <v-card-actions class="mt-6">
                    <v-spacer />
                    <v-btn class="mr-4" type="submit">Зарегистрироваться</v-btn>
                    <!--                    <v-btn @click="clear">clear</v-btn>-->
                  </v-card-actions>
                </form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
// import { mapActions } from "vuex";
import { validationMixin } from "vuelidate";
import {
  required,
  maxLength,
  minLength,
  email,
  sameAs
} from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],

  validations: {
    name: { required, maxLength: maxLength(10) },
    username: { required, maxLength: maxLength(10) },
    password: { required, minLength: minLength(8) },
    confirmPass: { required, sameAsPass: sameAs("password") },
    email: {
      required,
      email,
      validBgEmail: function(newEmail) {
        if (newEmail === "") return true;
        // eslint-disable-next-line no-unused-vars
        return new Promise((resolve, reject) => {
          setTimeout(() => {
            const value = newEmail.split("@")[1] == "bgnsk.ru";
            resolve(value);
          }, 1000);
        });
      }
    }
  },

  data: () => ({
    name: "",
    username: "",
    password: "",
    confirmPass: "",
    email: "",
    showPassword: false,
    showConfirmPass: false,
    errorMsgFromApi: null
  }),

  computed: {
    nameErrors() {
      const errors = [];
      if (!this.$v.name.$dirty) return errors;
      !this.$v.name.maxLength &&
        errors.push("Name must be at most 10 characters long");
      !this.$v.name.required && errors.push("Name is required.");
      return errors;
    },
    usernameErrors() {
      const errors = [];
      if (!this.$v.username.$dirty) return errors;
      !this.$v.username.maxLength &&
        errors.push("Name must be at most 10 characters long");
      !this.$v.username.required && errors.push("Name is required.");
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.minLength &&
        errors.push("Пароль должен быть не менее 8 символов.");
      !this.$v.password.required && errors.push("Password is required.");
      return errors;
    },
    confirmPassErrors() {
      const errors = [];
      if (!this.$v.confirmPass.$dirty) return errors;
      // !this.$v.confirmPass.minLength &&
      //   errors.push("Password must be at most 6 characters long");
      !this.$v.confirmPass.sameAsPass &&
        errors.push("Пароли долижны совпадать!");
      // console.log(this.$v.confirmPass.sameAsPass);
      return errors;
    },
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("Ввидите настоящий email.");
      !this.$v.email.required && errors.push("E-mail is required");
      !this.$v.email.validBgEmail &&
        errors.push("E-mail должен быть корпаративный !!!");
      return errors;
    }
  },

  methods: {
    // ...mapActions("auth", ["registerUser"]),
    submit() {
      this.$v.$touch();
    },
    clear() {
      this.$v.$reset();
      this.name = "";
      this.username = "";
      this.password = "";
      this.confirmPass = "";
      this.email = "";
    },
    registerUserForm() {
      this.$store
        .dispatch("registerUser", {
          name: this.name,
          email: this.email,
          username: this.username,
          password: this.password,
          confirmPass: this.confirmPass
        })
        .then(() => {
          this.errorMsgFromApi = null;
          this.$router.push({ name: "login" });
        })
        .catch(error => {
          // console.log(error);
          const obj = Object.keys(error.response.data);
          // console.log(obj[0]);
          this.errorMsgFromApi = error.response.data[obj[0]];
        });
    }
  }
};
</script>

<style scoped></style>
