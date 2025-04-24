import "./assets/main.css";

import "swiper/css";
import "/public/css/custom.css";
import "/public/css/dark.css";
import "/public/css/plugins.css";
import "/public/css/style.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(router);

app.mount("#app");
