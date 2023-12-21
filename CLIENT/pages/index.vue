<script setup lang="ts"> 
    interface InfoData {
        info_id: number;
        video_id: string;
        video_title: string;
        video_description: string;
    }

    const infoData = ref<InfoData[]>([]);
    const loading = ref(true);

    onMounted(async () => {
        try {
            const response = await fetch('/api/info');
            if (!response.ok) throw new Error('Failed to fetch');
            infoData.value = await response.json();
        } catch (err) {
            console.log(err);
        } finally {
            loading.value = false;
        }
    });
    
    const selectVideo = (videoId: String) => {
        useRouter().push({ path: '/watch', query: { v: String(videoId) } });
    };
</script>

<template>
    <div> 
        <div v-for="info in infoData" :key="info.info_id"> 
            <p style="cursor: pointer;" @click="selectVideo(info.video_id)">{{ info.video_id }}</p>
        </div> 
    </div>
</template>