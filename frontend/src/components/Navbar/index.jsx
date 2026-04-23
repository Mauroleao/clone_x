import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

function Navbar() {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const [isLoggedIn] = useState(() => {
    const token = localStorage.getItem('access_token');
    return !!token;
  });
  const [username] = useState(() => {
    const storedUsername = localStorage.getItem('username');
    return storedUsername || '';
  });

  function handleLogout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('username');
    navigate('/login');
  }

  function goToProfile() {
    navigate('/');
    setMenuOpen(false);
  }

  function goToMyProfile() {
    if (username) {
      navigate(`/perfil/${username}`);
      setMenuOpen(false);
    }
  }

  function goToEditProfile() {
    if (username) {
      navigate(`/perfil/${username}`);
      setMenuOpen(false);
    }
  }

  return (
    <nav style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: '12px 20px',
      backgroundColor: '#17bf63',
      color: 'white',
      borderBottom: '1px solid #ddd',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      position: 'sticky',
      top: 0,
      zIndex: 100
    }}>
      <div 
        style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}
        onClick={() => navigate('/')}
      >
        <span style={{ fontSize: '24px' }}>𝕏</span>
        <h2 style={{ margin: 0, fontSize: '18px', fontWeight: 'bold' }}>Clone X</h2>
      </div>

      {isLoggedIn ? (
        <div style={{ position: 'relative' }}>
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            style={{
              background: 'transparent',
              border: '1px solid white',
              color: 'white',
              padding: '8px 16px',
              borderRadius: '20px',
              cursor: 'pointer',
              fontWeight: 'bold',
              fontSize: '14px'
            }}
          >
            Menu ▼
          </button>

          {menuOpen && (
            <div style={{
              position: 'absolute',
              top: '40px',
              right: '0',
              backgroundColor: 'white',
              color: '#111',
              borderRadius: '8px',
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
              minWidth: '180px',
              zIndex: 1000
            }}>
              <button
                onClick={goToProfile}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: '12px 16px',
                  border: 'none',
                  background: 'none',
                  cursor: 'pointer',
                  textAlign: 'left',
                  fontSize: '14px',
                  borderBottom: '1px solid #eee'
                }}
              >
                Home
              </button>
              <button
                onClick={goToMyProfile}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: '12px 16px',
                  border: 'none',
                  background: 'none',
                  cursor: 'pointer',
                  textAlign: 'left',
                  fontSize: '14px',
                  borderBottom: '1px solid #eee'
                }}
              >
                👤 Meu Perfil
              </button>
              <button
                onClick={goToEditProfile}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: '12px 16px',
                  border: 'none',
                  background: 'none',
                  cursor: 'pointer',
                  textAlign: 'left',
                  fontSize: '14px',
                  borderBottom: '1px solid #eee',
                  color: '#17bf63',
                  fontWeight: 'bold'
                }}
              >
                ⚙️ Editar Perfil
              </button>
              <button
                onClick={handleLogout}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: '12px 16px',
                  border: 'none',
                  background: 'none',
                  cursor: 'pointer',
                  textAlign: 'left',
                  fontSize: '14px',
                  color: '#ef4444'
                }}
              >
                Sair
              </button>
            </div>
          )}
        </div>
      ) : (
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={() => navigate('/login')}
            style={{
              background: 'white',
              color: '#17bf63',
              border: 'none',
              padding: '8px 24px',
              borderRadius: '20px',
              cursor: 'pointer',
              fontWeight: 'bold',
              fontSize: '14px'
            }}
          >
            Entrar
          </button>
          <button
            onClick={() => navigate('/registro')}
            style={{
              background: 'transparent',
              color: 'white',
              border: '1px solid white',
              padding: '8px 24px',
              borderRadius: '20px',
              cursor: 'pointer',
              fontWeight: 'bold',
              fontSize: '14px'
            }}
          >
            Registrar
          </button>
        </div>
      )}
    </nav>
  );
}

export default Navbar;