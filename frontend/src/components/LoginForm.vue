<template>
  <v-app id="inspire">
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="elevation-12">
              <v-toolbar color="primary" dark flat>
                <v-toolbar-title>Вход</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <form v-on:submit.prevent="loginUserForm">
                  <h2 v-if="wrongCred">
                    Введены неверные учетные данные! Пожалуйста, введите ваши
                    правильные данные.
                    {{ wrongCredData }}
                  </h2>
                  <v-text-field
                    prepend-icon="mdi-account"
                    v-model="username"
                    :error-messages="usernameErrors"
                    label="Логин"
                    type="text"
                    required
                    @input="$v.username.$touch()"
                    @blur="$v.username.$touch()"
                  ></v-text-field>
                  <v-text-field
                    prepend-icon="mdi-lock"
                    v-model="password"
                    :error-messages="passwordErrors"
                    label="Пароль"
                    required
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPassword ? 'text' : 'password'"
                    @click:append="showPassword = !showPassword"
                    @input="$v.password.$touch()"
                    @blur="$v.password.$touch()"
                  ></v-text-field>
                  <v-card-actions>
                    <v-spacer />
                    <v-btn
                      class="mr-4"
                      color="primary"
                      type="submit"
                      :disabled="$v.$invalid"
                      >Войти
                    </v-btn>
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
import { required, minLength } from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],

  validations: {
    username: { required },
    password: { required, minLength: minLength(8) }
  },

  data: () => ({
    username: "",
    password: "",
    showPassword: false,
    wrongCred: false,
    wrongCredData: null
  }),

  computed: {
    usernameErrors() {
      const errors = [];
      if (!this.$v.username.$dirty) return errors;
      !this.$v.username.required && errors.push("Введите логин.");
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.minLength &&
        errors.push(
          `Вы ввели ${this.password.length} символов, неоходимо не менее 8.`
        );
      !this.$v.password.required && errors.push("Введите пароль.");
      return errors;
    }
  },

  methods: {
    // ...mapActions("auth", ["loginUser"]),
    submit() {
      this.$v.$touch();
    },
    clear() {
      this.$v.$reset();
      this.username = "";
      this.password = "";
    },
    loginUserForm() {
      // call loginUSer action
      this.$store
        .dispatch("loginUser", {
          username: this.username,
          password: this.password
        })
        .then(() => {
          this.wrongCred = false;
          this.$router.push({ name: "mortgage-search" });
        })
        .catch(err => {
          // console.log(err.response.data);
          this.wrongCredData = err.response.data;
          this.wrongCred = true; // if the credentials were wrong set wrongCred to true
        });
    }
  }
};
</script>

<style scoped></style>
