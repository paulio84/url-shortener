import { describe, it, expect } from "vitest"
import { mount } from "@vue/test-utils"
import FormField from "@/components/FormField.vue"

describe("FormField", () => {
  it("renders the label", () => {
    const wrapper = mount(FormField, {
      props: {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "you@example.com",
        modelValue: "",
      },
    })
    expect(wrapper.text()).toContain("Email")
  })

  it("renders the input with correct type", () => {
    const wrapper = mount(FormField, {
      props: {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "you@example.com",
        modelValue: "",
      },
    })
    const input = wrapper.find("input")
    expect(input.attributes("type")).toBe("email")
  })

  it("does not show toggle button for non-password fields", () => {
    const wrapper = mount(FormField, {
      props: {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "you@example.com",
        modelValue: "",
      },
    })
    expect(wrapper.find("button").exists()).toBe(false)
  })

  it("shows toggle button for password fields", () => {
    const wrapper = mount(FormField, {
      props: {
        id: "password",
        label: "Password",
        type: "password",
        placeholder: "",
        modelValue: "",
      },
    })
    expect(wrapper.find("button").exists()).toBe(true)
  })

  it("toggles password visibility when button is clicked", async () => {
    const wrapper = mount(FormField, {
      props: {
        id: "password",
        label: "Password",
        type: "password",
        placeholder: "",
        modelValue: "",
      },
    })
    const input = wrapper.find("input")
    const button = wrapper.find("button")

    expect(input.attributes("type")).toBe("password")
    await button.trigger("click")
    expect(input.attributes("type")).toBe("text")
    await button.trigger("click")
    expect(input.attributes("type")).toBe("password")
  })

  it("emits update:modelValue when input changes", async () => {
    const wrapper = mount(FormField, {
      props: {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "",
        modelValue: "",
      },
    })
    const input = wrapper.find("input")
    await input.setValue("test@example.com")
    expect(wrapper.emitted("update:modelValue")?.[0]).toEqual(["test@example.com"])
  })
})