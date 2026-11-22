import { useState } from 'react'
import Navbar, { PAGE_ANALYZE, PAGE_EXPERIMENTS, PAGE_ABOUT } from './components/Navbar'
import AnalyzePage from './pages/AnalyzePage'
import ExperimentsPage from './pages/ExperimentsPage'
import AboutPage from './pages/AboutPage'
import './index.css'

export default function App() {
  const [currentPage, setCurrentPage] = useState(PAGE_ANALYZE)
  const [backendStatus, setBackendStatus] = useState('checking')

  const renderPage = () => {
    switch (currentPage) {
      case PAGE_ANALYZE:
        return <AnalyzePage backendStatus={backendStatus} />
      case PAGE_EXPERIMENTS:
        return <ExperimentsPage />
      case PAGE_ABOUT:
        return <AboutPage />
      default:
        return <AnalyzePage backendStatus={backendStatus} />
    }
  }

  return (
    <div className="app-layout">
      <Navbar
        currentPage={currentPage}
        onNavigate={setCurrentPage}
        onStatusChange={setBackendStatus}
      />
      <main className="main-content">
        {renderPage()}
      </main>
      <footer className="footer">
        <div>
          BananaAI · Đề tài: Phân tích độ chín và chất lượng quả chuối bằng học sâu ·{' '}
          <span style={{ color: 'var(--accent-yellow)' }}>ResNet50</span>
        </div>
        <div style={{ marginTop: 4, fontSize: 12 }}>
          Mô hình phân tích dấu hiệu hình ảnh — không kết luận an toàn thực phẩm
        </div>
      </footer>
    </div>
  )
}
