<template>
  <i class="gg-volume"></i>
</template>

<style scoped>
.gg-volume {
    box-sizing: border-box;
    position: relative;
    display: block;
    transform: scale(var(--ggs,1));
    width: 8px;
    height: 8px;
    border: 2px solid;
    border-right: 0;
    -webkit-perspective: 12px;
    perspective: 12px;
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px
}
.gg-volume::after,
.gg-volume::before {
    content: "";
    display: block;
    box-sizing: border-box;
    position: absolute
}
.gg-volume::before {
    left: 2px;
    transform: rotateY(-90deg);
    width: 10px;
    height: 10px;
    border: 2px solid;
    border-left: 0;
    top: -3px
}
</style>
