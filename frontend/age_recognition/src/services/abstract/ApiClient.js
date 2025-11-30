import axios from "axios";

//idk jaki port
const API_BASE_URL = "http://localhost:8000";

class ApiClient {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: { "Content-Type": "application/json" },
    });

    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response && error.response.status === 401) {
        }

        return Promise.reject(error);
      }
    );
  }

  get(url, config = {}) {
    return this.client.get(url, config);
  }

  post(url, data, config = {}) {
    return this.client.post(url, data, config);
  }

  put(url, data, config = {}) {
    return this.client.put(url, data, config);
  }

  delete(url, config = {}) {
    return this.client.delete(url, config);
  }
}

export default new ApiClient();
