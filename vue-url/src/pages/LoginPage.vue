<template>
    <AuthCard title="Sign in to UrlMe">
        <form @submit.prevent="handleSubmit" class="space-y-4">
            
            <FormField
                id="email"
                v-model="email"
                label="Email"
                type="email"
                placeholder="you@example.com"
            />

            <FormField
                id="password"
                v-model="password"
                label="Password"
                type="password"
                placeholder=""
            />

            <p v-if="error" class="text-sm text-red-600">
                {{ error }}
            </p>

            <button 
                type="submit"
                :disabled="loading"
                class="w-full bg-blue-600 text-white rounded-md px-4 py-2 text-sm font-medium hover:bg-clue-700 hover:cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {{ loading ? "Signing in...": "Sign in" }}
            </button>

        </form>

        <p class="mt-4 text-sm text-gray-600">
            Don't have an account?
            <RouterLink to="/register" class="text-blue-600 hover:underline">
                Register
            </RouterLink>
        </p>
    </AuthCard>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import type { AuthResponse, APIError } from "@/types/api"
import AuthCard from "@/components/AuthCard.vue"
import FormField from "@/components/FormField.vue"

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
        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: email.value, 
                password: password.value,
            }),
        })

        if (!response.ok) {
            const data: APIError = await response.json()
            error.value = data.error.message
            return
        }

        const data: AuthResponse = await response.json()
        auth.login(data.access_token, data.refresh_token, data.user)
        router.push("/dashboard")
    } finally {
        loading.value = false
    }
}
</script>