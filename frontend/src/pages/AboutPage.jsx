import { useState, useEffect } from 'react';
import { fetchHealth } from '../api';

export default function AboutPage() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetchHealth().then(setHealth).catch(() => { });
  }, []);

  const models = health?.models || [];

  return (
    <div>
      <div className="hero">
        <div className="hero-badge">📖 Thông Tin Hệ Thống</div>
        <h1>Về BananaAI</h1>
        <p>
          Đề tài nghiên cứu: <em>Phân tích độ chín và chất lượng quả chuối bằng học sâu</em>
        </p>
      </div>

      <div className="experiments-layout">
        {/* Scope */}
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="card-title">🎯 Phạm Vi Ứng Dụng</div>
          <ul style={{ color: 'var(--text-secondary)', fontSize: 14, lineHeight: 2, paddingLeft: 20 }}>
            <li>Phân tích <strong>ảnh RGB</strong> của quả chuối (không yêu cầu dữ liệu phổ)</li>
            <li>Nhận diện <strong>ảnh chuối đơn</strong> — chưa hỗ trợ phát hiện từng quả trong ảnh nhiều chuối</li>
            <li>Mô hình là bộ phân loại ảnh — chưa có lớp "không phải chuối"</li>
            <li>Kết quả là điểm softmax — <strong>không</strong> phải xác suất đã hiệu chuẩn</li>
            <li>Không dùng để kết luận an toàn thực phẩm</li>
          </ul>
        </div>

        {/* Model Status */}
        <div style={{ marginBottom: 24 }}>
          <div style={{ fontFamily: 'Outfit', fontSize: 18, fontWeight: 700, marginBottom: 16 }}>
            🤖 Trạng Thái Model
          </div>
          {models.length === 0 ? (
            <div className="note-box">Đang tải thông tin model... (backend cần chạy trước)</div>
          ) : (
            <div className="model-status-grid">
              {models.map(m => (
                <ModelStatusCard key={m.model_id} model={m} />
              ))}
            </div>
          )}
        </div>

        {/* Architecture */}
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="card-title">🏗️ Kiến Trúc Hệ Thống & Cơ Chế Hybrid AI</div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            <div>
              <div style={{ fontWeight: 600, marginBottom: 8, color: 'var(--accent-yellow)' }}>Frontend</div>
              <ul style={{ color: 'var(--text-secondary)', fontSize: 14, lineHeight: 2, paddingLeft: 20 }}>
                <li>React + Vite</li>
                <li>Vanilla CSS (không dùng Tailwind)</li>
                <li>Cổng: localhost:5173</li>
              </ul>
            </div>
            <div>
              <div style={{ fontWeight: 600, marginBottom: 8, color: 'var(--accent-yellow)' }}>Backend & AI Pipeline</div>
              <ul style={{ color: 'var(--text-secondary)', fontSize: 14, lineHeight: 2, paddingLeft: 20 }}>
                <li>Python 3.11 + FastAPI</li>
                <li>TensorFlow 2.16 + Keras 3 (ResNet50)</li>
                <li>Cổng: localhost:8000</li>
              </ul>
            </div>
          </div>

          <div style={{ marginTop: 18, paddingTop: 16, borderTop: '1px solid var(--border)' }}>
            <div style={{ fontWeight: 600, marginBottom: 6, color: '#34d399', fontSize: 15 }}>
              🛡️ Cơ Chế Hybrid AI & Xử Lý Dữ Liệu Lạ (OOD - Out-of-Distribution)
            </div>
            <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.7 }}>
              Khi gặp các giống chuối lạ (như chuối <strong>Blue Java</strong> có vỏ xanh ngọc ánh lam hoặc chuối trong điều kiện ánh sáng đặc biệt),
              mô hình Deep Learning có thể bị <em>Softmax Overconfidence</em> (quá tự tin sai lệch).
              Hệ thống tích hợp thêm mô-đun <strong>Thị giác máy tính phân tích phổ màu (HSV Color Space Analysis)</strong> để tự động kiểm chứng
              tỷ lệ sắc xanh, sắc vàng và thâm nẫu thực tế, kịp thời phát hiện mâu thuẫn và đề xuất hiệu chỉnh chính xác.
            </p>
          </div>
        </div>

        {/* Label info */}
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="card-title">🏷️ Thứ Tự Nhãn (Xác Minh Từ Notebook)</div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
            <div>
              <div style={{ fontWeight: 600, marginBottom: 10, color: 'var(--text-secondary)' }}>
                Model Độ Chín (index 0→1→2)
              </div>
              <div style={{ fontFamily: 'monospace', fontSize: 13, background: 'rgba(0,0,0,0.3)', padding: 12, borderRadius: 8 }}>
                {['chin (Chín)', 'qua_chin (Quá chín)', 'xanh (Xanh)'].map((l, i) => (
                  <div key={i} style={{ color: ['#fbbf24', '#f97316', '#10b981'][i], marginBottom: 4 }}>
                    [{i}] {l}
                  </div>
                ))}
              </div>
              <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 8 }}>
                Dataset: Banana Ripeness Classification Dataset
              </div>
            </div>
            <div>
              <div style={{ fontWeight: 600, marginBottom: 10, color: 'var(--text-secondary)' }}>
                Model Chất Lượng (index 0→1→2)
              </div>
              <div style={{ fontFamily: 'monospace', fontSize: 13, background: 'rgba(0,0,0,0.3)', padding: 12, borderRadius: 8 }}>
                {['dom (Đốm)', 'thoi (Thối)', 'tot (Tốt)'].map((l, i) => (
                  <div key={i} style={{ color: ['#f97316', '#ef4444', '#10b981'][i], marginBottom: 4 }}>
                    [{i}] {l}
                  </div>
                ))}
              </div>
              <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 8 }}>
                Dataset: Banalyzer · Nhãn quy đổi: ripe→tot, overripe→dom, rotten→thoi
              </div>
            </div>
          </div>
        </div>

        {/* Sources */}
        <div className="card">
          <div className="card-title">📚 Nguồn Dữ Liệu</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {[
              {
                name: 'Banana Ripeness Classification Dataset',
                author: 'S.M. Shahriar',
                license: 'Apache 2.0',
                url: 'https://www.kaggle.com/datasets/shahriar26s/banana-ripeness-classification-dataset',
              },
              {
                name: 'Banalyzer - Banana Ripeness Classification Dataset',
                author: 'Charles C R',
                license: 'MIT',
                url: 'https://www.kaggle.com/datasets/iamchaarles/banalyzer-banana-ripeness-classification-dataset',
              },
              {
                name: 'Banana Ripeness RGB Images and Spectral Data',
                author: 'Kaggle',
                license: '—',
                url: 'https://www.kaggle.com',
              },
            ].map((ds, i) => (
              <div key={i} style={{ padding: 14, background: 'rgba(255,255,255,0.04)', borderRadius: 8, border: '1px solid var(--border)' }}>
                <div style={{ fontWeight: 600, marginBottom: 4 }}>{ds.name}</div>
                <div style={{ fontSize: 13, color: 'var(--text-muted)' }}>
                  Tác giả: {ds.author} · Giấy phép: {ds.license}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function ModelStatusCard({ model }) {
  const statusConfig = {
    ready: { pill: 'ready', label: 'Sẵn sàng', icon: '✅' },
    load_error: { pill: 'error', label: 'Lỗi tải', icon: '❌' },
    file_missing: { pill: 'error', label: 'Thiếu file', icon: '❌' },
    shape_mismatch: { pill: 'error', label: 'Shape mismatch', icon: '⚠️' },
    disabled: { pill: 'disabled', label: 'Chưa bật', icon: '⏸️' },
    not_loaded: { pill: 'loading', label: 'Chưa nạp', icon: '⏳' },
  };

  const cfg = statusConfig[model.status] || { pill: 'loading', label: model.status, icon: '❓' };

  return (
    <div className="model-status-card">
      <div className="model-status-icon">{cfg.icon}</div>
      <div className="model-status-info">
        <div className="model-status-name">{model.architecture}</div>
        <div className="model-status-dataset">{model.dataset}</div>
        {model.input_shape && (
          <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 6, fontFamily: 'monospace' }}>
            Input: {model.input_shape.join('×')} | Output: {model.output_shape?.join('×')}
          </div>
        )}
        <span className={`status-pill ${cfg.pill}`}>{cfg.label}</span>
        {model.error && (
          <div style={{ fontSize: 11, color: 'var(--accent-red)', marginTop: 6, lineHeight: 1.4 }}>
            {model.error.slice(0, 100)}...
          </div>
        )}
      </div>
    </div>
  );
}
