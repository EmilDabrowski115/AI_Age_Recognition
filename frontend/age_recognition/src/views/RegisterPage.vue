<template>
  <div class="register-page">
    <div class="register-container">
      <h1>Age Verification</h1>
      <form @submit.prevent="handleAgeVerify" class="register-form" v-if="!ageVerified">
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
          <button type="button" @click="openCamera" class="camera-button">Open Camera</button>
        </div>

        <div v-if="isCameraOpen" class="camera-modal">
          <video ref="video" autoplay class="camera-video"></video>
          <button @click="captureImage" class="capture-button">Capture</button>
        </div>

        <div v-if="preview" class="preview-box">
          <img :src="preview" alt="Preview" class="preview-img" />
        </div>

        <button type="submit" class="submit-button" :disabled="!file || isSubmitting">
          <span v-if="!isSubmitting">Verify Age</span>
          <span v-else>Verifying...</span>
        </button>
      </form>

      <div v-if="ageVerified">
        <p>Your age is: {{ userAge }}</p>
        <p v-if="isOldEnough" style="color:lightgreen;">You are old enough to register.</p>
        <p v-else style="color:tomato;">You are not old enough to register.</p>

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
      <button @click="goBack" class="back-button">Back to Home</button>
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

const isSubmitting = ref(false)
const isRegistering = ref(false)

const ageVerified = ref(false)
const userAge = ref(null)
const isOldEnough = ref(false)

const formData = reactive({
  username: '',
  password: ''
})

const isCameraOpen = ref(false)
const video = ref(null)

const handleFileChange = (event) => {
  const selected = event.target.files[0]
  file.value = selected

  if (selected) {
    preview.value = URL.createObjectURL(selected)
  }
}

const openCamera = async () => {
  isCameraOpen.value = true
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true })
    video.value.srcObject = stream
  } catch (err) {
    console.error('Error accessing camera:', err)
    alert('Error accessing camera. Please make sure you have a camera connected and have granted permission.')
    isCameraOpen.value = false
  }
}

const captureImage = () => {
  const canvas = document.createElement('canvas')
  canvas.width = video.value.videoWidth
  canvas.height = video.value.videoHeight
  const context = canvas.getContext('2d')
  context.drawImage(video.value, 0, 0, canvas.width, canvas.height)
  preview.value = canvas.toDataURL('image/png')
  canvas.toBlob((blob) => {
    file.value = blob
  })
  isCameraOpen.value = false
  const stream = video.value.srcObject
  const tracks = stream.getTracks()
  tracks.forEach(track => track.stop())
}

const handleAgeVerify = async () => {

  if (!file.value) return

  isSubmitting.value = true

  const formDataForAge = new FormData()
  formDataForAge.append('image', file.value)

  try {
    const response = await userService.ageVerify(formDataForAge)
    userAge.value = response.data.predicted_age
    ageVerified.value = true
    isOldEnough.value = userAge.value >= 18
  } catch (err) {
    userAge.value =20
    ageVerified.value = true // poki co
    isOldEnough.value = userAge.value >= 18
    alert('Age verification failed. Please try again.')
  } finally {
    isSubmitting.value = false
  }
}

const handleRegister = async () => {
  isRegistering.value = true

  try {
    await userService.register({
      username: formData.username,
      password: formData.password
    })
    router.push('/') // redirect after registration
  } catch (err) {
    console.error('Registration failed:', err)
    alert('Registration failed. Please try again.')
  } finally {
    isRegistering.value = false
  }
}

const goBack = () => {
  router.push('/')
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

.camera-button {
  width: 100%;
  padding: 1rem;
  background: #ff00ff;
  border: none;
  border-radius: 6px;
  color: #000;
  font-weight: bold;
  cursor: pointer;
  margin-top: 1rem;
}

.camera-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.camera-video {
  width: 80%;
  max-width: 600px;
  border-radius: 12px;
}

.capture-button {
  padding: 1rem 2rem;
  background: #00ffff;
  border: none;
  border-radius: 6px;
  color: #000;
  font-weight: bold;
  cursor: pointer;
  margin-top: 1rem;
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

.back-button {
  width: 100%;
  padding: 1rem;
  background: #ff00ff;
  border: none;
  border-radius: 6px;
  color: #000;
  font-weight: bold;
  cursor: pointer;
  margin-top: 1rem;
}
</style>
