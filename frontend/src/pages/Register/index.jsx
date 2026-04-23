import { useState } from 'react';
import api from '../../services/api';
import { useNavigate, Link } from 'react-router-dom';

function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Senhas não conferem');
      return;
    }

    if (password.length < 6) {
      setError('Senha deve ter no mínimo 6 caracteres');
      return;
    }

    try {
      setLoading(true);
      await api.post('users/register/', { 
        username, 
        email, 
        password 
      }, { timeout: 30000 });

      alert('Conta criada com sucesso!');
      navigate('/login');
    } catch (err) {
      if (err.code === 'ECONNABORTED') {
        setError('Tempo esgotado. O servidor está respondendo lentamente. Tente novamente.');
      } else {
        setError(err.response?.data?.error || 'Erro ao criar conta');
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <h1 style={styles.title}>X</h1>
        <h2 style={styles.subtitle}>Criar conta</h2>
        
        {error && <div style={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit} style={styles.form}>
          <input 
            type="text" 
            placeholder="Usuário" 
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={styles.input}
          />
          
          <input 
            type="email" 
            placeholder="Email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={styles.input}
          />
          
          <input 
            type="password" 
            placeholder="Senha" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={styles.input}
          />

          <input 
            type="password" 
            placeholder="Confirmar senha" 
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            style={styles.input}
          />
          
          <button 
            type="submit" 
            disabled={loading}
            style={styles.button}
          >
            {loading ? 'Criando conta...' : 'Criar conta'}
          </button>
        </form>

        <div style={styles.divider}></div>

        <p style={styles.loginText}>
          Já tem conta? <Link to="/login" style={styles.link}>Entrar</Link>
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
    color: '#c33',
    padding: '10px',
    borderRadius: '8px',
    marginBottom: '15px',
    fontSize: '14px',
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
  loginText: {
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

export default Register;
