<template>
    <nav ref="navRef" class="relative bg-white border-b border-gray-200 px-6 py-4">
        <div class="max-w-4xl mx-auto flex items-center justify-between">
            <RouterLink to="/" class="text-lg font-bold text-gray-900">UrlMe</RouterLink>

            <!-- Desktop nav -->
            <div class="hidden sm:flex items-center gap-4">
                <span class="text-sm text-gray-600">{{ auth.user?.email }}</span>
                <button
                    @click="handleLogout"
                    class="text-sm text-red-600 hover:text-red-800 font-medium hover:cursor-pointer"
                >
                    Sign out
                </button>
            </div>

            <!-- Mobile burger menu -->
            <button
                type="button"
                class="sm:hidden hover:cursor-pointer text-gray-600 hover:text-gray-900"
                @click.stop="toggleMenuOpen"
            >
                <Bars3Icon v-if="!menuOpen" class="w-6 h-6" />
                <XMarkIcon v-else class="w-6 h-6" />
            </button>
        </div>

        <!-- Mobile menu-->
        <div 
            v-if="menuOpen"
            class="sm:hidden absolute top-full right-0 w-full bg-white shadow-lg border-t border-gray-200 py-2 z-50"
        >
            <p class="px-4 py-2 text-sm text-gray-600 border-b border-gray-100">
                {{ auth.user?.email }}
            </p>
            <button 
                @click="handleLogout"
                class="px-4 py-2 text-sm text-red-600 hover:bg-gray-50 hover:text-red-800 font-medium hover:cursor-pointer"
            >
                Sign out
            </button>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import { Bars3Icon, XMarkIcon } from "@heroicons/vue/24/outline"

const router = useRouter()
const auth = useAuthStore()
const menuOpen = ref(false)
const navRef = ref<HTMLElement | null>(null)

function handleClickOutside(event: MouseEvent) {
    if (navRef.value && !navRef.value.contains(event.target as Node)) {
        menuOpen.value = false
    }
}

function handleLogout() {
    menuOpen.value = false
    auth.logout()
    router.push("/login")
}

function toggleMenuOpen() {
    menuOpen.value = !menuOpen.value
}

onMounted(() => {
    document.addEventListener("click", handleClickOutside)
})

onUnmounted(() => {
    document.removeEventListener("click", handleClickOutside)
})
</script>
