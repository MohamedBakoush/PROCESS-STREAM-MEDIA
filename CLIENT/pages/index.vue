<script setup lang="ts"> 
interface InfoData {
    info_id: string;
    supabase_user_id: string;
    public: boolean;
    video_name?: string;
    video_description?: string; 
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
        const response = await fetch(`/api/info?supabase_user_id=${userId}`);
        if (!response.ok) throw new Error('Failed to fetch data');
        infoData.value = await response.json();
    } catch (err) {
        console.error('Fetch error:', err); 
    } finally {
        loading.value = false;
    } 
};

const selectVideo = (videoId: string) => {
    router.push({ path: '/watch', query: { v: videoId } });
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
    <div>
        <button @click="signOut">SIGN OUT</button>

        <button @click="router.push({ path: '/upload' })">Upload Videos</button>
        <div v-for="info in infoData" :key="info.info_id">
            <p style="cursor: pointer;" @click="selectVideo(info.info_id)">{{ info.video_name }}</p>
        </div> 
    </div>
</template>