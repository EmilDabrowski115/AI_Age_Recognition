// Authentication service
class AuthService {
  constructor() {
    this.isAuthenticated = false
    this.user = null
  }

  // Login method (placeholder)
  async login(credentials) {
    try {
      console.log('Logging in with:', credentials)
      
      // Placeholder authentication
      this.isAuthenticated = true
      this.user = {
        id: Math.random().toString(36).substr(2, 9),
        email: credentials.email,
        name: credentials.name
      }
      
      return {
        success: true,
        user: this.user
      }
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  

  // Logout method
  logout() {
    this.isAuthenticated = false
    this.user = null
  }

  // Check if user is authenticated
  isLoggedIn() {
    return this.isAuthenticated
  }

  // Get current user
  getCurrentUser() {
    return this.user
  }
}

export default new AuthService()
