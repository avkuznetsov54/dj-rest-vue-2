<template>
  <div>
    <v-card>
      <v-card-text>
        <v-form v-on:submit.prevent="filterMortgages">
          <!--      <v-form v-on:change="filterMortgages">-->
          <v-container fluid>
            <v-row>
              <v-col cols="12" md="2">
                <v-select
                  multiple
                  label="Банк"
                  placeholder="Любой"
                  :items="BANKS_NAME_DATA"
                  v-model="filters.bank_name"
                  dense
                  clearable
                >
                  <template v-slot:selection="{ item, index }">
                    <!--                  <span v-if="index === 0">-->
                    <!--                    <span>{{ item }} </span>-->
                    <!--                  </span>-->
                    <span v-if="index === 0" class="ml-1 grey--text caption"
                      >Выбранно {{ filters.bank_name.length }} шт.</span
                    >
                  </template>
                </v-select>
              </v-col>
              <v-col cols="12" md="2">
                <v-select
                  multiple
                  label="Цель ипотеки"
                  placeholder="Любая"
                  :items="TARGET_CREDITS_NAME_DATA"
                  v-model="filters.names_target_credits"
                  dense
                  clearable
                >
                  <template v-slot:selection="{ item, index }">
                    <!--                  <span v-if="index === 0">-->
                    <!--                    <span>{{ item }} </span>-->
                    <!--                  </span>-->
                    <span v-if="index === 0" class="ml-1 grey--text caption"
                      >Выбранно
                      {{ filters.names_target_credits.length }} шт.</span
                    >
                  </template>
                </v-select>
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field
                  v-model="filters.property_value"
                  label="Стоимость недвижимости, руб"
                  placeholder="Любая"
                  min="0"
                  dense
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="2">
                <v-text-field
                  v-model="num_first_payment"
                  label="Первоначальный взнос, руб"
                  placeholder="Любой"
                  min="0"
                  dense
                  :suffix="procent_first_payment"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="2">
                <v-text-field
                  v-model="filters.time_credit"
                  type="number"
                  label="Срок, лет"
                  placeholder="Любой"
                  min="0"
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <template v-if="visibleSearch">
              <v-row>
                <v-col cols="12" md="2">
                  <v-text-field
                    v-model="filters.rate"
                    type="number"
                    label="Ставка"
                    placeholder="Любая"
                    suffix="%"
                    min="0"
                    dense
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="2">
                  <v-text-field
                    type="number"
                    v-model="filters.work_experience"
                    label="Стаж на последнем месте"
                    placeholder="Любой"
                    suffix="мес."
                    min="0"
                    dense
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="2">
                  <v-text-field
                    type="number"
                    v-model="filters.borrower_age"
                    label="Возрасть заёмщика"
                    placeholder="Любой"
                    suffix="лет"
                    min="0"
                    dense
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" md="2">
                  <v-checkbox
                    dense
                    v-model="filters.is_rate_salary"
                    value="yes"
                    class="mx-2"
                    label="Программы для зарплатников"
                  ></v-checkbox>
                </v-col>

                <v-col cols="12" md="2">
                  <v-checkbox
                    dense
                    v-model="filters.understatement_is_active"
                    class="mx-2"
                    label="Занижение"
                  ></v-checkbox>
                </v-col>

                <v-col cols="12" md="2">
                  <v-checkbox
                    dense
                    v-model="filters.express_issue"
                    class="mx-2"
                    value="yes"
                    label="Экспресс выдача"
                  ></v-checkbox>
                </v-col>

                <v-col cols="12" md="3">
                  <v-checkbox
                    dense
                    v-model="filters.inclusion_children"
                    class="mx-2"
                    value="yes"
                    label="Включение детей в число собственников"
                  ></v-checkbox>
                </v-col>
              </v-row>
            </template>
            <v-row>
              <v-spacer></v-spacer>
              <v-col cols="12" sm="6" md="4">
                <div class="float-right">
                  <v-btn color="primary" class="mx-1" type="submit" width="100"
                    >Найти
                  </v-btn>
                  <v-btn color="primary" class="mx-1" @click="clearFilter()"
                    ><v-icon>mdi-cached</v-icon>
                  </v-btn>
                  <v-btn color="primary" class="mx-1" @click="toggleSearch"
                    ><v-icon>
                      {{
                        visibleSearch ? "mdi-chevron-up" : "mdi-chevron-down"
                      }}
                    </v-icon>
                  </v-btn>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
    </v-card>

    <v-spacer class="my-4"></v-spacer>

    <div class="text-center d-flex pb-4 float-right">
      <v-btn v-if="showFullMortgage" color="blue-grey lighten-5" @click="all"
        >Развернуть</v-btn
      >
      <!--      <div>{{ panel }}</div>-->
      <v-btn v-else @click="none">Свернуть</v-btn>
    </div>

    <template v-if="progressСircular">
      <v-container fluid>
        <v-row>
          <v-col cols="12">
            <div class="text-center">
              <v-progress-circular
                :size="50"
                color="primary"
                indeterminate
              ></v-progress-circular>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </template>
    <template v-else>
      <v-expansion-panels v-model="panel" multiple>
        <v-expansion-panel
          class="no-transition"
          v-for="(mort, i) in MORTGAGES_DATA"
          :key="i"
        >
          <template v-if="mort.is_visible">
            <v-expansion-panel-header class="py-0">
              <v-container class="py-0" fill-height fluid>
                <v-row align="center">
                  <v-col cols="6" sm="3" md="2" lg="2">
                    <div>
                      <v-img
                        :src="mort.bank.bank_logo"
                        max-width="120"
                        max-height="50"
                        contain
                      ></v-img>
                    </div>
                    <div v-if="mort.bank.preference_is_active">
                      <v-chip
                        small
                        color="cyan"
                        text-color="white"
                        class="mt-1"
                      >
                        <span
                          >Преференция
                          <b>{{ mort.bank.preference_value }}%</b></span
                        >
                      </v-chip>
                    </div>
                  </v-col>
                  <v-col cols="6" sm="3" md="3" lg="2">
                    <div class="mt-2">
                      <span class="grey--text text--darken-1 body-2"
                        >«{{ mort.bank.bank_name }}»
                      </span>
                    </div>
                    <div>
                      <span class="grey--text text--darken-3 body-2"
                        >«{{ mort.programs_name }}»
                      </span>
                    </div>
                  </v-col>
                  <v-col cols="6" sm="3" md="2" lg="2">
                    <div>
                      <span
                        class="grey--text text--darken-3 headline font-weight-black"
                        >{{ mort.rate }}%
                      </span>
                      <span class="text--secondary nowrap"
                        >{{ mort.first_payment }}% ПВ
                      </span>
                    </div>
                    <div class="mt-1" v-if="mort.rate_salary">
                      <v-chip
                        small
                        color="grey lighten-4"
                        text-color="grey darken-1"
                      >
                        <span
                          ><b>{{ mort.rate_salary }}%</b> зарплатникам</span
                        >
                      </v-chip>
                    </div>
                    <div></div>
                  </v-col>
                  <v-col cols="6" sm="6" md="3" lg="3" class="text--secondary">
                    <div>
                      <span
                        class="grey--text text--darken-3 subtitle-1 font-weight-black"
                        >{{ mort.min_sum_credit | numCredit | toRUB }} -
                        {{ mort.max_sum_credit | numCredit | toRUB }}
                      </span>
                    </div>
                    <div>
                      <span class="text--secondary caption"
                        >На срок от {{ mort.min_time_credit }} до
                        {{ mort.max_time_credit }} лет
                      </span>
                    </div>
                  </v-col>
                  <v-col cols="12" sm="6" md="2" lg="2" class="text--secondary">
                    <div>
                      <span class="text--secondary caption"
                        >Возраст от {{ mort.min_borrower_age }} до
                        {{ mort.max_borrower_age }} лет
                      </span>
                    </div>
                    <div>
                      <span class="text--secondary caption"
                        >Стаж от {{ mort.work_experience }} месяцев
                      </span>
                    </div>
                  </v-col>
                </v-row>
              </v-container>
            </v-expansion-panel-header>

            <v-expansion-panel-content>
              <v-divider></v-divider>

              <div class="py-0" fill-height fluid>
                <v-row align="start" justify="center" no-gutters>
                  <v-col cols="12" sm="6" md="3" lg="3" align="left">
                    <v-list-item>
                      <v-list-item-content class="grey--text text--darken-1">
                        <!--                    <v-list-item-title-->
                        <!--                      class="mb-3 body-1 font-weight-bold grey&#45;&#45;text text&#45;&#45;darken-3"-->
                        <!--                      >Условия ипотеки-->
                        <!--                    </v-list-item-title>-->
                        <span class="caption"
                          >Цель:
                          <span
                            v-for="(item, index) in mort.targets"
                            :key="index"
                          >
                            {{ item.target_name
                            }}{{ mort.targets.length !== index + 1 ? "," : "" }}
                          </span>
                        </span>
                        <!--                    <span class="caption"-->
                        <!--                      >Программа: «{{ mort.programs_name }}»-->
                        <!--                    </span>-->
                        <!--                    <span class="caption"-->
                        <!--                      >Первоначальный взнос: {{ mort.first_payment }}%-->
                        <!--                    </span>-->
                        <!--                    <span class="caption">Ставка: {{ mort.rate }}% </span>-->
                        <!--                    <span class="caption"-->
                        <!--                      >Ставка для зарплатников:-->
                        <!--                      {{-->
                        <!--                        !mort.rate_salary ? "-" : mort.rate_salary + "%"-->
                        <!--                      }}</span-->
                        <!--                    >-->
                        <!--                    <span class="caption"-->
                        <!--                      >Сумма: {{ mort.min_sum_credit | numCredit | toRUB }} - -->
                        <!--                      {{ mort.max_sum_credit | numCredit | toRUB }}-->
                        <!--                    </span>-->
                        <!--                    <span class="caption"-->
                        <!--                      >Срок: от {{ mort.min_time_credit }} до-->
                        <!--                      {{ mort.max_time_credit }} лет-->
                        <!--                    </span>-->
                        <span class="caption">
                          Занижение:
                          {{ mort.understatement_is_active ? "Да" : "Нет"
                          }}{{
                            mort.understatement_comment
                              ? ", " + mort.understatement_comment
                              : ""
                          }}
                        </span>
                        <span class="caption"
                          >Созаёмщики: {{ mort.co_borrowers }}
                        </span>
                        <span class="caption"
                          >Комиссия: {{ mort.commission }}
                        </span>
                        <span class="caption"
                          >Регистрация продавца:
                          {{ mort.seller_registration }}
                        </span>
                        <span class="caption"
                          >Экспресс выдача:
                          {{
                            mort.express_issue == "yes"
                              ? "Да"
                              : mort.express_issue == "no"
                              ? "Нет"
                              : ""
                          }}
                        </span>
                        <span class="caption"
                          >Включение детей в число собственников:
                          {{
                            mort.inclusion_children == "yes"
                              ? "Да"
                              : mort.inclusion_children == "no"
                              ? "Нет"
                              : ""
                          }}
                        </span>
                        <span class="caption"
                          >Стаж на последнем месте от:
                          {{ mort.work_experience }} месяцев
                        </span>
                        <span class="caption"
                          >Время на решение банка:
                          {{ mort.time_for_bank_decision }}
                        </span>
                      </v-list-item-content>
                    </v-list-item>
                  </v-col>
                  <v-col cols="12" sm="6" md="3" lg="3" align="left">
                    <v-list-item>
                      <v-list-item-content
                        class="caption grey--text text--darken-1"
                      >
                        <!--                    <v-list-item-title-->
                        <!--                      class="mb-3 body-1 font-weight-bold grey&#45;&#45;text text&#45;&#45;darken-3"-->
                        <!--                      >Условия ипотеки-->
                        <!--                    </v-list-item-title>-->

                        <span class="caption">
                          Комната:
                          {{
                            mort.room == "yes"
                              ? "Да"
                              : mort.room == "no"
                              ? "Нет"
                              : ""
                          }}{{
                            mort.room_comment ? ", " + mort.room_comment : ""
                          }}
                        </span>
                        <span class="caption">
                          Доля:
                          {{
                            mort.share == "yes"
                              ? "Да"
                              : mort.share == "no"
                              ? "Нет"
                              : ""
                          }}{{
                            mort.share_comment ? ", " + mort.share_comment : ""
                          }}
                        </span>
                        <span class="caption">
                          Частный дом:
                          {{
                            mort.private_house == "yes"
                              ? "Да"
                              : mort.private_house == "no"
                              ? "Нет"
                              : ""
                          }}{{
                            mort.private_comment
                              ? ", " + mort.private_comment
                              : ""
                          }}
                        </span>
                        <span class="caption">
                          Апартаменты:
                          {{
                            mort.apartments == "yes"
                              ? "Да"
                              : mort.apartments == "no"
                              ? "Нет"
                              : ""
                          }}{{
                            mort.apartments_comment
                              ? ", " + mort.apartments_comment
                              : ""
                          }}
                        </span>
                        <span class="caption">
                          Перепланировка:
                          {{
                            mort.redevelopment == "yes"
                              ? "Да"
                              : mort.redevelopment == "no"
                              ? "Нет"
                              : ""
                          }}{{
                            mort.redevelopment_comment
                              ? ", " + mort.redevelopment_comment
                              : ""
                          }}
                        </span>
                        <p class="caption mb-1">
                          Перекрытия:<span class="grey--text text--darken-3">
                            {{ mort.overlap }}
                          </span>
                        </p>
                        <p class="caption mb-1">
                          Этажность:<span class="grey--text text--darken-3">
                            {{ mort.storeys }}
                          </span>
                        </p>
                        <p class="caption mb-1">
                          Износ жилья:<span class="grey--text text--darken-3">
                            {{ mort.housing_wear }}
                          </span>
                        </p>
                        <p class="caption mb-1">
                          Технические документы:
                          <span class="grey--text text--darken-3">
                            {{ mort.req_tech_docs }}
                          </span>
                        </p>
                      </v-list-item-content>
                    </v-list-item>
                  </v-col>
                  <v-col cols="12" sm="6" md="3" lg="3" align="left">
                    <v-list-item>
                      <v-list-item-content class="grey--text text--darken-1">
                        <!--                        <template v-if="monthlyPayment(mort)">-->
                        <!--                          <div>-->
                        <!--                            {{ monthlyPayment(mort) | numCredit | toRUB }}/мес.-->
                        <!--                          </div>-->
                        <!--                        </template>-->

                        <p class="caption mb-1">
                          Обязательные документы:
                          <span class="grey--text text--darken-3">
                            {{ mort.mandatory_documents }}
                          </span>
                        </p>
                        <p class="caption mb-1">
                          Документ подтверждение дохода:
                          <span class="grey--text text--darken-3">
                            {{ mort.proof_of_income_document }}
                          </span>
                        </p>
                        <p class="caption mb-1">
                          Дополнительная информация:
                          <span class="grey--text text--darken-3">
                            {{ mort.add_info }}
                          </span>
                        </p>
                      </v-list-item-content>
                    </v-list-item>
                  </v-col>
                  <v-col cols="12" sm="6" md="3" lg="3" align="left">
                    <v-list-item>
                      <v-list-item-content class="grey--text text--darken-1">
                        <template v-if="monthlyPayment(mort)">
                          <div>
                            <div
                              v-for="(pay, k, i) in monthlyPayment(mort)"
                              :key="i"
                            >
                              <template v-if="k === 'monthly_pay'">
                                <span>Ежемесячный платеж</span>
                                <p
                                  class="grey--text text--darken-1 headline font-weight-black"
                                >
                                  {{ pay | numCredit | toRUB }}/мес.
                                </p>
                              </template>
                              <template
                                v-if="k === 'preference_pay' && pay !== 'NaN'"
                              >
                                <span>С преференцией</span>
                                <p
                                  class="grey--text text--darken-1 headline font-weight-black"
                                >
                                  {{ pay | numCredit | toRUB }}/мес.
                                </p>
                              </template>
                              <template
                                v-if="k === 'salary_pay' && pay !== 'NaN'"
                              >
                                <span>Для зарплатников</span>
                                <p
                                  class="grey--text text--darken-1 headline font-weight-black"
                                >
                                  {{ pay | numCredit | toRUB }}/мес.
                                </p>
                              </template>
                            </div>
                          </div>
                        </template>
                        <template v-else>
                          <v-alert text color="grey lighten-1">
                            <v-list-item-content>
                              <p class="body-2">
                                Для расчёта ежемесечного платежа введите
                                подходящие для этой программы значения.
                              </p>
                              <p class="caption mb-1">
                                - Стоимость недвижимости
                              </p>
                              <p class="caption mb-1">- Первоначальный взнос</p>
                              <p class="caption mb-1">- Срок</p>
                            </v-list-item-content>
                          </v-alert>
                        </template>
                      </v-list-item-content>
                    </v-list-item>
                  </v-col>
                </v-row>
              </div>
            </v-expansion-panel-content>
          </template>
        </v-expansion-panel>
      </v-expansion-panels>
    </template>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";

export default {
  name: "MortgageSearchComp",

  data() {
    return {
      progressСircular: false,
      url: "api/v1/mortgages/all/",
      filters: [],
      selectTargets: ["Foo", "Bar", "Fizz", "Buzz"],
      panel: [],
      showFullMortgage: true,
      visibleSearch: false,
      num_first_payment: "",
      procent_first_payment: "",
      progMonthlyPayment: ""
    };
  },
  computed: {
    ...mapState("mortgages", [
      "MORTGAGES_DATA",
      "BANKS_NAME_DATA",
      "TARGET_CREDITS_NAME_DATA"
    ])
  },
  methods: {
    ...mapMutations("mortgages", [
      "SET_UPDATE_MORTGAGES_DATA",
      "SET_UPDATE_BANKS_NAME_DATA",
      "SET_UPDATE_TARGET_CREDITS_NAME_DATA"
    ]),
    ...mapActions("mortgages", [
      "FETCH_MORTGAGES",
      "FETCH_BANKS",
      "FETCH_TARGET_CREDITS"
    ]),
    toggleSearch() {
      this.visibleSearch = !this.visibleSearch;
    },

    // Create an array the length of our items
    // with all values as true
    all() {
      this.panel = [...Array(this.MORTGAGES_DATA.length).keys()].map(
        (k, i) => i
      );
      this.showFullMortgage = !this.showFullMortgage;
    },
    // Reset the panel
    none() {
      this.panel = [];
      this.showFullMortgage = !this.showFullMortgage;
    },
    clearFilter() {
      this.filters = [];
      this.num_first_payment = "";
      this.procent_first_payment = "";
      this.progressСircular = true;
      this.FETCH_MORTGAGES()
        .then(() => {
          this.progressСircular = false;
        })
        .catch(() => {
          this.progressСircular = false;
        });
      return this.filters;
    },
    filterMortgages() {
      const params = new URLSearchParams();
      for (let item in this.filters) {
        if (this.filters[item] !== "" && this.filters[item] !== null) {
          params.append(item, this.filters[item]);
        }
        // console.log(this.filters[item]);
      }
      // this.fetchMortgages(this.url, params);
      this.progressСircular = true;
      this.FETCH_MORTGAGES(params)
        .then(() => {
          this.progressСircular = false;
        })
        .catch(() => {
          this.progressСircular = false;
        });
      // console.log(this.BANKS_DATA);
      if (!this.showFullMortgage) {
        this.none();
      }
    },
    funcMontPay(rate, pref = 0) {
      let monthly_procent = (rate - pref) / 100 / 12;
      let tmp = Math.pow(1 + monthly_procent, this.filters.time_credit * 12);
      let monthlyPay =
        (Number(this.filters.property_value.replace(/\s+/g, "")) -
          Number(this.num_first_payment.replace(/\s+/g, ""))) *
        monthly_procent *
        (tmp / (tmp - 1));

      return monthlyPay;
    },
    monthlyPayment(mort) {
      // console.log(mort);
      // https://mortgage-calculator.ru/%D1%84%D0%BE%D1%80%D0%BC%D1%83%D0%BB%D0%B0-%D1%80%D0%B0%D1%81%D1%87%D0%B5%D1%82%D0%B0-%D0%B8%D0%BF%D0%BE%D1%82%D0%B5%D0%BA%D0%B8
      if (
        // проверка на "!== undefined" должна стоять выше чем ".replace", а то будет ошибка !!!
        this.filters.property_value !== undefined &&
        this.filters.time_credit !== undefined &&
        this.num_first_payment !== "" &&
        this.filters.property_value !== "" &&
        this.filters.time_credit !== "" &&
        Number(this.num_first_payment.replace(/\s+/g, "")) <=
          Number(this.filters.property_value.replace(/\s+/g, "")) &&
        this.filters.first_payment >= mort.first_payment &&
        Number(this.filters.property_value.replace(/\s+/g, "")) >=
          mort.min_sum_credit &&
        Number(this.filters.property_value.replace(/\s+/g, "")) <=
          mort.max_sum_credit &&
        this.filters.time_credit >= mort.min_time_credit &&
        this.filters.time_credit <= mort.max_time_credit
      ) {
        // console.log(this.filters.time_credit);
        // let monthly_procent = mort.rate / 100 / 12;
        // let tmp = Math.pow(1 + monthly_procent, this.filters.time_credit * 12);
        // let monthlyPay =
        //   (Number(this.filters.property_value.replace(/\s+/g, "")) -
        //     Number(this.num_first_payment.replace(/\s+/g, ""))) *
        //   monthly_procent *
        //   (tmp / (tmp - 1));

        let data = new Object();
        data["monthly_pay"] = this.funcMontPay(mort.rate).toFixed(2);
        if (mort.bank.preference_value !== null) {
          data["preference_pay"] = this.funcMontPay(
            mort.rate,
            mort.bank.preference_value
          ).toFixed(2);
        }
        data["salary_pay"] = this.funcMontPay(mort.rate_salary).toFixed(2);
        // console.log(data);
        return data;
        // return monthlyPay.toFixed(2);
      } else if (
        this.num_first_payment === "" ||
        this.filters.property_value === ""
      ) {
        return false;
      }
    },
    thousandSeparator(newValue) {
      let v = newValue.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, " ");
      // console.log("thousandSeparator => " + v);
      return v;
    },
    watchValue() {
      // console.log(this.filters.property_value);
      if (
        this.filters.property_value !== undefined &&
        this.num_first_payment !== ""
      ) {
        this.filters.first_payment = Math.floor(
          (Number(this.num_first_payment.replace(/\s+/g, "")) * 100) /
            Number(this.filters.property_value.replace(/\s+/g, ""))
        );
        let pr =
          (Number(this.num_first_payment.replace(/\s+/g, "")) * 100) /
          Number(this.filters.property_value.replace(/\s+/g, ""));
        if (pr >= 0 && pr <= 100) {
          this.procent_first_payment = pr.toFixed(2) + "%";
        } else {
          this.procent_first_payment = "";
        }
      } else {
        this.procent_first_payment = "";
        // console.log("watchValue => ");
      }
    }
  },
  created() {
    this.FETCH_MORTGAGES();
    this.FETCH_BANKS();
    this.FETCH_TARGET_CREDITS();
  },
  mounted() {},
  filters: {
    numCredit(value) {
      return new Intl.NumberFormat().format(value);
    },
    toRUB(value) {
      return `${value.toLocaleString()} ₽`;
    }
  },
  watch: {
    "filters.property_value": {
      handler: function(newValue) {
        if (newValue === "" || newValue === undefined) {
          this.filters.first_payment = "";
          this.procent_first_payment = "";
          return true;
        }
        this.filters.property_value = this.thousandSeparator(newValue);
        this.watchValue();
      },
      deep: true
    },
    num_first_payment: function(newValue) {
      if (newValue === "" || newValue === undefined) {
        this.filters.first_payment = "";
        this.procent_first_payment = "";
        return true;
      }
      this.num_first_payment = this.thousandSeparator(newValue);
      // console.log("watch => " + this.num_first_payment);
      // console.log(Number(this.filters.property_value));
      this.watchValue();
    }
    // "filters.time_credit": {
    //   // eslint-disable-next-line no-unused-vars
    //   handler: function(v) {
    //     // console.log(v);
    //     this.filterMortgages();
    //     // return this.clearAlertBox();
    //   },
    //   deep: true
    // }
  }
};
</script>

<style scoped>
/* Убираем анимацию у v-expansion-panel (ТОРМОЗИТ сильно!)*/
.no-transition {
  transition: none !important;
}
.v-item-group,
.v-expansion-panel-header,
.v-expansion-panel::before,
.v-expansion-panel-header:before,
.expand-transition-leave-active,
.expand-transition-enter-active {
  transition: none !important;
}
.nowrap {
  white-space: nowrap;
}
</style>
