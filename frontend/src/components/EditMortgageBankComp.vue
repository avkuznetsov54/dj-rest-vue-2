<template>
  <v-data-table
    :headers="headers"
    :items="listBanks"
    sort-by="calories"
    class="elevation-1"
  >
    <template v-slot:item.bank_logo="{ item }">
      <v-img
        v-if="item.bank_logo !== null"
        :src="item.bank_logo"
        max-width="120"
        max-height="50"
        contain
      ></v-img>
    </template>
    <template v-slot:item.preference_is_active="{ item }">
      <v-icon v-if="item.preference_is_active" color="green darken-2"
        >mdi-checkbox-marked-circle</v-icon
      >
    </template>

    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>Банки</v-toolbar-title>
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
              >Добавить банк</v-btn
            >
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="12" md="12">
                    <!--                    <v-text-field-->
                    <!--                      v-model="editedItem.bank_logo"-->
                    <!--                      label="Логотип"-->
                    <!--                    ></v-text-field>-->

                    <!--                    <v-file-input-->
                    <!--                      label="Выбрать логотип"-->
                    <!--                      show-size-->
                    <!--                      type="file"-->
                    <!--                      ref="file"-->
                    <!--                      v-on:change="handleFileUpload()"-->
                    <!--                    ></v-file-input>-->

                    <v-btn
                      color="primary"
                      class="white--text"
                      @click="$refs.file.click()"
                    >
                      <v-icon left dark>mdi-cloud-upload</v-icon>
                      Новый логотип
                    </v-btn>
                    <input
                      type="file"
                      ref="file"
                      style="display:none;"
                      v-on:change="handleFileUpload()"
                    />
                    <template v-if="newImageView">
                      <p class="font-weight-thin mt-1 mb-0">
                        Выбран: {{ newImageFile }}
                      </p>
                    </template>
                    <template v-if="currentImageView">
                      <p class="font-weight-thin mt-1">
                        На данный момент:
                        <router-link
                          class="link_w_u"
                          tag="a"
                          :to="currentImageLink"
                          >{{ currentImageFile }}
                        </router-link>
                      </p>
                    </template>
                  </v-col>
                  <v-col cols="12" sm="12" md="12">
                    <v-text-field
                      v-model="editedItem.bank_name"
                      label="Банк"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="6">
                    <v-checkbox
                      v-model="editedItem.preference_is_active"
                      label="Преференция"
                      color="primary"
                    ></v-checkbox>
                  </v-col>
                  <v-col cols="12" sm="6" md="6">
                    <v-text-field
                      v-model="editedItem.preference_value"
                      label="Процент преференции"
                      type="number"
                      min="0"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="12">
                    <v-textarea
                      v-model="editedItem.preference_comment"
                      label="Комментарий к преференции"
                      placeholder="Комментарий к преференции"
                      outlined
                    ></v-textarea>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Отмена</v-btn>
              <v-btn color="blue darken-1" text @click="save">Сохранить</v-btn>
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
import { APIUrl } from "@/api/axios-base";

export default {
  name: "EditMortgageBankComp",
  data: () => ({
    dialog: false,
    headers: [
      {
        text: "Логотип",
        align: "left",
        sortable: false,
        value: "bank_logo"
      },
      { text: "Название банка", value: "bank_name" },
      { text: "Преференция", value: "preference_is_active" },
      { text: "Процент", value: "preference_value" },
      { text: "Комментарий к преференции", value: "preference_comment" },
      { text: "Действия", value: "action", sortable: false }
    ],
    listBanks: [],
    editedIndex: -1,
    editedItem: {
      bank_logo: null,
      bank_name: null,
      preference_is_active: null,
      preference_value: null,
      preference_comment: null
    },
    defaultItem: {
      bank_logo: null,
      bank_name: null,
      preference_is_active: null,
      preference_value: null,
      preference_comment: null
    },
    currentImageFile: "",
    currentImageLink: "",
    currentImageView: true,
    newImageView: false,
    newImageFile: null
  }),

  computed: {
    ...mapState("mortgages", ["BANKS_ALL_DATA"]),
    ...mapGetters("mortgages", ["GET_BANKS_ALL_DATA"]),
    formTitle() {
      return this.editedIndex === -1 ? "Новый банк" : "Редактировать банк";
    }
  },

  watch: {
    // eslint-disable-next-line no-unused-vars
    dialog(val, oldVal) {
      val || this.close(); // true - модальное окно открыто, false - закрыто
      // console.log("новое значение: %s, старое значение: %s", val, oldVal);
      if (!val) {
        // false
        // при закрытии
        this.newImageFile = "";
        this.newImageView = false;
      }
    },
    newImageFile(val) {
      if (isNaN(val)) {
        // если выбрали картинку то показываем блок
        this.newImageView = true;
      }
    }
  },

  created() {
    this.FETCH_BANKS()
      // eslint-disable-next-line no-unused-vars
      .then(response => {
        // console.log("response " + response);
        // this.listBanks = response.data;
        this.listBanks = this.GET_BANKS_ALL_DATA;
      })
      .catch(() => {
        this.$store.dispatch("refreshToken").then(() => {
          this.FETCH_BANKS().then(() => {
            this.listBanks = this.GET_BANKS_ALL_DATA;
          });
        });
      });
    // this.initialize();
  },

  methods: {
    ...mapActions("mortgages", ["FETCH_BANKS", "FETCH_EDIT_BANKS"]),
    initialize() {
      this.listBanks = this.GET_BANKS_ALL_DATA;
      // console.log("initialize");
      // console.log(this.listBanks);
    },

    editItem(item) {
      // console.log(item);
      this.editedIndex = this.listBanks.indexOf(item);
      // console.log("2 => " + this.editedIndex);
      this.editedItem = Object.assign({}, item);
      // console.log("3 => " + this.editedIndex);
      this.dialog = true;

      // проверка на какую кнопку нажали "редактировать" или "добавить"
      if (item) {
        this.currentImageView = true;
        if (item.bank_logo !== null) {
          this.currentImageLink = item.bank_logo.replace(APIUrl, "");
          let arrayFromLink = item.bank_logo.split("/");
          this.currentImageFile = arrayFromLink[arrayFromLink.length - 1];
        }
      } else {
        this.currentImageView = false;
        this.currentImageLink = "";
        this.currentImageFile = "";
      }
    },

    deleteItem(item) {
      const index = this.listBanks.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.listBanks.splice(index, 1);
    },

    close() {
      this.dialog = false;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },

    save() {
      // Проверяем если есть индекс то нужно "редактирование"
      if (this.editedIndex > -1) {
        // Object.assign(this.listBanks[this.editedIndex], this.editedItem);
        this.submitFile();
      } else {
        // если индекс = -1 то нужно создать новый банк
        // this.listBanks.push(this.editedItem);
        // console.log("Добавление нового банка");
        // console.log(this.editedIndex);
      }
      // console.log(this.listBanks[this.editedIndex]);
      this.close();
    },

    submitFile() {
      //Initialize the form data
      let formData = new FormData();

      //Add the form data we need to submit
      if (
        isNaN(this.editedItem.bank_logo) && // isNaN(File) = true, isNaN(null) = false
        typeof this.editedItem.bank_logo !== "string"
      ) {
        formData.append("bank_logo", this.editedItem.bank_logo);
      }
      formData.append("bank_name", this.editedItem.bank_name);
      formData.append(
        "preference_is_active",
        this.editedItem.preference_is_active
      );
      // Number(this.editedItem.preference_value) - преобразует в число
      // typeof Number(value) === "number" - если оставят поле пустым будет true
      // if (0) - false
      if (
        typeof Number(this.editedItem.preference_value) === "number" &&
        typeof this.editedItem.preference_value !== "object" // typeof null = object
      ) {
        formData.append("preference_value", this.editedItem.preference_value);
      }
      formData.append("preference_comment", this.editedItem.preference_comment);

      // console.log(typeof this.editedItem.preference_value);
      // console.log(this.editedItem.preference_value);

      const payload = new Object();
      payload["id_bank"] = this.editedItem.id;
      payload["formData"] = formData;
      // const id_bank = this.editedItem.id;
      // console.log(payload);

      // Отправляем данные для изменения и ждём ответа
      this.FETCH_EDIT_BANKS(payload)
        // eslint-disable-next-line no-unused-vars
        .then(response => {
          // console.log("qqqq " + response);
          // записываем изменённые данные в таблицу на странице под нужным индексом элемента
          // Object.assign(this.listBanks[this.editedIndex], response.data);

          this.FETCH_BANKS()
            // eslint-disable-next-line no-unused-vars
            .then(response => {
              // console.log("response " + response);
              // this.listBanks = response.data;
              this.listBanks = this.GET_BANKS_ALL_DATA;
            });
        })
        // eslint-disable-next-line no-unused-vars
        .catch(error => {
          // console.log("error " + error);
          this.$store.dispatch("refreshToken").then(() => {
            // eslint-disable-next-line no-unused-vars
            this.FETCH_EDIT_BANKS(payload).then(response => {
              // console.log("qqqq " + response);
              // записываем изменённые данные в таблицу на странице под нужным индексом элемента
              // Object.assign(this.listBanks[this.editedIndex], response.data);

              this.FETCH_BANKS()
                // eslint-disable-next-line no-unused-vars
                .then(response => {
                  // console.log("response " + response);
                  // this.listBanks = response.data;
                  this.listBanks = this.GET_BANKS_ALL_DATA;
                });
            });
          });
        });
    },
    handleFileUpload() {
      // Если нажали на выбор файла и ни чего не выбрали, то ничего не добавляем в newImageFile
      if (this.$refs.file.files.length !== 0) {
        this.editedItem.bank_logo = this.$refs.file.files[0];
        // console.log(this.$refs.file.files[0]);
        // console.log(this.$refs.file.files[0].name);
        this.newImageFile = this.$refs.file.files[0].name;
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
