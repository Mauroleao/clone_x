import { useState, useEffect } from 'react';
import api from '../../services/api';
import PostForm from '../../components/PostForm';
import Post from '../../components/Post';
import Navbar from '../../components/Navbar';
import Search from '../../components/Search';

function Feed() {
  const [posts, setPosts] = useState([]);
  const [refreshKey, setRefreshKey] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPosts() {
      try {
        setLoading(true);
        const response = await api.get('posts/');
        const sortedPosts = response.data.sort((a, b) => 
          new Date(b.created_at) - new Date(a.created_at)
        );
        setPosts(sortedPosts);
      } catch (error) {
        console.error('Erro ao carregar o feed:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchPosts();
  }, [refreshKey]);

  function handleTriggerUpdate() {
    setRefreshKey(chaveAntiga => chaveAntiga + 1);
  }

  return (
    <div style={{ backgroundColor: '#f0f2f5', minHeight: '100vh', paddingBottom: '40px' }}>
      <Navbar />

      <div style={{ maxWidth: '600px', margin: '0 auto', padding: '0 15px' }}>
        <div style={{
          backgroundColor: '#fff',
          borderBottom: '2px solid #ddd',
          padding: '15px 0',
          position: 'sticky',
          top: '60px',
          zIndex: 50,
          marginBottom: '20px'
        }}>
          <Search />
        </div>

        <PostForm onPostCreated={handleTriggerUpdate} />

        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px 20px', color: '#999' }}>
            <p>Carregando posts...</p>
          </div>
        ) : posts.length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '40px 20px',
            backgroundColor: '#fff',
            borderRadius: '12px',
            border: '1px solid #ddd'
          }}>
            <p style={{ fontSize: '18px', color: '#666', margin: '10px 0' }}>
              Nenhum post ainda!
            </p>
            <p style={{ fontSize: '14px', color: '#999' }}>
              Comece a postar e veja o feed aparecer aqui
            </p>
          </div>
        ) : (
          posts.map(post => (
            <Post
              key={post.id}
              post={post}
              onUpdate={handleTriggerUpdate}
            />
          ))
        )}
      </div>
    </div>
  );
}

export default Feed;