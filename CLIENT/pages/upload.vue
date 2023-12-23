<template>
    <div>
        <input type="file" @change="handleFileChange" multiple />
        <button @click="uploadFile">Upload</button>
    </div>
</template>
  
<script setup> 
    const selectedFiles = ref(null);
    const supabaseUser = useSupabaseUser();

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
