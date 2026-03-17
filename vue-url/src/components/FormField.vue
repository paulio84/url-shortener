<template>
    <div>
        <label :for="id" class="block text-sm font-medium text-gray-700 mb-1">
            {{ label }}
        </label>
        <div class="relative">
            <input 
                :id="id" 
                :type="inputType" 
                :placeholder="placeholder"
                :value="modelValue"
                required
                class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 pr-10"
                @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
            />
            <button
                v-if="type === 'password'"
                type="button"
                @click="toggleVisibility"
                class="absolute inset-y-0 right-0 px-3 flex items-center text-gray-500 hover:cursor-pointer hover:text-gray-700"
            >
                <EyeSlashIcon v-if="passwordVisible" class="w-4 h-4" />
                <EyeIcon v-else class="w-4 h-4" />
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { EyeIcon, EyeSlashIcon } from "@heroicons/vue/24/outline";
import { ref, computed } from "vue"

const props = defineProps<{
    id: string
    label: string
    type: string
    placeholder: string
    modelValue: string
}>()

defineEmits<{
    "update:modelValue": [value: string]
}>()

const passwordVisible = ref(false)

const inputType = computed(() => {
    if (props.type === "password") {
        return passwordVisible.value ? "text" : "password"
    }
    return props.type
})

function toggleVisibility() {
    passwordVisible.value = !passwordVisible.value
}
</script>