<template>
  <v-card>
    <v-card-title class="my-0">
      <v-container fluid>
        <v-row>
          <v-col cols="12" sm="3" md="3">
            Программы
          </v-col>
          <v-col cols="12" sm="9" md="5">
            <v-text-field
              v-model="search"
              label="Отфильтровать"
              single-line
              dense
              clearable
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="12" md="4">
            <div class="float-right">
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
                    <v-card-title class="pb-0">
                      <v-container class="pb-0">
                        <v-row>
                          <v-col cols="12" sm="6">
                            <div>
                              <span class="headline">{{ formTitle }}</span>
                            </div>
                          </v-col>
                          <v-col cols="12" sm="6">
                            <div class="float-right">
                              <v-checkbox
                                v-model="editedItem.is_visible"
                                label="Отображать"
                                color="primary"
                              ></v-checkbox>
                            </div>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-title>

                    <v-card-text>
                      <v-container>
                        <v-row class="mb-7">
                          <v-col cols="12" sm="12" md="5">
                            <v-text-field
                              v-model="editedItem.programs_name"
                              label="Название программы"
                              placeholder=" "
                              @blur="$v.editedItem.programs_name.$touch()"
                              :error-messages="nameErrors"
                            ></v-text-field>
                            <v-select
                              label="Банк"
                              placeholder=" "
                              :items="GET_BANKS_ALL_DATA"
                              item-text="bank_name"
                              item-value="id"
                              v-model="editedItem.programs_bank"
                            >
                            </v-select>
                          </v-col>
                          <v-col cols="12" sm="4" md="2">
                            <v-text-field
                              v-model.number="editedItem.rate"
                              label="Ставка"
                              placeholder=" "
                              suffix="%"
                              :rules="[numberRule]"
                            ></v-text-field>
                            <v-text-field
                              v-model.number="editedItem.rate_salary"
                              label="Ставка зарплатникам"
                              placeholder=" "
                              suffix="%"
                              :rules="[numberRule]"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="4" md="2">
                            <v-text-field
                              v-model.number="editedItem.first_payment"
                              label="Первоначальный взнос"
                              placeholder=" "
                              suffix="%"
                              :rules="[numberRule]"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="3">
                            <v-select
                              multiple
                              label="Цель кредита"
                              placeholder=" "
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
                                  {{ editedItem.programs_target.length }}
                                  шт.</span
                                >
                              </template>
                            </v-select>
                          </v-col>
                        </v-row>
                        <v-row class="mb-7">
                          <v-col cols="12" sm="4" md="3">
                            <v-text-field
                              v-model.number="editedItem.min_sum_credit"
                              label="Мин. сумма кредита"
                              placeholder=" "
                              suffix="₽"
                              :rules="[numberRule]"
                            ></v-text-field>
                            <v-text-field
                              v-model.number="editedItem.max_sum_credit"
                              label="Макс. сумма кредита"
                              placeholder=" "
                              suffix="₽"
                              :rules="[numberRule]"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="4" md="3">
                            <v-text-field
                              v-model.number="editedItem.min_time_credit"
                              label="Мин. срок кредита"
                              placeholder=" "
                              suffix="лет"
                              :rules="[numberRule]"
                            ></v-text-field>
                            <v-text-field
                              v-model.number="editedItem.max_time_credit"
                              label="Макс. срок кредита"
                              placeholder=" "
                              suffix="лет"
                              :rules="[numberRule]"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="4" md="3">
                            <v-text-field
                              v-model.number="editedItem.min_borrower_age"
                              label="Мин. возраст заёмщика"
                              placeholder=" "
                              suffix="лет"
                              :rules="[numberRule]"
                            ></v-text-field>
                            <v-text-field
                              v-model.number="editedItem.max_borrower_age"
                              label="Макс. возраст заёмщика"
                              placeholder=" "
                              suffix="лет"
                              :rules="[numberRule]"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                        <v-row class="mb-7">
                          <v-col cols="12" sm="4" md="3">
                            <v-text-field
                              v-model.number="editedItem.work_experience"
                              label="Стаж на последнем месте"
                              placeholder=" "
                              suffix="мес."
                              :rules="[numberRule]"
                            ></v-text-field>
                            <v-text-field
                              v-model="editedItem.time_for_bank_decision"
                              label="Время на решение банка"
                              placeholder="от 2 до 5 дней"
                            ></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="4" md="5">
                            <v-textarea
                              v-model="editedItem.mandatory_documents"
                              label="Обязательные документы"
                              placeholder=" "
                              auto-grow
                              rows="1"
                            ></v-textarea>
                          </v-col>
                          <v-col cols="12" sm="4" md="4">
                            <v-textarea
                              v-model="editedItem.proof_of_income_document"
                              label="Документ подтверждение дохода"
                              placeholder=" "
                              auto-grow
                              rows="1"
                            ></v-textarea>
                          </v-col>
                        </v-row>
                        <v-row class="mb-7">
                          <v-col cols="12" sm="4" md="4">
                            <v-checkbox
                              v-model="editedItem.understatement_is_active"
                              label="Занижение, Есть/нет"
                              color="primary"
                            ></v-checkbox>
                          </v-col>
                          <v-col cols="12" sm="4" md="8">
                            <v-textarea
                              v-model="editedItem.understatement_comment"
                              label="Комментарий к занижению"
                              placeholder=" "
                              auto-grow
                              rows="1"
                            ></v-textarea>
                          </v-col>
                        </v-row>
                        <v-row class="mb-7">
                          <v-col cols="12" sm="4" md="4">
                            <v-textarea
                              v-model="editedItem.co_borrowers"
                              label="Созаемщики"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
                          </v-col>
                          <v-col cols="12" sm="4" md="4">
                            <v-textarea
                              v-model="editedItem.commission"
                              label="Комиссия"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
                          </v-col>
                          <v-col cols="12" sm="4" md="4">
                            <v-textarea
                              v-model="editedItem.seller_registration"
                              label="Регистрация продавца"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
                          </v-col>
                        </v-row>
                        <v-row class="mb-7">
                          <v-col cols="12" sm="4" md="4">
                            <v-select
                              v-model="editedItem.express_issue"
                              :items="itemsYesNo"
                              item-text="text"
                              item-value="value"
                              label="Экспресс выдача"
                              dense
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="4" md="6">
                            <v-select
                              v-model="editedItem.inclusion_children"
                              :items="itemsYesNo"
                              item-text="text"
                              item-value="value"
                              label="Включение детей в число собственников"
                              dense
                            ></v-select>
                          </v-col>
                        </v-row>
                        <v-row class="mb-7">
                          <v-col cols="12" sm="4" md="3">
                            <v-select
                              v-model="editedItem.room"
                              :items="itemsYesNo"
                              item-text="text"
                              item-value="value"
                              label="Комната"
                              dense
                            ></v-select>
                            <v-textarea
                              v-model="editedItem.room_comment"
                              label="Комментарий к Комната"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
                          </v-col>
                          <v-col cols="12" sm="4" md="3">
                            <v-select
                              v-model="editedItem.share"
                              :items="itemsYesNo"
                              item-text="text"
                              item-value="value"
                              label="Доля"
                              dense
                            ></v-select>
                            <v-textarea
                              v-model="editedItem.share_comment"
                              label="Комментарий к Доля"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
                          </v-col>
                          <v-col cols="12" sm="4" md="3">
                            <v-select
                              v-model="editedItem.private_house"
                              :items="itemsYesNo"
                              item-text="text"
                              item-value="value"
                              label="Частный дом"
                              dense
                            ></v-select>
                            <v-textarea
                              v-model="editedItem.private_comment"
                              label="Комментарий к Частный дом"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
                          </v-col>
                          <v-col cols="12" sm="4" md="3">
                            <v-select
                              v-model="editedItem.apartments"
                              :items="itemsYesNo"
                              item-text="text"
                              item-value="value"
                              label="Апартаменты"
                              dense
                            ></v-select>
                            <v-textarea
                              v-model="editedItem.apartments_comment"
                              label="Комментарий к Апартаменты"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
                          </v-col>
                        </v-row>
                        <v-row class="mb-7">
                          <v-col cols="12" sm="4" md="4">
                            <v-select
                              v-model="editedItem.redevelopment"
                              :items="itemsYesNo"
                              item-text="text"
                              item-value="value"
                              label="Перепланировка"
                              dense
                            ></v-select>
                          </v-col>
                          <v-col cols="12" sm="4" md="8">
                            <v-textarea
                              v-model="editedItem.redevelopment_comment"
                              label="Комментарий к Перепланировка"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
                          </v-col>
                        </v-row>
                        <v-row class="mb-7">
                          <v-col cols="12" sm="4" md="3">
                            <v-textarea
                              v-model="editedItem.overlap"
                              label="Перекрытия"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
                          </v-col>
                          <v-col cols="12" sm="4" md="3">
                            <v-textarea
                              v-model="editedItem.storeys"
                              label="Этажность"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
                          </v-col>
                          <v-col cols="12" sm="4" md="3">
                            <v-textarea
                              v-model="editedItem.housing_wear"
                              label="Износ жилья"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
                          </v-col>
                          <v-col cols="12" sm="4" md="3">
                            <v-textarea
                              v-model="editedItem.req_tech_docs"
                              label="Требования к тех. документам"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col cols="12" sm="12" md="12">
                            <v-textarea
                              v-model="editedItem.add_info"
                              label="Дополнительная информация"
                              placeholder=" "
                              auto-grow
                              rows="1"
                              dense
                            ></v-textarea>
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
                      <v-btn color="blue darken-1" text @click="close"
                        >Отмена</v-btn
                      >
                      <v-btn color="blue darken-1" text type="submit"
                        >Сохранить</v-btn
                      >
                    </v-card-actions>
                  </v-card>
                </form>
              </v-dialog>
              <v-dialog v-model="dialogCopyItem" max-width="500px">
                <v-card>
                  <v-card-title>
                    <span class="headline">Дублирование программы</span>
                  </v-card-title>
                  <v-card-text>
                    <v-container>
                      <v-row>
                        Вы действительно хотите дублировать эту программу?
                      </v-row>
                    </v-container>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close"
                      >Отмена</v-btn
                    >
                    <v-btn color="blue darken-1" text @click="copyMortgage"
                      >Дублировать</v-btn
                    >
                  </v-card-actions>
                </v-card>
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
                    <v-btn color="blue darken-1" text @click="close"
                      >Отмена</v-btn
                    >
                    <v-btn color="red darken-1 white--text" @click="deleteBank"
                      >Удалить</v-btn
                    >
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-card-title>
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
          max-width="80"
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
      <template v-slot:item.is_visible="{ item }">
        <v-icon v-if="item.is_visible" color="green darken-2"
          >mdi-checkbox-marked-circle</v-icon
        >
      </template>
      <template v-slot:item.date_modified="{ item }">
        <span> {{ item.date_modified | normDate }} </span>
      </template>

      <!--      <template v-slot:top>-->
      <!--        <v-toolbar flat color="white">-->
      <!--          <v-toolbar-title>Кредитные программы</v-toolbar-title>-->
      <!--          &lt;!&ndash;                <v-divider class="mx-4" inset vertical></v-divider>&ndash;&gt;-->
      <!--          <v-spacer></v-spacer>-->
      <!--          <v-text-field-->
      <!--            v-model="search"-->
      <!--            label="Поиск"-->
      <!--            single-line-->
      <!--            clearable-->
      <!--          ></v-text-field>-->
      <!--          <v-spacer></v-spacer>-->
      <!--          <v-dialog persistent v-model="dialog" max-width="1000px">-->
      <!--            <template v-slot:activator="{ on }">-->
      <!--              <v-btn-->
      <!--                color="primary"-->
      <!--                dark-->
      <!--                class="mb-2"-->
      <!--                v-on="on"-->
      <!--                @click="editItem()"-->
      <!--                >Добавить программу</v-btn-->
      <!--              >-->
      <!--            </template>-->
      <!--            <form @submit.prevent="save">-->
      <!--              <v-card>-->
      <!--                <v-card-title>-->
      <!--                  <span class="headline">{{ formTitle }}</span>-->
      <!--                </v-card-title>-->

      <!--                <v-card-text>-->
      <!--                  <v-container>-->
      <!--                    <v-row>-->
      <!--                      <v-col cols="12" sm="12" md="4">-->
      <!--                        <v-select-->
      <!--                          label="Банк"-->
      <!--                          placeholder="Любой"-->
      <!--                          :items="GET_BANKS_ALL_DATA"-->
      <!--                          item-text="bank_name"-->
      <!--                          item-value="id"-->
      <!--                          v-model="editedItem.programs_bank"-->
      <!--                        >-->
      <!--                        </v-select>-->
      <!--                      </v-col>-->

      <!--                      <v-col cols="12" sm="12" md="4">-->
      <!--                        <v-text-field-->
      <!--                          v-model="editedItem.programs_name"-->
      <!--                          label="Название программы"-->
      <!--                          @blur="$v.editedItem.programs_name.$touch()"-->
      <!--                          :error-messages="nameErrors"-->
      <!--                        ></v-text-field>-->
      <!--                      </v-col>-->

      <!--                      <v-col cols="12" sm="4" md="2">-->
      <!--                        <v-text-field-->
      <!--                          v-model="editedItem.rate"-->
      <!--                          label="Ставка"-->
      <!--                        ></v-text-field>-->
      <!--                      </v-col>-->
      <!--                      <v-col cols="12" sm="4" md="2">-->
      <!--                        <v-text-field-->
      <!--                          v-model="editedItem.rate_salary"-->
      <!--                          label="Ставка зарплатникам"-->
      <!--                        ></v-text-field>-->
      <!--                      </v-col>-->
      <!--                      <v-col cols="12" sm="4" md="2">-->
      <!--                        <v-text-field-->
      <!--                          v-model="editedItem.first_payment"-->
      <!--                          label="Первый взнос"-->
      <!--                        ></v-text-field>-->
      <!--                      </v-col>-->

      <!--                      <v-col cols="12" sm="12" md="4">-->
      <!--                        <v-select-->
      <!--                          multiple-->
      <!--                          label="Цель кредита"-->
      <!--                          placeholder="Любой"-->
      <!--                          :items="GET_TARGET_CREDITS_ALL_DATA"-->
      <!--                          item-text="target_name"-->
      <!--                          item-value="id"-->
      <!--                          v-model="editedItem.programs_target"-->
      <!--                        >-->
      <!--                          <template v-slot:selection="{ item, index }">-->
      <!--                            &lt;!&ndash;                  <span v-if="index === 0">&ndash;&gt;-->
      <!--                            &lt;!&ndash;                    <span>{{ item }} </span>&ndash;&gt;-->
      <!--                            &lt;!&ndash;                  </span>&ndash;&gt;-->
      <!--                            <span-->
      <!--                              v-if="index === 0"-->
      <!--                              class="ml-1 grey&#45;&#45;text caption"-->
      <!--                              >Выбранно-->
      <!--                              {{ editedItem.programs_target.length }} шт.</span-->
      <!--                            >-->
      <!--                          </template>-->
      <!--                        </v-select>-->
      <!--                      </v-col>-->
      <!--                    </v-row>-->
      <!--                    <v-row>-->
      <!--                      <v-col>-->
      <!--                        <div v-if="errMsgBank">-->
      <!--                          &lt;!&ndash;                        <div v-for="(errRow, i) in errMsgBank" :key="i">&ndash;&gt;-->
      <!--                          &lt;!&ndash;                          <div v-for="(err, i) in errRow" :key="i">&ndash;&gt;-->
      <!--                          <v-alert width="100%" type="error">-->
      <!--                            {{ errMsgBank }}-->
      <!--                          </v-alert>-->
      <!--                          &lt;!&ndash;                          </div>&ndash;&gt;-->
      <!--                          &lt;!&ndash;                        </div>&ndash;&gt;-->
      <!--                        </div>-->
      <!--                      </v-col>-->
      <!--                    </v-row>-->
      <!--                  </v-container>-->
      <!--                </v-card-text>-->

      <!--                <v-card-actions>-->
      <!--                  <v-spacer></v-spacer>-->
      <!--                  <v-btn color="blue darken-1" text @click="close"-->
      <!--                    >Отмена</v-btn-->
      <!--                  >-->
      <!--                  <v-btn color="blue darken-1" text type="submit"-->
      <!--                    >Сохранить</v-btn-->
      <!--                  >-->
      <!--                </v-card-actions>-->
      <!--              </v-card>-->
      <!--            </form>-->
      <!--          </v-dialog>-->

      <!--          <v-dialog v-model="dialogDelete" max-width="500px">-->
      <!--            <v-card>-->
      <!--              <v-card-title>-->
      <!--                <span class="headline">Удаление программы</span>-->
      <!--              </v-card-title>-->

      <!--              <v-card-text>-->
      <!--                <v-container>-->
      <!--                  <v-row>-->
      <!--                    Будте внимательны! Вы действительно хотите удалить эту-->
      <!--                    программу?-->
      <!--                  </v-row>-->
      <!--                </v-container>-->
      <!--              </v-card-text>-->

      <!--              <v-card-actions>-->
      <!--                <v-spacer></v-spacer>-->
      <!--                <v-btn color="blue darken-1" text @click="closeDialogDelete"-->
      <!--                  >Отмена</v-btn-->
      <!--                >-->
      <!--                <v-btn color="red darken-1 white&#45;&#45;text" @click="deleteBank"-->
      <!--                  >Удалить</v-btn-->
      <!--                >-->
      <!--              </v-card-actions>-->
      <!--            </v-card>-->
      <!--          </v-dialog>-->

      <!--        </v-toolbar>-->
      <!--      </template>-->

      <template v-slot:item.action="{ item }">
        <v-icon class="mr-2" @click="copyItem(item)">
          mdi-content-copy
        </v-icon>

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
  </v-card>
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
    numberRule: v => {
      if (v === undefined || v === null) return true;
      if ((!isNaN(parseFloat(v)) && v >= 0) || v === "") return true;
      return "Введите число.";
    },
    dialog: false,
    dialogCopyItem: false,
    dialogDelete: false,
    search: "",
    headers: [
      {
        width: "8%",
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
      { text: "Название программы", width: "20%", value: "programs_name" },
      {
        text: "Ставка",
        width: "8%",
        align: "center",
        value: "rate"
      },
      {
        text: "Ставка зарплатникам",
        width: "8%",
        align: "center",
        value: "rate_salary"
      },
      {
        text: "ПВ",
        width: "8%",
        align: "center",
        value: "first_payment"
      },
      {
        text: "Отображать",
        width: "5%",
        align: "center",
        value: "is_visible"
      },
      {
        text: "Дата изменения",
        width: "5%",
        align: "center",
        value: "date_modified"
      },
      {
        text: "Действия",
        align: "right",
        width: "15%",
        value: "action",
        sortable: false
      }
    ],
    listProgram: [],
    editedIndex: -1,
    editedItem: {},
    defaultItem: {},
    errMsgFieldBankName: null,
    errMsgBank: null,
    itemsYesNo: [
      { text: "-", value: "" },
      { text: "Да", value: "yes" },
      { text: "Нет", value: "no" }
    ]
  }),

  computed: {
    ...mapState("mortgages", ["BANKS_NAME_DATA", "MORTGAGES_DATA"]),
    ...mapGetters("mortgages", [
      "GET_BANKS_ALL_DATA",
      "GET_TARGET_CREDITS_ALL_DATA",
      "GET_MORTGAGES_DATA"
    ]),
    ...mapGetters("user_info", ["GET_USER_INFO_DATA"]),
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
    this.FETCH_MORTGAGES_CRUD()
      // eslint-disable-next-line no-unused-vars
      .then(response => {
        // console.log("response " + response);
        // this.listProgram = response.data;
        this.listProgram = this.GET_MORTGAGES_DATA;
      })
      .catch(() => {
        this.$store.dispatch("refreshToken").then(() => {
          this.FETCH_MORTGAGES_CRUD().then(() => {
            this.listProgram = this.GET_MORTGAGES_DATA;
          });
        });
      });
    // this.initialize();
  },
  filters: {
    normDate(value) {
      const date = new Date(value);
      let year, month, day, h, m, s;
      year = date.getFullYear();
      month = date.getMonth() + 1;
      day = date.getDate();
      h = date.getHours();
      m = date.getMinutes();
      s = date.getSeconds();
      const correct_date = day + "." + month + "." + year + " " + h + ":" + m + ":" + s;
      return correct_date;
    }
  },
  methods: {
    ...mapActions("mortgages", [
      "FETCH_BANKS",
      "FETCH_TARGET_CREDITS",
      "FETCH_MORTGAGES_CRUD",
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
      // console.log(this.editedItem);
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

    copyItem(item) {
      this.editedIndex = this.listProgram.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.editedItem.programs_name =
        this.editedItem.programs_name + " (Копия)";
      // let val = "create";
      // this.submitForm(val);
      this.dialogCopyItem = true;
    },
    copyMortgage() {
      let val = "create";
      this.submitForm(val);
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
          this.FETCH_MORTGAGES_CRUD()
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
              this.FETCH_MORTGAGES_CRUD()
                // eslint-disable-next-line no-unused-vars
                .then(response => {
                  this.listProgram = this.GET_MORTGAGES_DATA;
                });
            });
          });
        });

      this.close();
    },

    close() {
      this.dialog = false;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
      this.errMsgBank = null;

      this.dialogCopyItem = false;
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

      let formData = new Object();
      formData["is_visible"] = this.editedItem.is_visible;
      formData["programs_bank"] = this.editedItem.programs_bank;
      formData["programs_name"] = this.editedItem.programs_name;
      formData["rate"] = this.editedItem.rate;

      if (this.editedItem.rate_salary === "") {
        formData["rate_salary"] = null;
      } else {
        formData["rate_salary"] = this.editedItem.rate_salary;
      }

      formData["first_payment"] = this.editedItem.first_payment;
      formData["programs_target"] = this.editedItem.programs_target;
      formData["min_sum_credit"] = this.editedItem.min_sum_credit;
      formData["max_sum_credit"] = this.editedItem.max_sum_credit;
      formData["min_time_credit"] = this.editedItem.min_time_credit;
      formData["max_time_credit"] = this.editedItem.max_time_credit;
      formData["min_borrower_age"] = this.editedItem.min_borrower_age;
      formData["max_borrower_age"] = this.editedItem.max_borrower_age;
      formData["work_experience"] = this.editedItem.work_experience;
      formData[
        "time_for_bank_decision"
      ] = this.editedItem.time_for_bank_decision;
      formData["mandatory_documents"] = this.editedItem.mandatory_documents;
      formData[
        "proof_of_income_document"
      ] = this.editedItem.proof_of_income_document;
      formData[
        "understatement_is_active"
      ] = this.editedItem.understatement_is_active;
      formData[
        "understatement_comment"
      ] = this.editedItem.understatement_comment;
      formData["co_borrowers"] = this.editedItem.co_borrowers;
      formData["commission"] = this.editedItem.commission;
      formData["seller_registration"] = this.editedItem.seller_registration;
      formData["express_issue"] = this.editedItem.express_issue;
      formData["inclusion_children"] = this.editedItem.inclusion_children;
      formData["room"] = this.editedItem.room;
      formData["room_comment"] = this.editedItem.room_comment;
      formData["share"] = this.editedItem.share;
      formData["share_comment"] = this.editedItem.share_comment;
      formData["private_house"] = this.editedItem.private_house;
      formData["private_comment"] = this.editedItem.private_comment;
      formData["apartments"] = this.editedItem.apartments;
      formData["apartments_comment"] = this.editedItem.apartments_comment;
      formData["redevelopment"] = this.editedItem.redevelopment;
      formData["redevelopment_comment"] = this.editedItem.redevelopment_comment;
      formData["overlap"] = this.editedItem.overlap;
      formData["storeys"] = this.editedItem.storeys;
      formData["housing_wear"] = this.editedItem.housing_wear;
      formData["req_tech_docs"] = this.editedItem.req_tech_docs;
      formData["add_info"] = this.editedItem.add_info;

      // console.log(typeof this.editedItem.preference_value);
      // console.log(formData);

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
            this.FETCH_MORTGAGES_CRUD()
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
            // console.log(error.config);
            this.$store.dispatch("refreshToken").then(() => {
              this.FETCH_EDIT_MORTGAGES(payload)
                // eslint-disable-next-line no-unused-vars
                .then(response => {
                  // console.log("qqqq " + response);
                  // записываем изменённые данные в таблицу на странице под нужным индексом элемента
                  // Object.assign(this.listProgram[this.editedIndex], response.data);

                  this.FETCH_MORTGAGES_CRUD()
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
            this.FETCH_MORTGAGES_CRUD()
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
                  this.FETCH_MORTGAGES_CRUD()
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
