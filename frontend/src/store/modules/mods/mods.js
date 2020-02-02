const modsModule = {
  namespaced: true,
  state: {
    APIData: "" // received data from the backend API is stored here.
  },
  mutations: {

    SET_UPDATE_APIData(state, data) {
      state.APIData = data;
    },
    destroyAPIData(state) {
      state.APIData = null;
    }
  }
};

export default modsModule;
