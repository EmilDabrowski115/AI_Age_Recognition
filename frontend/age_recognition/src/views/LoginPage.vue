<template>
  <div class="register-page">
    <div class="register-container">
      <h1>Login</h1>

      <form @submit.prevent="handleSubmit" class="register-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
              id="username"
              type="text"
              v-model="formData.username"
              required
              class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
              id="password"
              type="password"
              v-model="formData.password"
              required
              class="form-input"
          />
        </div>

        <button type="submit" class="submit-button" :disabled="isSubmitting">
          <span v-if="!isSubmitting">Login</span>
          <span v-else>Logging in...</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import userService from '../services/userService.js'

const router = useRouter()

const formData = reactive({
  username: '',
  password: ''
})

const isSubmitting = ref(false)

const handleSubmit = async () => {
  isSubmitting.value = true
  try {
    await userService.login({
      username: formData.username,
      password: formData.password
    })
    router.push('/') // redirect po poprawnym logowaniu
  } catch (err) {
    console.error('Login failed:', err)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #111;
  color: white;
}

.register-container {
  background: rgba(255,255,255,0.08);
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 350px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-input {
  width: 100%;
  padding: 0.8rem;
  border-radius: 6px;
  border: none;
  margin-top: 0.3rem;
}

.submit-button {
  width: 100%;
  padding: 1rem;
  background: #00ffff;
  border: none;
  border-radius: 6px;
  color: #000;
  font-weight: bold;
  cursor: pointer;
}
</style>
