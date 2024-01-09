<script setup lang="ts"> 

import Upload from '@/components/video/upload.vue';
let isUploadOverlayVisible = ref(false);
const toggleUploadOverlay = () => {
    isUploadOverlayVisible.value = !isUploadOverlayVisible.value;
};

interface InfoData {
    video_id: string;
    video_title: string;
    video_description: boolean; 
    auto_generated_thumbnail_num: number;
}

const infoData = ref<InfoData[]>([]);
const loading = ref(false);
const router = useRouter();

const supabaseClient = useSupabaseClient();
const supabaseUser = useSupabaseUser();

watch(supabaseUser, (newUser) => {
    if (newUser && !infoData.value.length) {
        fetchInfoData();
    } else {
        infoData.value = []; // Clear data on sign out
    }
});

const fetchInfoData = async () => {
    loading.value = true;
    try {
        const userId = supabaseUser.value.id;
        const response = await fetch(`/api/availableVideos?supabase_user_id=${userId}`);
        if (!response.ok) throw new Error('Failed to fetch data');
        infoData.value = await response.json();
    } catch (err) {
        console.error('Fetch error:', err); 
    } finally {
        loading.value = false;
    } 
};

const selectVideo = (videoId: string) => {
    router.push({ path: '/watch', query: { user: supabaseUser.value.id, v: videoId } });
};

const getThumbnail = (videoId: string, thumbNum: number) => {
    return `http://localhost:1935/watch?user=${supabaseUser.value.id}&v=${videoId}&t=${thumbNum}`;
};

const signOut = async () => {
    await supabaseClient.auth.signOut();
    infoData.value = []; // Clear user data on sign out
    router.push({ path: '/login' });
};

onMounted(() => {
    if (!supabaseUser.value) {
        router.push({ path: '/login' });
    } else {
        fetchInfoData();
    }
});
</script>

<template>
    <div class="max-h-screen overflow-auto">
        <button @click="signOut" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            SIGN OUT
        </button>

        <button @click="toggleUploadOverlay" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded ml-2">
            Upload Videos
        </button>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mt-4">
            <div class="rounded overflow-hidden shadow-lg" style="cursor: pointer;" v-for="info in infoData" :key="info.video_id"  @click="selectVideo(info.video_id)">
                <img :src="getThumbnail(info.video_id, 0)" alt="video thumbnail" class="w-full h-48 object-cover">
                <div class="px-6 py-4">
                    <p class="font-bold text-xl mb-2">
                        {{ info.video_title }}
                    </p>
                </div>
            </div>
        </div>

        <Upload v-if="isUploadOverlayVisible" @close="toggleUploadOverlay" />
    </div>
</template>