<template>
    <i class="gg-volume">
        <i class="gg-close"></i>
    </i>
     
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



  .gg-close { 
 position: relative; 
}

.gg-close::before,
.gg-close::after {
    content: "";
    position: absolute;
    right: -22px;
    top: 0.5px;
    width: 18px;
    height: 2px;
    background-color: white;
    scale: 0.8;
}

.gg-close::before {
    transform: rotate(45deg) scale(0.7);
}

.gg-close::after {
    transform: rotate(-45deg) scale(0.7);
}
  </style>
  