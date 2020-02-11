<template>
  <v-data-table
    :headers="headers"
    :items="listTargetCredits"
    sort-by="calories"
    class="elevation-1"
    locale="ru-Ru"
    :items-per-page="-1"
    hide-default-footer
  >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>Цели кредита</v-toolbar-title>
        <!--        <v-divider class="mx-4" inset vertical></v-divider>-->
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on }">
            <v-btn
              color="primary"
              dark
              class="mb-2"
              v-on="on"
              @click="editItem()"
              >Добавить цель</v-btn
            >
          </template>
          <form @submit.prevent="save">
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="12" md="12">
                      <v-text-field
                        v-model="editedItem.target_name"
                        label="Название цели"
                        @blur="$v.editedItem.target_name.$touch()"
                        :error-messages="nameErrors"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12" sm="12" md="12">
                      <v-textarea
                        v-model="editedItem.target_desc"
                        label="Комментарий к цели"
                        placeholder="Комментарий к цели"
                        outlined
                      ></v-textarea>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                      <div v-if="errMsgBank">
                        <div v-for="(errRow, i) in errMsgBank" :key="i">
                          <div v-for="(err, i) in errRow" :key="i">
                            <v-alert width="100%" type="error">
                              {{ err }}
                            </v-alert>
                          </div>
                        </div>
                      </div>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close">Отмена</v-btn>
                <v-btn color="blue darken-1" text type="submit"
                  >Сохранить</v-btn
                >
              </v-card-actions>
            </v-card>
          </form>
        </v-dialog>

        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="headline">Удаление цели</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  Будте внимательны! При удалении данной цели, она так же
                  удалиться в ипотечных программах!
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDialogDelete"
                >Отмена</v-btn
              >
              <v-btn color="red darken-1 white--text" @click="deleteBank"
                >Удалить</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>

    <template v-slot:item.action="{ item }">
      <v-icon class="mr-2" @click="editItem(item)">
        mdi-square-edit-outline
      </v-icon>

      <v-icon color="red darken-2" @click="deleteItem(item)">
        mdi-delete
      </v-icon>
    </template>

    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">Обновить</v-btn>
    </template>
  </v-data-table>
</template>

<script>
import { mapState, mapGetters, mapActions } from "vuex";
// import { APIUrl } from "@/api/axios-base";

import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";

export default {
  name: "EditTargetCreditsComp",
  mixins: [validationMixin],

  validations: {
    editedItem: { target_name: { required } }
  },
  data: () => ({
    dialog: false,
    dialogDelete: false,
    headers: [
      { text: "Название цели", width: "30%", value: "target_name" },
      {
        text: "Комментарий к цели",
        width: "40%",
        value: "target_desc"
      },
      { text: "Действия", width: "10%", value: "action", sortable: false }
    ],
    listTargetCredits: [],
    editedIndex: -1,
    editedItem: {
      target_name: null,
      target_desc: null
    },
    defaultItem: {
      target: null,
      target_desc: null
    },
    errMsgFieldBankName: null,
    errMsgBank: null
  }),

  computed: {
    ...mapState("mortgages", ["TARGET_CREDITS_ALL_DATA"]),
    ...mapGetters("mortgages", ["GET_TARGET_CREDITS_ALL_DATA"]),
    formTitle() {
      return this.editedIndex === -1 ? "Новая цель" : "Редактировать цель";
    },
    nameErrors() {
      const errors = [];
      if (!this.$v.editedItem.target_name.$dirty) return errors;
      // !this.$v.name.maxLength &&
      //   errors.push("Name must be at most 10 characters long");
      !this.$v.editedItem.target_name.required &&
        errors.push("Это поле обязательное.");
      return errors;
    }
  },

  watch: {
    // eslint-disable-next-line no-unused-vars
    dialog(val, oldVal) {
      val || this.close(); // true - модальное окно открыто, false - закрыто
      // console.log("новое значение: %s, старое значение: %s", val, oldVal);
    }
  },

  created() {
    this.FETCH_TARGET_CREDITS()
      // eslint-disable-next-line no-unused-vars
      .then(response => {
        // console.log("response " + response);
        // this.listTargetCredits = response.data;
        this.listTargetCredits = this.GET_TARGET_CREDITS_ALL_DATA;
      })
      .catch(() => {
        this.$store.dispatch("refreshToken").then(() => {
          this.FETCH_TARGET_CREDITS().then(() => {
            this.listTargetCredits = this.GET_TARGET_CREDITS_ALL_DATA;
          });
        });
      });
    // this.initialize();
  },

  methods: {
    ...mapActions("mortgages", [
      "FETCH_TARGET_CREDITS",
      "FETCH_EDIT_TARGET_CREDITS",
      "FETCH_DELETE_TARGET_CREDITS",
      "FETCH_CREATE_TARGET_CREDITS"
    ]),
    initialize() {
      this.listTargetCredits = this.GET_TARGET_CREDITS_ALL_DATA;
      // console.log("initialize");
      // console.log(this.listTargetCredits);
    },

    editItem(item) {
      // console.log(item);
      this.editedIndex = this.listTargetCredits.indexOf(item);
      // console.log("2 => " + this.editedIndex);
      this.editedItem = Object.assign({}, item);
      // console.log("3 => " + this.editedIndex);
      this.dialog = true;

      // // проверка на какую кнопку нажали "редактировать" или "добавить"
      // if (item) {
      //   this.currentImageView = true;
      //   if (item.bank_logo !== null) {
      //     const url = new URL(item.bank_logo);
      //     // console.log(url.pathname);
      //     this.currentImageLink = url.pathname;
      //     // this.currentImageLink = item.bank_logo.replace(APIUrl, "");
      //     let arrayFromLink = item.bank_logo.split("/");
      //     this.currentImageFile = arrayFromLink[arrayFromLink.length - 1];
      //   }
      // } else {
      //   this.currentImageView = false;
      //   this.currentImageLink = "";
      //   this.currentImageFile = "";
      // }
    },

    // eslint-disable-next-line no-unused-vars
    deleteItem(item) {
      this.editedIndex = this.listTargetCredits.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },
    deleteBank() {
      const payload = new Object();
      payload["id_target_name"] = this.editedItem.id;
      this.FETCH_DELETE_TARGET_CREDITS(payload)
        // eslint-disable-next-line no-unused-vars
        .then(response => {
          this.FETCH_TARGET_CREDITS()
            // eslint-disable-next-line no-unused-vars
            .then(response => {
              this.listTargetCredits = this.GET_TARGET_CREDITS_ALL_DATA;
            });
        })
        // eslint-disable-next-line no-unused-vars
        .catch(error => {
          this.$store.dispatch("refreshToken").then(() => {
            // eslint-disable-next-line no-unused-vars
            this.FETCH_DELETE_TARGET_CREDITS(payload).then(response => {
              this.FETCH_TARGET_CREDITS()
                // eslint-disable-next-line no-unused-vars
                .then(response => {
                  this.listTargetCredits = this.GET_TARGET_CREDITS_ALL_DATA;
                });
            });
          });
        });

      this.dialogDelete = false;
    },

    close() {
      this.dialog = false;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
      this.errMsgBank = null;
    },

    // openDialogDelete() {
    //   this.dialogDelete = true;
    // },
    closeDialogDelete() {
      this.dialogDelete = false;
    },

    save() {
      // Проверяем если есть индекс то нужно "редактирование"
      if (this.editedIndex > -1) {
        // Object.assign(this.listTargetCredits[this.editedIndex], this.editedItem);
        let val = "update";
        this.submitForm(val);
      } else {
        // если индекс = -1 то нужно создать новый банк
        // this.listTargetCredits.push(this.editedItem);
        // console.log("Добавление нового банка");
        // console.log(this.editedIndex);

        let val = "create";
        this.submitForm(val);
      }
      // console.log(this.listTargetCredits[this.editedIndex]);
    },

    submitForm(val) {
      if (!this.editedItem.target_name) {
        return true;
      }

      //Initialize the form data
      let formData = new FormData();

      formData.append("target_name", this.editedItem.target_name);

      if (this.editedItem.target_desc || this.editedItem.target_desc === "") {
        formData.append("target_desc", this.editedItem.target_desc);
      }

      // console.log(typeof this.editedItem.preference_value);
      // console.log(this.editedItem.preference_is_active);

      const payload = new Object();
      payload["id_target_name"] = this.editedItem.id;
      payload["formData"] = formData;
      // const id_bank = this.editedItem.id;
      // console.log(payload);

      if (val === "update") {
        // Отправляем данные для изменения и ждём ответа
        this.FETCH_EDIT_TARGET_CREDITS(payload)
          // eslint-disable-next-line no-unused-vars
          .then(response => {
            this.FETCH_TARGET_CREDITS()
              // eslint-disable-next-line no-unused-vars
              .then(response => {
                // console.log("response " + response);
                // this.listTargetCredits = response.data;
                this.listTargetCredits = this.GET_TARGET_CREDITS_ALL_DATA;
                this.close();
              });
          })
          // eslint-disable-next-line no-unused-vars
          .catch(error => {
            // console.log("error " + error);
            this.$store.dispatch("refreshToken").then(() => {
              this.FETCH_EDIT_TARGET_CREDITS(payload)
                // eslint-disable-next-line no-unused-vars
                .then(response => {
                  // console.log("qqqq " + response);
                  // записываем изменённые данные в таблицу на странице под нужным индексом элемента
                  // Object.assign(this.listTargetCredits[this.editedIndex], response.data);

                  this.FETCH_TARGET_CREDITS()
                    // eslint-disable-next-line no-unused-vars
                    .then(response => {
                      // console.log("response " + response);
                      // this.listTargetCredits = response.data;
                      this.listTargetCredits = this.GET_TARGET_CREDITS_ALL_DATA;
                      this.close();
                    });
                }) // eslint-disable-next-line no-unused-vars
                .catch(err => {
                  this.errMsgBank = err.response.data;
                });
            });
          });
      } else {
        this.FETCH_CREATE_TARGET_CREDITS(payload)
          // eslint-disable-next-line no-unused-vars
          .then(response => {
            this.FETCH_TARGET_CREDITS()
              // eslint-disable-next-line no-unused-vars
              .then(response => {
                // console.log("response " + response);
                // this.listTargetCredits = response.data;
                this.listTargetCredits = this.GET_TARGET_CREDITS_ALL_DATA;
                this.close();
              });
          })
          // eslint-disable-next-line no-unused-vars
          .catch(error => {
            // console.log("error " + error);
            this.$store.dispatch("refreshToken").then(() => {
              this.FETCH_CREATE_TARGET_CREDITS(payload)
                // eslint-disable-next-line no-unused-vars
                .then(response => {
                  this.FETCH_TARGET_CREDITS()
                    // eslint-disable-next-line no-unused-vars
                    .then(response => {
                      // console.log("response " + response);
                      this.listTargetCredits = this.GET_TARGET_CREDITS_ALL_DATA;
                      this.close();
                    });
                })
                // eslint-disable-next-line no-unused-vars
                .catch(err => {
                  this.errMsgBank = err.response.data;
                  // console.log(err.response.data);
                });
            });
          });
      }
    }
  }
};
</script>

<style scoped>
.link_w_u {
  text-decoration: none;
}
</style>
