<template>
  <div class="register-page">
    <div class="register-container">
      <h1>Age Verification</h1>

      <!-- Age verification form -->
      <form @submit.prevent="handleVerifyAge" class="register-form" v-if="!ageVerified">
        <div class="form-group">
          <label for="image">Upload your photo</label>
          <input
              id="image"
              type="file"
              accept="image/*"
              @change="handleFileChange"
              required
              class="form-input"
          />
        </div>

        <!-- Photo preview -->
        <div v-if="preview" class="preview-box">
          <img :src="preview" alt="Preview" class="preview-img" />
        </div>

        <button
            type="submit"
            class="submit-button"
            :disabled="isVerifying || !file"
        >
          <span v-if="!isVerifying">Verify Age</span>
          <span v-else>Verifying...</span>
        </button>
      </form>

      <!-- After age verified -->
      <div v-if="ageVerified">
        <p>Your verified age: {{ userAge }}</p>
        <p v-if="isOldEnough" style="color: lightgreen;">
          You are old enough to register.
        </p>
        <p v-else style="color: tomato;">
          You are not old enough to register.
        </p>

        <!-- Registration form only if old enough -->
        <div v-if="isOldEnough">
          <h1>Create Account</h1>
          <form @submit.prevent="handleRegister" class="register-form">
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

            <button type="submit" class="submit-button" :disabled="isRegistering">
              <span v-if="!isRegistering">Register</span>
              <span v-else>Registering...</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import userService from '../services/userService.js'

const router = useRouter()

const file = ref(null)
const preview = ref(null)

const isVerifying = ref(false)
const isRegistering = ref(false)

const ageVerified = ref(false)
const userAge = ref(null)
const isOldEnough = ref(false)

const formData = reactive({
  username: '',
  password: ''
})

const handleFileChange = (event) => {
  const selected = event.target.files[0]
  file.value = selected
  if (selected) {
    preview.value = URL.createObjectURL(selected)
  }
}

const handleVerifyAge = async () => {
  if (!file.value) return

  isVerifying.value = true
  const formDataForAge = new FormData()
  formDataForAge.append('image', file.value)

  try {
    // const response = await userService.ageVerify(formDataForAge)
    // userAge.value = response.age
    ageVerified.value = true
    isOldEnough.value = userAge.value >= 18 // minimum age limit
  } catch (err) {
    ageVerified.value = true
    console.error('Verification failed:', err)
    alert('Age verification failed. Please try again.')
  } finally {
    isVerifying.value = false
    ageVerified.value = true
  }
}

const handleRegister = async () => {
  isRegistering.value = true
  try {
    await userService.register({
      username: formData.username,
      password: formData.password
    })
    router.push('/')
  } catch (err) {
    console.error('Registration failed:', err)
    alert('Registration failed. Please try again.')
  } finally {
    isRegistering.value = false
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
  background: rgba(255, 255, 255, 0.08);
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
  background: #fff;
}

.preview-box {
  width: 200px;
  height: 200px;
  margin: 1rem auto;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #00ffff;
  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
