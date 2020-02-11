<template>
  <v-app id="inspire" class="app-main-layout">
    <!--    Navbar-->
    <v-app-bar
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      app
      color="blue darken-3"
      dark
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <!--      <v-toolbar-title style="width: 300px" class="ml-0 pl-4">-->
      <!--        <span class="hidden-sm-and-down">Dashboard</span>-->
      <!--      </v-toolbar-title>-->
      <!--      <v-text-field-->
      <!--        flat-->
      <!--        solo-inverted-->
      <!--        hide-details-->
      <!--        prepend-inner-icon="mdi-magnify"-->
      <!--        label="Search"-->
      <!--        class="hidden-sm-and-down"-->
      <!--      />-->
      <v-spacer />
      <v-btn icon>
        <v-icon>mdi-apps</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-bell</v-icon>
      </v-btn>

      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-account-circle</v-icon>
          </v-btn>
        </template>

        <!--        <v-list>-->
        <!--          <v-list>-->
        <!--            <v-list-item>-->
        <!--              <v-list-item-avatar>-->
        <!--                <img-->
        <!--                  src="https://cdn.vuetifyjs.com/images/john.jpg"-->
        <!--                  alt="John"-->
        <!--                />-->
        <!--              </v-list-item-avatar>-->

        <!--              <v-list-item-content>-->
        <!--                <v-list-item-title>John Leider</v-list-item-title>-->
        <!--                <v-list-item-subtitle-->
        <!--                  >Founder of Vuetify.js</v-list-item-subtitle-->
        <!--                >-->
        <!--              </v-list-item-content>-->
        <!--            </v-list-item>-->
        <!--          </v-list>-->

        <!--          <v-divider></v-divider>-->

        <!--          <v-list-item v-for="(item, index) in itemsUserIcon" :key="index">-->
        <!--            <v-list-item-title>{{ item.title }}</v-list-item-title>-->
        <!--          </v-list-item>-->
        <!--          <v-list-item>-->
        <!--            <v-list-item-title>Выход</v-list-item-title>-->
        <!--          </v-list-item>-->
        <!--        </v-list>-->

        <template>
          <v-card width="256" class="mx-auto">
            <v-list>
              <v-list-item>
                <v-list-item-avatar>
                  <!--                  <img-->
                  <!--                    src="https://cdn.vuetifyjs.com/images/john.jpg"-->
                  <!--                    alt="John"-->
                  <!--                  />-->
                  <v-icon large>mdi-account-circle</v-icon>
                </v-list-item-avatar>
                <v-list-item-content align="left">
                  <v-list-item-title class="title">
                    {{ GET_USER_INFO_DATA.username }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    subtext
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>

              <v-divider></v-divider>

              <v-list dense nav>
                <!--                <v-list-item-->
                <!--                  v-for="item in itemsUserIcon"-->
                <!--                  :key="item.title"-->
                <!--                  :to="item.url"-->
                <!--                  link-->
                <!--                >-->
                <!--                  <v-list-item-icon>-->
                <!--                    <v-icon>{{ item.icon }}</v-icon>-->
                <!--                  </v-list-item-icon>-->

                <!--                  <v-list-item-content align="left">-->
                <!--                    <v-list-item-title>{{ item.title }}</v-list-item-title>-->
                <!--                  </v-list-item-content>-->
                <!--                </v-list-item>-->
                <template v-if="GET_USER_INFO_DATA.groups != false">
                  <v-list-item to="/#">
                    <v-list-item-icon class="mr-2">
                      <v-icon>mdi-settings</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content align="left">
                      <v-list-item-title>Администрирование</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </template>

                <v-list-item to="/logout">
                  <v-list-item-icon class="mr-2">
                    <v-icon>mdi-logout</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content align="left">
                    <v-list-item-title>Выход</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-list>
          </v-card>
        </template>
      </v-menu>
    </v-app-bar>
    <!--    END Navbar-->

    <!--    Sidebar-->
    <v-navigation-drawer
      v-model="drawer"
      :clipped="$vuetify.breakpoint.lgAndUp"
      app
    >
      <v-list dense>
        <template>
          <v-list-item
            v-for="item in linksMenu"
            :key="item.title"
            link
            :to="item.url"
            :exact="item.exact"
          >
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content align="left">
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </template>

        <v-divider></v-divider>

        <template v-if="GET_USER_INFO_DATA.groups != false">
          <v-subheader>Доступ для группы</v-subheader>

          <div v-for="(group, i) in GET_USER_INFO_DATA.groups" :key="i">
            <template v-if="group.name === 'Редактор Ипотека'">
              <template v-for="item in itemsMortgage">
                <v-row v-if="item.heading" :key="item.heading">
                  <v-col cols="6">
                    <v-subheader v-if="item.heading">
                      {{ item.heading }}
                    </v-subheader>
                  </v-col>
                  <v-col cols="6">
                    <a href="#!" class="body-2 black--text">EDIT</a>
                  </v-col>
                </v-row>

                <v-list-group
                  v-else-if="item.children"
                  :key="item.text"
                  v-model="item.model"
                  :prepend-icon="item.model ? item.icon : item['icon-alt']"
                  append-icon=""
                >
                  <template v-slot:activator>
                    <v-list-item-content>
                      <v-list-item-title>
                        {{ item.text }}
                      </v-list-item-title>
                    </v-list-item-content>
                  </template>
                  <v-list-item
                    v-for="(child, i) in item.children"
                    :key="i"
                    link
                    :to="child.url"
                    :exact="child.exact"
                  >
                    <v-list-item-action v-if="child.icon">
                      <v-icon>{{ child.icon }}</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title>
                        {{ child.text }}
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-group>

                <v-list-item v-else :key="item.text" link>
                  <v-list-item-action>
                    <v-icon>{{ item.icon }}</v-icon>
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title>
                      {{ item.text }}
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </template>
            </template>
          </div>

          <v-divider></v-divider>
        </template>
      </v-list>
    </v-navigation-drawer>
    <!--    END Sidebar-->

    <v-content>
      <v-container v-bind:fluid="drawer">
        <!--        class="fill-height" -->
        <!--        <v-row align="center" justify="center">-->
        <router-view />
        <!--        </v-row>-->
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { mapState, mapGetters, mapActions } from "vuex";

export default {
  name: "main-layout",
  data: () => ({
    right: null,
    drawer: null,
    linksMenu: [
      { title: "Главная", url: "/", exact: true, icon: "mdi-view-dashboard" },
      // { title: "Login", url: "/login", icon: "mdi-account" },
      // { title: "Registration", url: "/registr", icon: "mdi-account-plus" },
      { title: "Ипотека", url: "/mortgage-search", icon: "mdi-view-list" },
      { title: "Контакты", url: "/contacts", icon: "mdi-contacts" },
      { title: "About", url: "/about", icon: "mdi-vector-polyline-minus" },
      { title: "Помощь", url: "/help", icon: "mdi-help-circle" },
      { title: "Cars", url: "/cars", icon: "mdi-car-multiple" },
      { title: "Mods", url: "/mods", icon: "mdi-history" }
      // { title: "Logout", url: "/logout", icon: "mdi-account" }
    ],
    itemsUserIcon: [
      { title: "Администрирование", url: "", icon: "mdi-settings" },
      // { title: "Click Me 2" },
      // { title: "Click Me 3" },
      // { title: "Click Me 4" },
      { title: "Выход", url: "/logout", icon: "mdi-logout" }
    ],
    itemsMortgage: [
      {
        icon: "mdi-chevron-up",
        "icon-alt": "mdi-chevron-down",
        text: 'Редактирование "Ипотека"',
        model: false,
        children: [
          { icon: "mdi-plus", url: "/mortgage-editbank", text: "Банки" },
          { icon: "mdi-plus", url: "/mortgage-edittargetcredits", text: "Цель ипотеки" },
          { icon: "mdi-plus", text: "Программы" }
        ]
      }
    ]
  }),
  computed: {
    ...mapState("user_info", ["USER_INFO_DATA"]),
    ...mapGetters("user_info", ["GET_USER_INFO_DATA"])
  },
  methods: {
    ...mapActions("user_info", ["FETCH_USER_INFO"]),
    get_user_info() {
      const refresh_token = localStorage.getItem("refresh_token");
      this.FETCH_USER_INFO(refresh_token);
    }
  },
  created() {
    this.get_user_info();
  }
};
</script>
