import { useState, useEffect } from 'react';
import { fetchHealth } from '../api';

const PAGE_ANALYZE = 'analyze';
const PAGE_EXPERIMENTS = 'experiments';
const PAGE_ABOUT = 'about';

export default function Navbar({ currentPage, onNavigate }) {
  const [backendStatus, setBackendStatus] = useState('checking');
  const [modelStatuses, setModelStatuses] = useState([]);

  useEffect(() => {
    const check = async () => {
      try {
        const data = await fetchHealth();
        setBackendStatus(data.any_model_ready ? 'ok' : 'degraded');
        setModelStatuses(data.models || []);
      } catch {
        setBackendStatus('offline');
      }
    };
    check();
    // Kiểm tra lại mỗi 30 giây
    const interval = setInterval(check, 30000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { id: PAGE_ANALYZE, label: '🔍 Phân Tích', icon: '🔍' },
    { id: PAGE_EXPERIMENTS, label: '📊 Thực Nghiệm', icon: '📊' },
    { id: PAGE_ABOUT, label: '📖 Thông Tin', icon: '📖' },
  ];

  const statusLabel =
    backendStatus === 'ok' ? 'Sẵn sàng' :
      backendStatus === 'degraded' ? 'Hạn chế' :
        backendStatus === 'offline' ? 'Offline' : 'Đang kết nối...';

  const dotClass =
    backendStatus === 'ok' ? 'ok' :
      backendStatus === 'offline' ? 'error' : '';

  return (
    <nav className="navbar" role="navigation" aria-label="Điều hướng chính">
      <div className="navbar-inner">
        <button
          className="navbar-logo"
          onClick={() => onNavigate(PAGE_ANALYZE)}
          style={{ background: 'none', border: 'none', cursor: 'pointer' }}
          aria-label="Trang chủ BananaAI"
        >
          <span className="navbar-logo-icon">🍌</span>
          <span className="navbar-logo-text">BananaAI</span>
        </button>

        <ul className="navbar-nav" role="list">
          {navItems.map(item => (
            <li key={item.id}>
              <button
                className={`nav-link ${currentPage === item.id ? 'active' : ''}`}
                onClick={() => onNavigate(item.id)}
                id={`nav-${item.id}`}
                aria-current={currentPage === item.id ? 'page' : undefined}
              >
                {item.label}
              </button>
            </li>
          ))}
        </ul>

        <div className="navbar-status" id="backend-status-indicator">
          <div className={`status-dot ${dotClass}`} />
          <span>Backend: {statusLabel}</span>
          {backendStatus === 'ok' && (
            <span style={{ color: 'var(--accent-green)', fontSize: 12 }}>
              ({modelStatuses.filter(m => m.status === 'ready').length}/{modelStatuses.length} model)
            </span>
          )}
        </div>
      </div>
    </nav>
  );
}

export { PAGE_ANALYZE, PAGE_EXPERIMENTS, PAGE_ABOUT };
