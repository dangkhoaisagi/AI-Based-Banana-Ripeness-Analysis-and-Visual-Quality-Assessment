import { useState, useEffect } from 'react';
import { fetchExperiments } from '../api';

const METRIC_LABELS = {
  Accuracy: 'Accuracy',
  Macro_Precision: 'Macro Precision',
  Macro_Recall: 'Macro Recall',
  Macro_F1: 'Macro F1',
  Test_Loss: 'Test Loss',
  Training_Time_Seconds: 'Thời gian train (s)',
  Selected_Stage: 'Giai đoạn',
};

const MODEL_ICONS = {
  ResNet50: '🏆',
  EfficientNetB0: '⚡',
  DenseNet121: '🔷',
  MobileNetV3Small: '📱',
  InceptionV3: '🌀',
};

export default function ExperimentsPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeDataset, setActiveDataset] = useState(0);

  useEffect(() => {
    fetchExperiments()
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="experiments-layout">
        <div className="empty-state">
          <span className="empty-state-icon">⏳</span>
          <div className="empty-state-title">Đang tải dữ liệu thực nghiệm...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="experiments-layout">
        <div className="error-box">
          <span>❌</span>
          <div>
            <div style={{ fontWeight: 600 }}>Không thể tải dữ liệu</div>
            <div style={{ fontSize: 13, marginTop: 4 }}>{error}</div>
          </div>
        </div>
      </div>
    );
  }

  const experiments = data?.experiments || [];
  const current = experiments[activeDataset];

  return (
    <div>
      <div className="hero">
        <div className="hero-badge">📊 Kết Quả Thực Nghiệm</div>
        <h1>So Sánh Năm Kiến Trúc</h1>
        <p>
          Kết quả thực nghiệm trên ba bộ dữ liệu với năm kiến trúc học sâu.
          Dữ liệu đọc trực tiếp từ file CSV kết quả.
        </p>
      </div>

      <div className="experiments-layout">
        {/* Info box */}
        <div className="info-box">
          <strong>ℹ️ Lưu ý:</strong> Các chỉ số này là kết quả từ tập test trong thực nghiệm (được cung cấp qua CSV).
          Checkpoint .keras được cung cấp là ResNet50 — chưa xác minh chắc chắn rằng đây là checkpoint
          tạo ra các dòng CSV này. Macro F1 được dùng làm tiêu chí so sánh chính vì đánh giá đồng đều các lớp.
        </div>

        {/* Dataset tabs */}
        <div className="dataset-tabs" role="tablist">
          {experiments.map((exp, i) => (
            <button
              key={i}
              className={`dataset-tab ${activeDataset === i ? 'active' : ''}`}
              onClick={() => setActiveDataset(i)}
              role="tab"
              id={`tab-dataset-${i}`}
              aria-selected={activeDataset === i}
            >
              {getDatasetShortName(exp.dataset)}
            </button>
          ))}
        </div>

        {/* Table */}
        {current ? (
          <DatasetTable experiment={current} />
        ) : (
          <div className="empty-state">
            <span className="empty-state-icon">📂</span>
            <div className="empty-state-title">Không có dữ liệu</div>
          </div>
        )}
      </div>
    </div>
  );
}

function DatasetTable({ experiment }) {
  const { dataset, task, filename, status, rows, best_model_by_macro_f1 } = experiment;

  const taskLabel = task === 'ripeness' ? 'Phân loại độ chín' : 'Phân loại chất lượng';

  if (status !== 'ok') {
    return (
      <div className="card">
        <div className="card-title">📊 {dataset}</div>
        <div className="error-box">
          <span>⚠️</span>
          <div>
            <div style={{ fontWeight: 600 }}>
              {status === 'file_missing' ? 'File CSV không tìm thấy' : 'Lỗi đọc file'}
            </div>
            <div style={{ fontSize: 12, marginTop: 4 }}>{filename}</div>
          </div>
        </div>
      </div>
    );
  }

  // Lọc cột cần hiển thị (bỏ Task, vì đã biết từ dataset)
  const cols = ['Model', 'Selected_Stage', 'Accuracy', 'Macro_Precision', 'Macro_Recall', 'Macro_F1', 'Test_Loss'];

  return (
    <div className="slide-in">
      <div style={{ marginBottom: 16 }}>
        <div style={{ fontSize: 20, fontWeight: 700, fontFamily: 'Outfit', marginBottom: 4 }}>
          {dataset}
        </div>
        <div style={{ fontSize: 14, color: 'var(--text-muted)', display: 'flex', gap: 16, flexWrap: 'wrap' }}>
          <span>📋 Tác vụ: {taskLabel}</span>
          <span>📁 Nguồn: {filename}</span>
          {best_model_by_macro_f1 && (
            <span>🏆 Tốt nhất (Macro F1): <strong style={{ color: 'var(--accent-yellow)' }}>{best_model_by_macro_f1}</strong></span>
          )}
        </div>
      </div>

      <div className="table-wrapper">
        <table id={`table-${task}`}>
          <thead>
            <tr>
              {cols.map(col => (
                <th key={col}>
                  {METRIC_LABELS[col] || col}
                  {col === 'Macro_F1' && ' ↓'}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows
              .filter(r => r.Model)
              .sort((a, b) => (b.Macro_F1 || 0) - (a.Macro_F1 || 0))
              .map((row, i) => {
                const isBest = row.Model === best_model_by_macro_f1;
                return (
                  <tr key={i} className={isBest ? 'best-row' : ''}>
                    {cols.map(col => (
                      <td key={col}>
                        {col === 'Model' ? (
                          <div className="model-name">
                            <span>{MODEL_ICONS[row.Model] || '🔹'}</span>
                            {row.Model}
                            {isBest && <span className="best-badge">Best</span>}
                          </div>
                        ) : col === 'Selected_Stage' ? (
                          <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                            {row[col] || '—'}
                          </span>
                        ) : typeof row[col] === 'number' ? (
                          <span className="metric-value">
                            {col === 'Test_Loss'
                              ? row[col].toFixed(4)
                              : col === 'Training_Time_Seconds'
                                ? Math.round(row[col]) + 's'
                                : (row[col] * 100).toFixed(2) + '%'}
                          </span>
                        ) : (
                          row[col] ?? '—'
                        )}
                      </td>
                    ))}
                  </tr>
                );
              })}
          </tbody>
        </table>
      </div>

      {/* Macro F1 explanation */}
      <div className="note-box" style={{ marginTop: 16 }}>
        <strong>Macro F1</strong>: Trung bình F1 của tất cả các lớp với trọng số bằng nhau — tiêu chí phù hợp
        khi các lớp có số lượng mẫu không cân bằng. Dòng nổi bật màu vàng là mô hình đứng đầu theo Macro F1.
      </div>
    </div>
  );
}

function getDatasetShortName(dataset) {
  if (dataset?.includes('Banalyzer')) return 'Banalyzer';
  if (dataset?.includes('RGB')) return 'RGB & Spectral';
  return 'Ripeness';
}
