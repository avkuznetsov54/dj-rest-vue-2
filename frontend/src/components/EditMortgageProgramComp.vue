<template>
  <v-data-table
    :headers="headers"
    :items="listProgram"
    sort-by="calories"
    class="elevation-1"
    locale="ru-Ru"
    :items-per-page="-1"
    hide-default-footer
    sortBy="bank.bank_name"
    :search="search"
  >
    <template v-slot:item.bank.bank_logo="{ item }">
      <v-img
        v-if="item.bank.bank_logo !== null"
        :src="item.bank.bank_logo"
        max-width="120"
        max-height="50"
        contain
      ></v-img>
    </template>
    <template v-slot:item.rate="{ item }">
      <span> {{ item.rate }}% </span>
    </template>
    <template v-slot:item.rate_salary="{ item }">
      <span v-if="item.rate_salary !== null"> {{ item.rate_salary }}% </span>
    </template>
    <template v-slot:item.first_payment="{ item }">
      <span v-if="item.first_payment !== null">
        {{ item.first_payment }}%
      </span>
    </template>

    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>Кредитные программы</v-toolbar-title>
        <!--                <v-divider class="mx-4" inset vertical></v-divider>-->
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          label="Поиск"
          single-line
          clearable
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-dialog persistent v-model="dialog" max-width="1000px">
          <template v-slot:activator="{ on }">
            <v-btn
              color="primary"
              dark
              class="mb-2"
              v-on="on"
              @click="editItem()"
              >Добавить программу</v-btn
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
                    <v-col cols="12" sm="12" md="4">
                      <v-select
                        label="Банк"
                        placeholder="Любой"
                        :items="GET_BANKS_ALL_DATA"
                        item-text="bank_name"
                        item-value="id"
                        v-model="editedItem.programs_bank"
                      >
                      </v-select>
                    </v-col>

                    <v-col cols="12" sm="12" md="4">
                      <v-text-field
                        v-model="editedItem.programs_name"
                        label="Название программы"
                        @blur="$v.editedItem.programs_name.$touch()"
                        :error-messages="nameErrors"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12" sm="4" md="2">
                      <v-text-field
                        v-model="editedItem.rate"
                        label="Ставка"
                        placeholder="Ставка"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12" sm="12" md="4">
                      <v-select
                        multiple
                        label="Цель кредита"
                        placeholder="Любой"
                        :items="GET_TARGET_CREDITS_ALL_DATA"
                        item-text="target_name"
                        item-value="id"
                        v-model="editedItem.programs_target"
                      >
                        <template v-slot:selection="{ item, index }">
                          <!--                  <span v-if="index === 0">-->
                          <!--                    <span>{{ item }} </span>-->
                          <!--                  </span>-->
                          <span
                            v-if="index === 0"
                            class="ml-1 grey--text caption"
                            >Выбранно
                            {{ editedItem.programs_target.length }} шт.</span
                          >
                        </template>
                      </v-select>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col>
                      <div v-if="errMsgBank">
                        <!--                        <div v-for="(errRow, i) in errMsgBank" :key="i">-->
                        <!--                          <div v-for="(err, i) in errRow" :key="i">-->
                        <v-alert width="100%" type="error">
                          {{ errMsgBank }}
                        </v-alert>
                        <!--                          </div>-->
                        <!--                        </div>-->
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
              <span class="headline">Удаление программы</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  Будте внимательны! Вы действительно хотите удалить эту
                  программу?
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
  name: "EditMortgageProgramComp",
  mixins: [validationMixin],

  validations: {
    editedItem: { programs_name: { required } }
  },
  data: () => ({
    dialog: false,
    dialogDelete: false,
    search: "",
    headers: [
      {
        width: "12%",
        align: "left",
        sortable: false,
        value: "bank.bank_logo"
      },
      {
        text: "Банк",
        width: "15%",
        align: "left",
        value: "bank.bank_name"
      },
      { text: "Название программы", width: "30%", value: "programs_name" },
      {
        text: "Ставка",
        width: "10%",
        value: "rate"
      },
      {
        text: "Ставка зарплатникам",
        width: "10%",
        value: "rate_salary"
      },
      {
        text: "ПВ",
        width: "10%",
        value: "first_payment"
      },
      { text: "Действия", width: "10%", value: "action", sortable: false }
    ],
    listProgram: [],
    editedIndex: -1,
    editedItem: {},
    defaultItem: {},
    errMsgFieldBankName: null,
    errMsgBank: null
  }),

  computed: {
    ...mapState("mortgages", ["BANKS_NAME_DATA", "MORTGAGES_DATA"]),
    ...mapGetters("mortgages", [
      "GET_BANKS_ALL_DATA",
      "GET_TARGET_CREDITS_ALL_DATA",
      "GET_MORTGAGES_DATA"
    ]),
    formTitle() {
      return this.editedIndex === -1
        ? "Новая программа"
        : "Редактировать программу";
    },
    nameErrors() {
      const errors = [];
      if (!this.$v.editedItem.programs_name.$dirty) return errors;
      // !this.$v.name.maxLength &&
      //   errors.push("Name must be at most 10 characters long");
      !this.$v.editedItem.programs_name.required &&
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
    this.FETCH_BANKS();
    this.FETCH_TARGET_CREDITS();
    this.FETCH_MORTGAGES()
      // eslint-disable-next-line no-unused-vars
      .then(response => {
        // console.log("response " + response);
        // this.listProgram = response.data;
        this.listProgram = this.GET_MORTGAGES_DATA;
      })
      .catch(() => {
        this.$store.dispatch("refreshToken").then(() => {
          this.FETCH_MORTGAGES().then(() => {
            this.listProgram = this.GET_MORTGAGES_DATA;
          });
        });
      });
    // this.initialize();
  },

  methods: {
    ...mapActions("mortgages", [
      "FETCH_BANKS",
      "FETCH_TARGET_CREDITS",
      "FETCH_MORTGAGES",
      "FETCH_EDIT_MORTGAGES",
      "FETCH_DELETE_MORTGAGES",
      "FETCH_CREATE_MORTGAGES"
    ]),
    initialize() {
      this.listProgram = this.GET_MORTGAGES_DATA;
      // console.log("initialize");
      // console.log(this.listProgram);
    },

    editItem(item) {
      // console.log(item);
      this.editedIndex = this.listProgram.indexOf(item);
      // console.log("2 => " + this.editedIndex);
      this.editedItem = Object.assign({}, item);
      // console.log("3 => " + this.editedIndex);
      console.log(this.editedItem);
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
      this.editedIndex = this.listProgram.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },
    deleteBank() {
      const payload = new Object();
      payload["id_programs_name"] = this.editedItem.id;
      this.FETCH_DELETE_MORTGAGES(payload)
        // eslint-disable-next-line no-unused-vars
        .then(response => {
          this.FETCH_MORTGAGES()
            // eslint-disable-next-line no-unused-vars
            .then(response => {
              this.listProgram = this.GET_MORTGAGES_DATA;
            });
        })
        // eslint-disable-next-line no-unused-vars
        .catch(error => {
          this.$store.dispatch("refreshToken").then(() => {
            // eslint-disable-next-line no-unused-vars
            this.FETCH_DELETE_MORTGAGES(payload).then(response => {
              this.FETCH_MORTGAGES()
                // eslint-disable-next-line no-unused-vars
                .then(response => {
                  this.listProgram = this.GET_MORTGAGES_DATA;
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
        // Object.assign(this.listProgram[this.editedIndex], this.editedItem);
        let val = "update";
        this.submitForm(val);
      } else {
        // если индекс = -1 то нужно создать новый банк
        // this.listProgram.push(this.editedItem);
        // console.log("Добавление нового банка");
        // console.log(this.editedIndex);

        let val = "create";
        this.submitForm(val);
      }
      // console.log(this.listProgram[this.editedIndex]);
    },

    submitForm(val) {
      if (!this.editedItem.programs_name) {
        return true;
      }

      //Initialize the form data
      // let formData = new FormData();
      // formData.append("programs_bank", this.editedItem.programs_bank);
      // formData.append("programs_name", this.editedItem.programs_name);
      // formData.append("programs_target", this.editedItem.programs_target);

      let formData = new Object();
      formData["programs_bank"] = this.editedItem.programs_bank;
      formData["programs_name"] = this.editedItem.programs_name;
      formData["programs_target"] = this.editedItem.programs_target;

      // console.log(typeof this.editedItem.preference_value);
      console.log(this.editedItem.programs_target);

      const payload = new Object();
      payload["id_programs_name"] = this.editedItem.id;
      payload["formData"] = formData;
      // const id_bank = this.editedItem.id;
      // console.log(payload);

      if (val === "update") {
        // Отправляем данные для изменения и ждём ответа
        this.FETCH_EDIT_MORTGAGES(payload)
          // eslint-disable-next-line no-unused-vars
          .then(response => {
            this.FETCH_MORTGAGES()
              // eslint-disable-next-line no-unused-vars
              .then(response => {
                // console.log("response " + response);
                // this.listProgram = response.data;
                this.listProgram = this.GET_MORTGAGES_DATA;
                this.close();
              });
          })
          // eslint-disable-next-line no-unused-vars
          .catch(error => {
            console.log(error.config);
            this.$store.dispatch("refreshToken").then(() => {
              this.FETCH_EDIT_MORTGAGES(payload)
                // eslint-disable-next-line no-unused-vars
                .then(response => {
                  // console.log("qqqq " + response);
                  // записываем изменённые данные в таблицу на странице под нужным индексом элемента
                  // Object.assign(this.listProgram[this.editedIndex], response.data);

                  this.FETCH_MORTGAGES()
                    // eslint-disable-next-line no-unused-vars
                    .then(response => {
                      // console.log("response " + response);
                      // this.listProgram = response.data;
                      this.listProgram = this.GET_MORTGAGES_DATA;
                      this.close();
                    });
                }) // eslint-disable-next-line no-unused-vars
                .catch(err => {
                  this.errMsgBank = err.response.data;
                });
            });
          });
      } else {
        this.FETCH_CREATE_MORTGAGES(payload)
          // eslint-disable-next-line no-unused-vars
          .then(response => {
            this.FETCH_MORTGAGES()
              // eslint-disable-next-line no-unused-vars
              .then(response => {
                // console.log("response " + response);
                // this.listProgram = response.data;
                this.listProgram = this.GET_MORTGAGES_DATA;
                this.close();
              });
          })
          // eslint-disable-next-line no-unused-vars
          .catch(error => {
            // console.log("error " + error);
            this.$store.dispatch("refreshToken").then(() => {
              this.FETCH_CREATE_MORTGAGES(payload)
                // eslint-disable-next-line no-unused-vars
                .then(response => {
                  this.FETCH_MORTGAGES()
                    // eslint-disable-next-line no-unused-vars
                    .then(response => {
                      // console.log("response " + response);
                      this.listProgram = this.GET_MORTGAGES_DATA;
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
