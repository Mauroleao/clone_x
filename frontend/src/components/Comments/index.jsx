import { useState, useEffect } from 'react';
import api from '../../services/api';

function Comments({ postId, onCommentAdded }) {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [showComments, setShowComments] = useState(false);

  useEffect(() => {
    if (showComments) {
      loadComments();
    }
  }, [postId, showComments]);

  async function loadComments() {
    try {
      const response = await api.get(`posts/${postId}/respostas/`);
      setComments(response.data);
    } catch (error) {
      console.error('Erro ao carregar comentários:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleAddComment(e) {
    e.preventDefault();
    if (!newComment.trim()) return;

    try {
      setSubmitting(true);
      const response = await api.post(`posts/${postId}/respostas/`, {
        content: newComment
      });
      setComments([...comments, response.data]);
      setNewComment('');
      if (onCommentAdded) onCommentAdded();
    } catch (error) {
      console.error('Erro ao adicionar comentário:', error);
      alert('Erro ao adicionar comentário');
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDeleteComment(commentId) {
    if (!window.confirm('Tem certeza que deseja deletar este comentário?')) return;

    try {
      await api.delete(`posts/respostas/${commentId}/`);
      setComments(comments.filter(c => c.id !== commentId));
    } catch (error) {
      console.error('Erro ao deletar comentário:', error);
      alert('Erro ao deletar comentário');
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
    <div style={{ marginTop: '12px' }}>
      <button
        onClick={() => setShowComments(!showComments)}
        style={{
          background: 'none',
          border: 'none',
          color: '#17bf63',
          cursor: 'pointer',
          fontSize: '12px',
          fontWeight: 'bold',
          padding: 0
        }}
      >
        {showComments ? '✕ Ocultar comentários' : `💬 Ver comentários (${comments.length})`}
      </button>

      {showComments && (
        <div style={{ marginTop: '12px', borderTop: '1px solid #eee', paddingTop: '12px' }}>
          {/* Formulário para adicionar comentário */}
          <form onSubmit={handleAddComment} style={{ marginBottom: '12px' }}>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-end' }}>
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value.slice(0, 280))}
                placeholder="Adicionar um comentário..."
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  border: '1px solid #ddd',
                  borderRadius: '8px',
                  fontSize: '13px',
                  fontFamily: 'inherit',
                  minHeight: '36px',
                  resize: 'vertical',
                  maxHeight: '100px'
                }}
                disabled={submitting}
              />
              <button
                type="submit"
                disabled={submitting || !newComment.trim()}
                style={{
                  padding: '8px 16px',
                  backgroundColor: newComment.trim() ? '#17bf63' : '#ccc',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '20px',
                  cursor: newComment.trim() && !submitting ? 'pointer' : 'not-allowed',
                  fontSize: '12px',
                  fontWeight: 'bold',
                  whiteSpace: 'nowrap'
                }}
              >
                {submitting ? 'Enviando...' : 'Comentar'}
              </button>
            </div>
            <div style={{ fontSize: '11px', color: '#999', marginTop: '4px', textAlign: 'right' }}>
              {newComment.length}/280
            </div>
          </form>

          {/* Lista de comentários */}
          <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
            {loading ? (
              <div style={{ fontSize: '12px', color: '#999', textAlign: 'center', padding: '8px' }}>
                Carregando...
              </div>
            ) : comments.length === 0 ? (
              <div style={{ fontSize: '12px', color: '#999', textAlign: 'center', padding: '8px' }}>
                Nenhum comentário ainda
              </div>
            ) : (
              comments.map(comment => (
                <div key={comment.id} style={{
                  marginBottom: '12px',
                  padding: '8px 12px',
                  backgroundColor: '#f9f9f9',
                  borderRadius: '8px',
                  fontSize: '13px'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '8px' }}>
                    <div style={{ flex: 1 }}>
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        marginBottom: '4px'
                      }}>
                        {comment.author_photo ? (
                          <img 
                            src={comment.author_photo}
                            alt="Foto"
                            style={{
                              width: '24px',
                              height: '24px',
                              borderRadius: '50%',
                              objectFit: 'cover'
                            }}
                          />
                        ) : (
                          <div style={{
                            width: '24px',
                            height: '24px',
                            borderRadius: '50%',
                            backgroundColor: '#17bf63',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: '#fff',
                            fontSize: '11px',
                            fontWeight: 'bold'
                          }}>
                            {comment.author_username?.charAt(0).toUpperCase()}
                          </div>
                        )}
                        <strong style={{ color: '#17bf63' }}>@{comment.author_username}</strong>
                        <span style={{ color: '#999', fontSize: '11px' }}>· {formatDate(comment.created_at)}</span>
                      </div>
                      <p style={{ margin: '0', color: '#333', wordWrap: 'break-word' }}>
                        {comment.content}
                      </p>
                    </div>
                    <button
                      onClick={() => handleDeleteComment(comment.id)}
                      style={{
                        background: 'none',
                        border: 'none',
                        color: '#ff6b6b',
                        cursor: 'pointer',
                        fontSize: '11px',
                        padding: 0,
                        minWidth: 'auto'
                      }}
                      title="Deletar comentário"
                    >
                      ✕
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Comments;
