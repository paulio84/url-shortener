<template>
    <AuthCard title="Create an account">
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
                class="w-full bg-blue-600 text-white rounded-md px-4 py-2 text-sm font-medium hover:bg-blue-700 hover:cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
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

    </AuthCard>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import type { APIError, AuthResponse } from "@/api/types"
import AuthCard from "@/components/AuthCard/AuthCard.vue"
import FormField from "@/components/FormField/FormField.vue"
import { loginUser, registerUser } from "@/api/auth"

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
        const registerResponse = await registerUser(email.value, password.value)

        if (!registerResponse.ok) {
            const data: APIError = await registerResponse.json()
            error.value = data.error.message
            return
        }

        const loginResponse = await loginUser(email.value, password.value)

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