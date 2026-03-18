<template>
    <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-semibold text-gray-900">Your URLs</h2>
        </div>

        <div v-if="loading" class="px-6 py-8 flex justify-center text-sm text-gray-500">
            <img :src="loadingSpinner" alt="Loading..." class="w-14 h-auto">
        </div>

        <div v-else-if="urls.length === 0" class="px-6 py-8 text-center text-sm text-gray-500">
            No URLs yet. Shorten one above!
        </div>
        
        <table v-else class="w-full text-sm">
            <thead class="bg-gray-50 border-b border-gray-200">
                <tr>
                    <th class="px-6 py-3 text-left font-medium text-gray-500">Original URL</th>
                    <th class="px-6 py-3 text-left font-medium text-gray-500">Short URL</th>
                    <th class="px-6 py-3 text-left font-medium text-gray-500">Clicks</th>
                    <th class="px-6 py-3 text-left font-medium text-gray-500">Created</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
                <tr v-for="url in urls" :key="url.id" class="hover:bg-gray-100">
                    <td :title="url.original_url" class="px-6 py-4 max-w-xs truncate text-gray-900">
                        {{ url.original_url }}
                    </td>
                    <td class="px-6 py-4">
                        <a 
                            :href="fullShortUrl(url.short_url)"
                            target="_blank"
                            rel="noopener noreferrer"
                            class="text-blue-600 hover:underline"
                        >
                            {{ url.short_url }}
                        </a>
                    </td>
                    <td class="px-6 py-4 text-gray-600">{{ url.clicks }}</td>
                    <td class="px-6 py-4 text-gray-600">{{ formatDate(url.created_at) }}</td>
                </tr>
            </tbody>
        </table>

    </div>
</template>

<script setup lang="ts">
import loadingSpinner from "@/assets/loading_spinner.svg"
import type { ShortURL } from "@/api/types"
import { fullShortUrl } from "@/api/urls";

defineProps<{
    urls: ShortURL[]
    loading: boolean
}>()

function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString("en-GB", {
        day: "numeric",
        month: "short",
        year: "numeric",
    })
}
</script>