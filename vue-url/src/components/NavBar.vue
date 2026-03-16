<template>
    <nav class="bg-white border-b border-gray-200 px-6 py-4">
        <div class="max-w-4xl mx-auto flex items-center justify-between">
            <span class="text-lg font-bold text-gray-900">UrlMe</span>
            <div class="flex items-center gap-4">
                <span class="text-sm text-gray-600">{{ auth.user?.email }}</span>
                <button
                    @click="handleLogout"
                    class="text-sm text-red-600 hover:text-red-800 font-medium hover:cursor-pointer"
                >
                    Sign out
                </button>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const auth = useAuthStore()

function handleLogout() {
    auth.logout()
    router.push("/login")
}
</script>
