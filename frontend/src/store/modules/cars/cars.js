const carsModule = {
  namespaced: true,
  state: {
    CARS_DATA: null
  },
  getters: {},
  mutations: {
    SET_UPDATE_CARS_DATA(state, data) {
      state.CARS_DATA = data;
    },
    destroy_CARS_DATA(state) {
      state.CARS_DATA = null;
    }
  },
  actions: {}
};

export default carsModule;
