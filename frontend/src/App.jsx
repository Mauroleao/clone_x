import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './pages/Login';
import Register from './pages/Register';
import Feed from './pages/Feed'; 
import Profile from './pages/Profile';
import api from './services/api';

const ProtectedRoute = ({ element, isAuthenticated }) => {
  if (isAuthenticated === null) return <div style={{ textAlign: 'center', padding: '40px' }}>Carregando...</div>;
  return isAuthenticated ? element : <Navigate to="/login" />;
};

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('access_token');
      const isAuth = !!token;
      setIsAuthenticated(isAuth);
      console.log('Auth check:', isAuth ? 'Autenticado' : 'Não autenticado');
    };

    // Check inicial
    checkAuth();

    // Listener para mudanças no localStorage (outro aba/janela)
    const handleStorageChange = () => {
      checkAuth();
    };

    window.addEventListener('storage', handleStorageChange);
    
    // Acordar o backend na primeira carga
    const wakeupBackend = async () => {
      try {
        await api.get('users/debug/', { timeout: 5000 }).catch(() => {});
      } catch (e) {
        // Silenciar erros
      }
    };
    
    wakeupBackend();

    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<Register />} />
        <Route path="/" element={<ProtectedRoute element={<Feed />} isAuthenticated={isAuthenticated} />} />
        <Route path="/perfil/:username" element={<ProtectedRoute element={<Profile />} isAuthenticated={isAuthenticated} />} />
      </Routes>
    </Router>
  );
}

export default App;