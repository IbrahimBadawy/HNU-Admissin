<template>
  <PreLoader />
  <router-view />
  <Cursor />
</template>

<script>
import Cursor from "./components/layout/Cursor.vue";
import PreLoader from "./components/layout/PreLoader.vue";
import { dataImage, portfolioHover, scroll_, stickyNav } from "./utilits";

import WOW from "wow.js";

export default {
  name: "App",
  data() {
    return { dark: false };
  },
  mounted() {
    window.addEventListener("scroll", stickyNav);
    window.addEventListener("scroll", scroll_);
    setTimeout(() => {
      dataImage();
      portfolioHover();
      new WOW().init();
    }, 100);
  },
  components: { PreLoader, Cursor },
};
</script>
