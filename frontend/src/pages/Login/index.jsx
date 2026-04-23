import { useState } from 'react';
import api from '../../services/api';
import { useNavigate, Link } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    
    if (!username.trim() || !password.trim()) {
      setError('Usuário e senha são obrigatórios');
      return;
    }
    
    try {
      setLoading(true);
      console.log('Tentando fazer login...', { username });
      
      // Limpar tokens antigos antes de fazer login (evita usar token inválido)
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      
      const response = await api.post('users/login/', { username, password }, { timeout: 30000 });
      
      console.log('Login bem-sucedido! Salvando tokens...', response.data);
      
      if (!response.data.access || !response.data.refresh) {
        throw new Error('Tokens não recebidos do servidor');
      }
      
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      localStorage.setItem('username', username);
      
      console.log('Tokens salvos. Navegando para home...');
      
      // Força um reload completo para que o App.jsx pegue o novo token no localStorage
      window.location.href = '/';
    } catch (error) {
      console.error('Erro detalhado no login:', {
        message: error.message,
        code: error.code,
        status: error.response?.status,
        data: error.response?.data,
        fullError: error
      });
      
      if (error.code === 'ECONNABORTED') {
        setError('Tempo esgotado. O servidor está respondendo lentamente. Tente novamente.');
      } else if (error.response?.status === 401) {
        setError('Usuário ou senha inválidos');
      } else if (error.response?.status >= 500) {
        setError('Erro no servidor. Tente novamente mais tarde.');
      } else if (!error.response) {
        setError('Erro de conexão. Verifique sua internet e tente novamente.');
      } else {
        setError(error.response?.data?.detail || error.message || 'Erro ao fazer login. Tente novamente.');
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <h1 style={styles.title}>X</h1>
        <h2 style={styles.subtitle}>Entrar no Clone X</h2>
        
        {error && <div style={styles.error}>{error}</div>}
        
        <form onSubmit={handleSubmit} style={styles.form}>
          <input 
            type="text" 
            placeholder="Usuário" 
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            disabled={loading}
            style={styles.input}
          />
          
          <input 
            type="password" 
            placeholder="Senha" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
            style={styles.input}
          />
          
          <button 
            type="submit" 
            disabled={loading}
            style={styles.button}
          >
            {loading ? 'Conectando...' : 'Entrar'}
          </button>
        </form>

        <div style={styles.divider}></div>

        <p style={styles.registerText}>
          Não tem conta? <Link to="/registro" style={styles.link}>Criar conta</Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    backgroundColor: '#f0f2f5',
  },
  box: {
    backgroundColor: '#fff',
    padding: '40px',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
    width: '100%',
    maxWidth: '400px',
  },
  title: {
    fontSize: '48px',
    fontWeight: 'bold',
    color: '#17bf63',
    margin: '0 0 10px 0',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: '20px',
    marginBottom: '30px',
    color: '#111',
    textAlign: 'center',
  },
  error: {
    backgroundColor: '#fee',
    color: '#c00',
    padding: '12px',
    borderRadius: '8px',
    marginBottom: '20px',
    fontSize: '14px',
    border: '1px solid #fcc',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
  },
  input: {
    padding: '12px',
    marginBottom: '15px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    fontSize: '14px',
    fontFamily: 'inherit',
  },
  button: {
    padding: '12px',
    backgroundColor: '#17bf63',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
    marginBottom: '20px',
  },
  divider: {
    height: '1px',
    backgroundColor: '#ddd',
    marginBottom: '20px',
  },
  registerText: {
    textAlign: 'center',
    color: '#666',
    margin: 0,
  },
  link: {
    color: '#17bf63',
    textDecoration: 'none',
    fontWeight: 'bold',
  },
};

export default Login;