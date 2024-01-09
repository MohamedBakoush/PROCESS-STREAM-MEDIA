<script setup lang="ts">
    import videoPlayer from '@/components/video/player.vue';
</script>

<template>
    <videoPlayer :src="'http://localhost:1935/watch?user=' + useRoute().query.user + '&v=' + useRoute().query.v" />
</template>