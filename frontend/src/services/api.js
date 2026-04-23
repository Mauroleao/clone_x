import axios from 'axios';

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/';

const api = axios.create({
    baseURL: apiUrl,
    timeout: 60000 // Aumentado para 60s devido ao tempo de cold start (spin up) do Render
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401 && error.config?.headers?.Authorization) {
            if (!error.config?.url?.includes('login') && !error.config?.url?.includes('register')) {
                console.log('Token invalido ou expirado, limpando...');
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('username');
            }
        }
        return Promise.reject(error);
    }
);

export default api;
