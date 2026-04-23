import { useState } from 'react';
import api from '../../services/api';

function PostForm({ onPostCreated }) {
  const [content, setContent] = useState('');
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  function handleImageChange(e) {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    
    if (!content.trim()) {
      alert('Escreva algo para postar!');
      return;
    }

    const formData = new FormData();
    formData.append('content', content);
    if (image) formData.append('image', image);

    try {
      setLoading(true);
      await api.post('posts/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setContent('');
      setImage(null);
      setPreview(null);
      if (document.getElementById('file-input')) {
        document.getElementById('file-input').value = '';
      }
      onPostCreated();
    } catch (error) {
      console.error('Erro ao criar post:', error);
      alert('Erro ao enviar a postagem.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{
      border: '1px solid #ddd',
      padding: '15px',
      borderRadius: '12px',
      marginBottom: '20px',
      backgroundColor: '#fff',
      boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
    }}>
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'flex', gap: '12px', marginBottom: '12px' }}>
          <div style={{
            width: '48px',
            height: '48px',
            backgroundColor: '#17bf63',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            fontWeight: 'bold',
            fontSize: '20px',
            flexShrink: 0
          }}>
            Y
          </div>

          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="No que você está pensando?!"
            style={{
              flex: 1,
              minHeight: '80px',
              padding: '12px',
              boxSizing: 'border-box',
              border: '1px solid #eee',
              borderRadius: '12px',
              resize: 'none',
              fontSize: '15px',
              fontFamily: 'inherit',
              outline: 'none',
              transition: '0.2s'
            }}
            onFocus={(e) => e.target.style.borderColor = '#17bf63'}
            onBlur={(e) => e.target.style.borderColor = '#eee'}
          />
        </div>

        {preview && (
          <div style={{ position: 'relative', marginBottom: '12px' }}>
            <img
              src={preview}
              alt="Preview"
              style={{
                maxWidth: '100%',
                maxHeight: '200px',
                borderRadius: '12px',
                objectFit: 'cover'
              }}
            />
            <button
              type="button"
              onClick={() => {
                setImage(null);
                setPreview(null);
                if (document.getElementById('file-input')) {
                  document.getElementById('file-input').value = '';
                }
              }}
              style={{
                position: 'absolute',
                top: '8px',
                right: '8px',
                backgroundColor: 'rgba(0,0,0,0.5)',
                color: 'white',
                border: 'none',
                borderRadius: '50%',
                width: '32px',
                height: '32px',
                cursor: 'pointer',
                fontSize: '18px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              ✕
            </button>
          </div>
        )}

        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          paddingTop: '12px',
          borderTop: '1px solid #eee'
        }}>
          <label
            htmlFor="file-input"
            style={{
              cursor: 'pointer',
              fontSize: '20px',
              transition: '0.2s',
              display: 'inline-block'
            }}
            onMouseOver={(e) => e.currentTarget.style.opacity = '0.7'}
            onMouseOut={(e) => e.currentTarget.style.opacity = '1'}
          >
            🖼️
          </label>
          <input
            id="file-input"
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            style={{ display: 'none' }}
          />

          <button
            type="submit"
            disabled={loading || !content.trim()}
            style={{
              padding: '10px 30px',
              backgroundColor: content.trim() && !loading ? '#17bf63' : '#ccc',
              color: 'white',
              border: 'none',
              borderRadius: '25px',
              cursor: content.trim() && !loading ? 'pointer' : 'not-allowed',
              fontWeight: 'bold',
              fontSize: '15px',
              transition: '0.2s'
            }}
            onMouseOver={(e) => {
              if (content.trim() && !loading) {
                e.target.style.backgroundColor = '#14a85a';
              }
            }}
            onMouseOut={(e) => {
              if (content.trim() && !loading) {
                e.target.style.backgroundColor = '#17bf63';
              }
            }}
          >
            {loading ? 'Postando...' : 'Postar'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default PostForm;