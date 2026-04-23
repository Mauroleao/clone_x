import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import Post from '../../components/Post';
import Navbar from '../../components/Navbar';
import ProfileEditModal from '../../components/ProfileEditModal';

function Profile() {
  const { username } = useParams();
  const [userPosts, setUserPosts] = useState([]);
  const [isFollowing, setIsFollowing] = useState(false);
  const [followersCount, setFollowersCount] = useState(0);
  const [followingCount, setFollowingCount] = useState(0);
  const [currentUser, setCurrentUser] = useState(null);
  const [profileUser, setProfileUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploadingPhoto, setUploadingPhoto] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        
        const postsResponse = await api.get('posts/');
        const filtered = postsResponse.data.filter(p => p.author_username === username);
        setUserPosts(filtered);

        const currentResponse = await api.get(`users/profile/${username}/`);
        setProfileUser(currentResponse.data);

        const myProfileResponse = await api.get(`users/profile/`).catch(() => null);
        if (myProfileResponse) {
          setCurrentUser(myProfileResponse.data);
        }
      } catch (err) { 
        console.error('Erro ao carregar perfil:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [username]);

  async function handleFollow() {
    try {
      const resp = await api.post(`users/follow/${username}/`);
      if (resp.status === 201) {
        setIsFollowing(true);
        setFollowersCount(followersCount + 1);
      } else if (resp.status === 200) {
        setIsFollowing(false);
        setFollowersCount(Math.max(0, followersCount - 1));
      }
    } catch (err) { 
      console.error('Erro ao seguir/deixar de seguir:', err);
    }
  }

  async function handlePhotoUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    try {
      setUploadingPhoto(true);
      const formData = new FormData();
      formData.append('photo', file);

      const response = await api.patch('users/profile/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setProfileUser(response.data);
      setCurrentUser(response.data);
    } catch (err) {
      console.error('Erro ao fazer upload da foto:', err);
      alert('Erro ao enviar foto de perfil');
    } finally {
      setUploadingPhoto(false);
    }
  }

  const isOwnProfile = currentUser && currentUser.username === username;
  const profileData = profileUser || { username };
  const displayName = profileData.first_name || profileData.last_name 
    ? `${profileData.first_name} ${profileData.last_name}`.trim()
    : null;

  if (loading) {
    return (
      <div style={{ backgroundColor: '#f0f2f5', minHeight: '100vh' }}>
        <Navbar />
        <div style={{ textAlign: 'center', padding: '40px 20px' }}>Carregando...</div>
      </div>
    );
  }

  return (
    <div style={{ backgroundColor: '#f0f2f5', minHeight: '100vh' }}>
      <Navbar />
      <div style={{ maxWidth: '600px', margin: '0 auto', padding: '0 15px' }}>
        {/* Header do Perfil */}
        <div style={{
          backgroundColor: '#fff',
          borderBottom: '1px solid #ddd',
          padding: '15px',
          position: 'sticky',
          top: 0,
          zIndex: 10
        }}>
          <button
            onClick={() => navigate(-1)}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '16px',
              cursor: 'pointer',
              color: '#17bf63',
              marginBottom: '10px'
            }}
          >
            ← Voltar
          </button>
          <h2 style={{ margin: '0 0 5px 0' }}>@{username}</h2>
          <p style={{ margin: '0 0 15px 0', color: '#666', fontSize: '14px' }}>
            {userPosts.length} {userPosts.length === 1 ? 'post' : 'posts'}
          </p>
        </div>

        {/* Card do Perfil */}
        <div style={{
          backgroundColor: '#fff',
          padding: '20px',
          border: '1px solid #ddd',
          borderRadius: '12px',
          marginBottom: '20px',
          marginTop: '10px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '15px' }}>
            <div style={{ position: 'relative' }}>
              {profileData.profile?.photo_url ? (
                <img 
                  src={profileData.profile.photo_url}
                  alt="Foto de perfil"
                  style={{
                    width: '100px',
                    height: '100px',
                    borderRadius: '50%',
                    objectFit: 'cover',
                    border: '3px solid #17bf63'
                  }}
                />
              ) : (
                <div style={{
                  width: '100px',
                  height: '100px',
                  backgroundColor: '#17bf63',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '40px',
                  color: '#fff'
                }}>
                  {username?.charAt(0).toUpperCase()}
                </div>
              )}
              
              {isOwnProfile && (
                <label style={{
                  position: 'absolute',
                  bottom: '0',
                  right: '0',
                  backgroundColor: '#17bf63',
                  borderRadius: '50%',
                  padding: '8px',
                  cursor: 'pointer',
                  fontSize: '16px',
                  color: '#fff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: '35px',
                  height: '35px'
                }}>
                  📷
                  <input 
                    type="file" 
                    accept="image/*" 
                    onChange={handlePhotoUpload}
                    disabled={uploadingPhoto}
                    style={{ display: 'none' }}
                  />
                </label>
              )}
            </div>

            <div style={{ flex: 1 }}>
              <h2 style={{ margin: '0 0 2px 0' }}>@{username}</h2>
              {displayName && (
                <p style={{ margin: '0 0 5px 0', fontWeight: '500', fontSize: '15px', color: '#333' }}>
                  {displayName}
                </p>
              )}
              {profileData.profile?.bio && (
                <p style={{ margin: '0 0 10px 0', color: '#666', fontSize: '13px' }}>
                  {profileData.profile.bio}
                </p>
              )}
              <div style={{ display: 'flex', gap: '20px', fontSize: '14px' }}>
                <span><strong>{followingCount}</strong> Seguindo</span>
                <span><strong>{followersCount}</strong> Seguidores</span>
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            {isOwnProfile ? (
              <button
                onClick={() => setShowEditModal(true)}
                style={{
                  flex: 1,
                  padding: '10px 20px',
                  backgroundColor: '#17bf63',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '25px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  fontSize: '14px',
                  transition: '0.2s'
                }}
                onMouseOver={(e) => e.target.style.backgroundColor = '#14a85a'}
                onMouseOut={(e) => e.target.style.backgroundColor = '#17bf63'}
              >
                ⚙️ Editar Perfil
              </button>
            ) : (
              <button
                onClick={handleFollow}
                style={{
                  flex: 1,
                  padding: '10px 20px',
                  backgroundColor: isFollowing ? '#ccc' : '#17bf63',
                  color: isFollowing ? '#666' : '#fff',
                  border: 'none',
                  borderRadius: '25px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  fontSize: '14px',
                  transition: '0.2s'
                }}
                onMouseOver={(e) => {
                  if (!isFollowing) {
                    e.target.style.backgroundColor = '#14a85a';
                  }
                }}
                onMouseOut={(e) => {
                  if (!isFollowing) {
                    e.target.style.backgroundColor = '#17bf63';
                  }
                }}
              >
                {isFollowing ? '✓ Seguindo' : '+ Seguir'}
              </button>
            )}
          </div>
        </div>

        {/* Posts do Usuário */}
        <div>
          <h3 style={{ padding: '15px 0', borderBottom: '1px solid #ddd' }}>Posts</h3>
          {userPosts.length === 0 ? (
            <div style={{
              textAlign: 'center',
              padding: '40px 20px',
              color: '#666'
            }}>
              <p>Nenhum post ainda</p>
            </div>
          ) : (
            userPosts.map(post => <Post key={post.id} post={post} onUpdate={() => {}} />)
          )}
        </div>
      </div>

      {showEditModal && (
        <ProfileEditModal
          profile={profileData}
          onClose={() => setShowEditModal(false)}
          onSave={(updatedProfile) => {
            setProfileUser(updatedProfile);
            setCurrentUser(updatedProfile);
            setShowEditModal(false);
          }}
        />
      )}
    </div>
  );
}

export default Profile;