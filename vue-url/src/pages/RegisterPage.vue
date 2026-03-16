<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50">
        <div class="w-full max-w-md bg-white rounded-lg shadow p-8">
            <h1 class="text-2xl font-bold text-gray-900 mb-6">
                Create an account
            </h1>

            <form @submit.prevent="handleSubmit" class="space-y-4">
                
                <div>
                    <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
                        Email
                    </label>
                    <input 
                        id="email" 
                        type="email" 
                        v-model="email"
                        required
                        placeholder="you@example.com"
                        class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
                        Password
                    </label>
                    <input 
                        id="password"
                        type="password"
                        v-model="password"
                        required
                        class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <p v-if="error" class="text-sm text-red-600">
                    {{ error }}
                </p>

                <button 
                    type="submit"
                    :disabled="loading"
                    class="w-full bg-blue-600 text-white rounded-md px-4 py-2 text-sm font-medium hobver:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {{ loading ? "Creating account...": "Create account" }}
                </button>

            </form>

            <p class="mt-4 text-sm text-gray-600">
                Already have an account?
                <RouterLink to="/login" class="text-blue-600 hover:underline">
                    Sign in
                </RouterLink>
            </p>

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import type { AuthResponse, APIError } from "@/types/api"

const router = useRouter()
const auth = useAuthStore()

const email = ref("")
const password = ref("")
const error = ref<string | null>(null)
const loading = ref(false)

async function handleSubmit() {
    error.value = null
    loading.value = true

    try {
        const registerResponse = await fetch("/api/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: email.value,
                password: password.value,
            }),
        })

        if (!registerResponse.ok) {
            const data: APIError = await registerResponse.json()
            error.value = data.error.message
            return
        }

        const loginResponse = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: email.value,
                password: password.value,
            }),
        })

        if (!loginResponse.ok) {
            const data: APIError = await loginResponse.json()
            error.value = data.error.message
            return
        }

        const data: AuthResponse = await loginResponse.json()
        auth.login(data.access_token, data.refresh_token, data.user)
        router.push("/dashboard")

    } finally {
        loading.value = false
    }
}
</script>