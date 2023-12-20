<template>
    <div>
        <input type="file" @change="handleFileChange" multiple />
        <button @click="uploadFile">Upload</button>
    </div>
</template>
  
<script setup> 
    const selectedFiles = ref(null)

    function handleFileChange(event) {
        selectedFiles.value = Array.from(event.target.files);
    }

    async function uploadFile() {
        if (selectedFiles.value.length === 0) return;

        for (const file of selectedFiles.value) {
            const formData = new FormData();
            formData.append('file', file);

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
