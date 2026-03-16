<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50">
        <div class="w-full max-w-md bg-white rounded-lg shadow p-8">
            <h1 class="text-2xl font-bold text-gray-900 mb-6">
                {{ title }}
            </h1>
            <slot />
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    title: string
}>()
</script>