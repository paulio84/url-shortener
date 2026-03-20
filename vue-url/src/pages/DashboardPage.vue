<template>
    <div class="min-h-screen bg-gray-50">
        <NavBar />
        <main class="max-w-4xl mx-auto px-4 sm:px-6 py-8 space-y-6">
            <ShortenForm @shortened="handleShortened" />
            <URLTable :urls="urls" :loading="loading" />
        </main>
    </div>
</template>
    
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue"
import type { ShortURL } from "@/api/types"
import NavBar from '@/components/NavBar/NavBar.vue';
import ShortenForm from '@/components/ShortenForm/ShortenForm.vue';
import URLTable from '@/components/URLTable/URLTable.vue';
import { fetchURLs } from "@/api/urls";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore()

const urls = ref<ShortURL[]>([])
const loading = ref(false)

async function loadURLs() {
    if (!auth.accessToken) return

    loading.value = true
    try {
        const response = await fetchURLs(auth.accessToken)
        if (!response.ok) return
        urls.value = await response.json()
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    loadURLs()
    window.addEventListener("focus", loadURLs)
})

onUnmounted(() => {
    window.removeEventListener("focus", loadURLs)
})

function handleShortened(newUrl: ShortURL) {
    urls.value = [newUrl, ...urls.value]
}

</script>