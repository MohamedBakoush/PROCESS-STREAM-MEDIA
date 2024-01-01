<script setup> 
    const selectedFiles = ref(null);
    const supabaseUser = useSupabaseUser();

    const emit = defineEmits(['close']);
    const closeOverlay = () => {
        emit('close');
    };

    function handleFileChange(event) {
        selectedFiles.value = Array.from(event.target.files);
    }

    async function uploadFile() {
        if (selectedFiles.value.length === 0) return;

        const supabaseUserId = supabaseUser.value?.id; // Get the Supabase user ID
        if (!supabaseUserId) {
            console.error('User ID not available');
            return;
        }

        for (const file of selectedFiles.value) {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('supabase_user_id', supabaseUserId); // Append user ID to formData

            try {
                await $fetch('http://localhost:1945/upload', {
                    method: 'POST',
                    body: formData,
                });
                alert('Upload successful');
            } catch (error) {
                console.error('Upload failed', error);
                alert('Upload failed');
            }
        } 
    }
</script>

<template>
    <div class="fixed inset-0 bg-gray-600 bg-opacity-75 flex justify-center items-center">
        <div class="bg-white p-4 rounded-lg shadow-lg">
            <input type="file" @change="handleFileChange" multiple />
            <button @click="uploadFile" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Upload
            </button>
            <button @click="closeOverlay" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded ml-2">
                Close
            </button>
        </div>
    </div>
</template>