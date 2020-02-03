import axios from "axios";

// const APIUrl = process.env.VUE_APP_API_ROOT;
const APIUrl = "http://127.0.0.1:8000";
// const APIUrl = "http://testserv01.tmweb.ru:8000/";

const axiosBase = axios.create({
  baseURL: APIUrl,
  headers: { contentType: "application/json" }
});

export { axiosBase, APIUrl };
