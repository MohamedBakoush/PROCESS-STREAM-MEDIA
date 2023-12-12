<script setup lang="ts">
    import Page404 from '@/components/error/404.vue';
    import "@/index.css"; 

    useHead({
        title: 'Error - 404 Not Found',
        meta: [
            { name: 'description', content: "Page Not Found" },
            { name: 'viewport', content: 'width=device-width, initial-scale=1' }
        ],
    });
</script> 

<template>
    <NuxtLayout name="404">   
        <Page404/>
    </NuxtLayout>
</template>