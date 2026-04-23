import { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import Comments from '../Comments';

function Post({ post, onUpdate }) {
  const [postData, setPostData] = useState(post);
  
  async function handleLike() {
    try {
      await api.post(`posts/${post.id}/like/`);
      onUpdate();
    } catch (error) {
      console.error("Erro ao curtir post:", error);
    }
  }

  let imageUrl = null;
  if (post.image) {
    if (post.image.startsWith('http')) {
      imageUrl = post.image;
    } else {
      const cleanPath = post.image.startsWith('/') ? post.image : `/${post.image}`;
      imageUrl = `http://127.0.0.1:8000${cleanPath}`;
    }
  }

  function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'agora';
    if (diffMins < 60) return `${diffMins}m`;
    if (diffHours < 24) return `${diffHours}h`;
    if (diffDays < 30) return `${diffDays}d`;
    
    return date.toLocaleDateString('pt-BR');
  }

  return (
    <div style={{
      border: '1px solid #ddd',
      padding: '15px',
      marginBottom: '10px',
      borderRadius: '12px',
      backgroundColor: '#fff',
      transition: '0.2s',
      cursor: 'pointer'
    }}
      onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#fafafa'}
      onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#fff'}
    >
      {/* Header do Post */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '12px', alignItems: 'flex-start' }}>
        {post.author_photo ? (
          <img 
            src={post.author_photo}
            alt="Foto de perfil"
            style={{
              width: '48px',
              height: '48px',
              borderRadius: '50%',
              objectFit: 'cover',
              flexShrink: 0
            }}
          />
        ) : (
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
            {post.author_username?.charAt(0).toUpperCase()}
          </div>
        )}

        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Link
              to={`/perfil/${post.author_username}`}
              style={{ color: '#17bf63', textDecoration: 'none', fontWeight: 'bold' }}
            >
              @{post.author_username}
            </Link>
            <span style={{ color: '#999', fontSize: '14px' }}>
              · {formatDate(post.created_at)}
            </span>
          </div>
        </div>
      </div>

      {/* Conteúdo do Post */}
      <p style={{ wordWrap: 'break-word', fontSize: '15px', margin: '12px 0', lineHeight: '1.5' }}>
        {post.content}
      </p>

      {/* Imagem do Post */}
      {imageUrl && (
        <img
          src={imageUrl}
          alt="Imagem do post"
          style={{
            maxWidth: '100%',
            borderRadius: '12px',
            marginTop: '12px',
            marginBottom: '12px',
            maxHeight: '400px',
            objectFit: 'cover'
          }}
        />
      )}

      {/* Botões de Interação */}
      <div style={{
        display: 'flex',
        gap: '30px',
        marginTop: '15px',
        paddingTop: '12px',
        borderTop: '1px solid #eee',
        color: '#666',
        fontSize: '14px'
      }}>
        <button
          onClick={handleLike}
          style={{
            background: 'none',
            border: 'none',
            padding: '8px 12px',
            borderRadius: '20px',
            cursor: 'pointer',
            color: '#666',
            fontSize: '14px',
            transition: '0.2s',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.backgroundColor = '#ffe0e0';
            e.currentTarget.style.color = '#e91e63';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.backgroundColor = 'transparent';
            e.currentTarget.style.color = '#666';
          }}
        >
          ❤️ <span>{postData.likes_count}</span>
        </button>

        <button
          style={{
            background: 'none',
            border: 'none',
            padding: '8px 12px',
            borderRadius: '20px',
            cursor: 'pointer',
            color: '#666',
            fontSize: '14px',
            transition: '0.2s',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.backgroundColor = '#e3f2fd';
            e.currentTarget.style.color = '#17bf63';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.backgroundColor = 'transparent';
            e.currentTarget.style.color = '#666';
          }}
        >
          💬 <span>{postData.comments_count || 0}</span>
        </button>

        <button
          style={{
            background: 'none',
            border: 'none',
            padding: '8px 12px',
            borderRadius: '20px',
            cursor: 'pointer',
            color: '#666',
            fontSize: '14px',
            transition: '0.2s',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.backgroundColor = '#f0f0f0';
            e.currentTarget.style.color = '#17bf63';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.backgroundColor = 'transparent';
            e.currentTarget.style.color = '#666';
          }}
        >
          🔄 <span>0</span>
        </button>

        <button
          style={{
            background: 'none',
            border: 'none',
            padding: '8px 12px',
            borderRadius: '20px',
            cursor: 'pointer',
            color: '#666',
            fontSize: '14px',
            transition: '0.2s',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.backgroundColor = '#fff3e0';
            e.currentTarget.style.color = '#ff9800';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.backgroundColor = 'transparent';
            e.currentTarget.style.color = '#666';
          }}
        >
          📤 <span>0</span>
        </button>
      </div>

      {/* Seção de Comentários */}
      <Comments 
        postId={postData.id} 
        onCommentAdded={() => {
          setPostData({
            ...postData,
            comments_count: (postData.comments_count || 0) + 1
          });
        }}
      />
    </div>
  );
}

export default Post;