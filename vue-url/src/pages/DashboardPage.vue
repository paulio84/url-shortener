<template>
    <div class="min-h-screen bg-gray-50">
        <NavBar />
        <main class="max-w-4xl mx-auto px-6 py-8 space-y-6">
            <ShortenForm @shortened="handleShortened" />
            <URLTable :urls="urls" :loading="loading" />
        </main>
    </div>
</template>
    
<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useAuthStore } from "@/stores/auth"
import type { ShortURL } from "@/types/api"
import NavBar from '@/components/NavBar.vue';
import ShortenForm from '@/components/ShortenForm.vue';
import URLTable from '@/components/URLTable.vue';

const auth = useAuthStore()

const urls = ref<ShortURL[]>([])
const loading = ref(false)

onMounted(async () => {
    loading.value = true
    try {
        const response = await fetch("/api/urls", {
            headers: { Authorization: `Bearer ${auth.accessToken}` },
        })
        if (!response.ok) return
        urls.value = await response.json()
    } finally {
        loading.value = false
    }
})

function handleShortened(newUrl: ShortURL) {
    urls.value = [newUrl, ...urls.value]
}

</script>