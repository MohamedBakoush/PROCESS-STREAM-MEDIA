<template>
  <i class="gg-media-play"></i>
</template>

<style scoped>
.gg-media-play {
  box-sizing: border-box;
  position: relative;
  display: block;
  width: 22px;
  height: 22px;
}
.gg-media-play::before {
  content: "";
  display: block;
  box-sizing: border-box;
  position: absolute;
  width: 0;
  height: 10px;
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid;
  top: 6px;
  left: 9px;
}
</style>
