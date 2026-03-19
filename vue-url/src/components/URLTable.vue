<template>
    <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-semibold text-gray-900">Your URLs</h2>
        </div>

        <div v-if="loading" class="px-6 py-8 flex justify-center text-sm text-gray-500">
            <img :src="loadingSpinner" alt="Loading..." class="w-14 h-auto">
        </div>

        <div v-else-if="noURLs" class="px-6 py-8 text-center text-sm text-gray-500">
            No URLs yet. Shorten one above!
        </div>
        
        <template v-else>
            <!-- Mobile view -->
            <ul class="divide-y divide-gray-200 sm:hidden">
                <li 
                    v-for="url in urls"
                    :key="url.id"
                    class="px-4 py-3"
                >
                    <button
                        type="button"
                        class="w-full flex items-center justify-between hover:cursor-pointer"
                        @click="toggleExpanded(url.id)"
                    >
                        <a
                            target="_blank"
                            rel="noreferrer noopener"
                            :href="fullShortUrl(url.short_url)"
                            class="text-blue-600 hover:underline text-sm font-medium"
                            @click.stop
                        >
                            {{ url.short_url }}
                        </a>
                        <ChevronDownIcon
                            class="w-4 h-4 text-gray-400 transition-transform duration-200"
                            :class="{ 'rotate-180': expandedIds.includes(url.id) }"
                        />
                    </button>
                    <div
                        v-if="expandedIds.includes(url.id)"
                        class="mt-2 space-y-1 text-sm text-gray-600"
                    >
                        <p 
                            :title="url.original_url"
                            class="truncate text-gray-900"
                        >
                            {{ url.original_url }}
                        </p>
                        <p>Clicks: {{ url.clicks }}</p>
                        <p>Created: {{ formatDate(url.created_at) }}</p>
                    </div>
                </li>
            </ul>

            <!-- Tablet/Desktop view -->
            <table class="hidden sm:table w-full text-sm">
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
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue"
import { ChevronDownIcon } from "@heroicons/vue/24/outline"
import loadingSpinner from "@/assets/loading_spinner.svg"
import type { ShortURL } from "@/api/types"
import { fullShortUrl } from "@/api/urls";

const props = defineProps<{
    urls: ShortURL[]
    loading: boolean
}>()

const noURLs = computed(() => props.urls.length === 0)

const expandedIds = ref<number[]>([])

function toggleExpanded(id: number) {
    const index = expandedIds.value.indexOf(id)
    if (index === -1) {
        expandedIds.value.push(id)
    } else {
        expandedIds.value.splice(index, id)
    }
}

function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString("en-GB", {
        day: "numeric",
        month: "short",
        year: "numeric",
    })
}
</script>