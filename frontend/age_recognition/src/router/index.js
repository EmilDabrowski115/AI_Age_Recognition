import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import LoginPage from "@/views/LoginPage.vue";
import AgeVerifyPage from "@/views/AgeVerifyPage.vue";

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingPage
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage
  },
    {
        path: '/login',
        name: 'Login',
        component: LoginPage
    },
    {
        path: '/ageVerify',
        name: 'AgeVerify',
        component: AgeVerifyPage
    }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
