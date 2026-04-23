import { useEffect, useState } from 'react'
import api from '../services/api'

export function DebugInfo() {
  const [info, setInfo] = useState({
    apiUrl: '',
    viteEnv: {},
    hasToken: false,
    backendStatus: 'checking...'
  })

  useEffect(() => {
    // Coletar informações de debug
    const debugInfo = {
      apiUrl: api.defaults.baseURL,
      viteEnv: {
        VITE_API_URL: import.meta.env.VITE_API_URL,
        MODE: import.meta.env.MODE,
        DEV: import.meta.env.DEV,
      },
      hasToken: !!localStorage.getItem('access_token'),
      backendStatus: 'unknown'
    }

    // Testar conexão com backend
    fetch(api.defaults.baseURL + 'users/debug/')
      .then(r => debugInfo.backendStatus = r.status === 200 ? '✅ Online' : `❌ ${r.status}`)
      .catch(() => debugInfo.backendStatus = '❌ Offline')
      .finally(() => setInfo(debugInfo))
  }, [])

  return (
    <div style={{
      position: 'fixed',
      bottom: 10,
      right: 10,
      background: '#222',
      color: '#0f0',
      padding: '10px',
      fontFamily: 'monospace',
      fontSize: '12px',
      maxWidth: '300px',
      borderRadius: '5px',
      zIndex: 9999,
      border: '1px solid #0f0'
    }}>
      <div>🔧 DEBUG INFO</div>
      <div>API URL: {info.apiUrl}</div>
      <div>VITE_API_URL: {info.viteEnv.VITE_API_URL}</div>
      <div>Backend: {info.backendStatus}</div>
      <div>Token: {info.hasToken ? '✅ Salvo' : '❌ Não encontrado'}</div>
    </div>
  )
}
