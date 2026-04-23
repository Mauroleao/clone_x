import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const navigate = useNavigate();

  async function handleSearch(e) {
    const value = e.target.value;
    setQuery(value);

    if (value.trim().length < 2) {
      setResults([]);
      setShowResults(false);
      return;
    }

    try {
      const response = await api.get('posts/');
      const filtered = response.data.filter(post =>
        post.content.toLowerCase().includes(value.toLowerCase()) ||
        post.author_username.toLowerCase().includes(value.toLowerCase())
      );
      setResults(filtered);
      setShowResults(true);
    } catch (error) {
      console.error('Erro ao buscar:', error);
    }
  }

  function handleSelectPost(postId) {
    setQuery('');
    setShowResults(false);
    window.scrollTo(0, 0);
  }

  return (
    <div style={{ position: 'relative', marginBottom: '20px' }}>
      <input
        type="text"
        placeholder="🔍 Buscar posts..."
        value={query}
        onChange={handleSearch}
        style={{
          width: '100%',
          padding: '12px 15px',
          border: '1px solid #ddd',
          borderRadius: '25px',
          fontSize: '14px',
          boxSizing: 'border-box',
          backgroundColor: '#f5f5f5'
        }}
      />

      {showResults && results.length > 0 && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          right: 0,
          backgroundColor: '#fff',
          border: '1px solid #ddd',
          borderRadius: '12px',
          maxHeight: '300px',
          overflowY: 'auto',
          zIndex: 1000,
          marginTop: '5px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
        }}>
          {results.map(post => (
            <div
              key={post.id}
              onClick={() => handleSelectPost(post.id)}
              style={{
                padding: '12px 15px',
                borderBottom: '1px solid #eee',
                cursor: 'pointer',
                transition: '0.2s'
              }}
              onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#f5f5f5'}
              onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#fff'}
            >
              <strong style={{ color: '#17bf63' }}>@{post.author_username}</strong>
              <p style={{ margin: '5px 0 0 0', fontSize: '14px', color: '#666' }}>
                {post.content.substring(0, 50)}...
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Search;
