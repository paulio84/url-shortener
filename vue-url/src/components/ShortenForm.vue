<template>
    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Shorten a URL</h2>

        <form @submit.prevent="handleSubmit" class="flex flex-col sm:flex-row gap-2">
            <input 
                v-model="originalUrl"
                type="url"
                required
                placeholder="https://example.com/very/long/url"
                class="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button 
                type="submit"
                :disabled="loading"
                class="bg-blue-600 text-white rounded-md px-4 py-2 text-sm font-medium hover:cursor-pointer hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
            >
                {{ loading ? "Shortening..." : "Shorten URL" }}
            </button>
        </form>

        <p v-if="error" class="mt-2 text-sm text-red-600">{{ error }}</p>

    </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import type { ShortURL, APIError } from "@/api/types"
import { shortenURL } from "@/api/urls"
import { useAuthStore } from "@/stores/auth"

const auth = useAuthStore()

const originalUrl = ref("")
const error = ref<string | null>(null)
const loading = ref(false)

const emit = defineEmits<{
    shortened: [url: ShortURL]
}>()

async function handleSubmit() {
    if (!auth.accessToken) return

    error.value = null
    loading.value = true

    try {
        const response = await shortenURL(originalUrl.value, auth.accessToken)

        if (!response.ok) {
            const data: APIError = await response.json()
            error.value = data.error.message
            return
        }

        const data: ShortURL = await response.json()
        emit("shortened", data)
        originalUrl.value = ""

    } finally {
        loading.value = false
    }
}
</script>