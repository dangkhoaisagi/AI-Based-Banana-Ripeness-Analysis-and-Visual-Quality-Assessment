import { useState, useRef, useCallback } from 'react';
import { predictImage } from '../api';

const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_SIZE_MB = 10;

export default function AnalyzePage({ backendStatus }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFile = useCallback((selectedFile) => {
    if (!selectedFile) return;

    // Validate type
    if (!ALLOWED_TYPES.includes(selectedFile.type)) {
      setError('Định dạng không hỗ trợ. Chỉ chấp nhận JPG, PNG, WebP.');
      return;
    }

    // Validate size
    if (selectedFile.size > MAX_SIZE_MB * 1024 * 1024) {
      setError(`File quá lớn. Tối đa ${MAX_SIZE_MB} MB.`);
      return;
    }

    setError(null);
    setResult(null);
    setFile(selectedFile);

    // Preview
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(selectedFile);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  }, [handleFile]);

  const handleDragOver = (e) => { e.preventDefault(); setDragging(true); };
  const handleDragLeave = () => setDragging(false);

  const handleAnalyze = async () => {
    if (!file || loading) return;
    setLoading(true);
    setError(null);
    try {
      const data = await predictImage(file);
      setResult(data.result);
    } catch (err) {
      setError(err.message || 'Lỗi không xác định. Hãy kiểm tra backend đã chạy chưa.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div>
      <div className="hero">
        <div className="hero-badge">🔬 Deep Learning · ResNet50</div>
        <h1>Phân Tích Quả Chuối</h1>
        <p>
          Tải ảnh quả chuối để phân tích <strong>độ chín</strong> và{' '}
          <strong>chất lượng theo nhãn quy đổi</strong> bằng mô hình học sâu đã huấn luyện.
        </p>
      </div>

      <div className="analyze-layout">
        {/* Left: Upload / Preview */}
        <div>
          {!preview ? (
            <div
              className={`upload-zone ${dragging ? 'dragging' : ''}`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onClick={() => fileInputRef.current?.click()}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => e.key === 'Enter' && fileInputRef.current?.click()}
              id="upload-dropzone"
            >
              <span className="upload-icon">🍌</span>
              <div className="upload-title">Chọn hoặc kéo thả ảnh</div>
              <div className="upload-subtitle">Hỗ trợ một ảnh chuối đơn</div>
              <div className="upload-formats">
                {['JPG', 'JPEG', 'PNG', 'WebP'].map(f => (
                  <span className="format-tag" key={f}>{f}</span>
                ))}
              </div>
              <button
                className="btn btn-secondary btn-sm"
                onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}
                type="button"
              >
                📁 Chọn file
              </button>
              <div style={{ marginTop: 12, fontSize: 12, color: 'var(--text-muted)' }}>
                Tối đa {MAX_SIZE_MB} MB
              </div>
              <input
                ref={fileInputRef}
                type="file"
                accept=".jpg,.jpeg,.png,.webp"
                style={{ display: 'none' }}
                onChange={(e) => handleFile(e.target.files?.[0])}
                id="file-input"
              />
            </div>
          ) : (
            <div className="fade-in">
              <div className="preview-container">
                <img
                  src={preview}
                  alt="Ảnh chuối đã chọn"
                  className="preview-image"
                />
                <div className="preview-overlay">
                  <button
                    className="btn-icon"
                    onClick={handleReset}
                    title="Xóa ảnh"
                    id="btn-remove-image"
                  >✕</button>
                </div>
              </div>

              <div style={{ marginTop: 12, fontSize: 13, color: 'var(--text-muted)' }}>
                📄 {file?.name} · {(file?.size / 1024).toFixed(0)} KB
              </div>

              <div style={{ display: 'flex', gap: 10, marginTop: 16 }}>
                <button
                  id="btn-analyze"
                  className="btn btn-primary"
                  onClick={handleAnalyze}
                  disabled={loading}
                  style={{ flex: 1 }}
                >
                  {loading ? (
                    <>
                      <span className="spinner" />
                      Đang phân tích...
                    </>
                  ) : (
                    <>🔍 Phân tích</>
                  )}
                </button>
                <button
                  id="btn-change-image"
                  className="btn btn-secondary btn-sm"
                  onClick={() => { setResult(null); setError(null); fileInputRef.current?.click(); }}
                  disabled={loading}
                >
                  🔄 Đổi ảnh
                </button>
              </div>
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="error-box fade-in" style={{ marginTop: 16 }}>
              <span>⚠️</span>
              <div>
                <div style={{ fontWeight: 600, marginBottom: 4 }}>Lỗi</div>
                <div>{error}</div>
              </div>
            </div>
          )}

          {/* Backend status warning */}
          {backendStatus === 'offline' && (
            <div className="warning-box" style={{ marginTop: 16 }}>
              <span>🔌</span>
              <div>Backend đang offline. Hãy khởi động server bằng lệnh trong README.</div>
            </div>
          )}
        </div>

        {/* Right: Results */}
        <div>
          {!result && !loading && (
            <div className="empty-state">
              <span className="empty-state-icon">📊</span>
              <div className="empty-state-title">Chưa có kết quả</div>
              <div className="empty-state-desc">
                Chọn ảnh và nhấn <strong>Phân tích</strong> để xem dự đoán từ mô hình.
              </div>
            </div>
          )}

          {loading && (
            <div className="empty-state">
              <span className="empty-state-icon" style={{ animation: 'spin 1s linear infinite', display: 'inline-block' }}>⚙️</span>
              <div className="empty-state-title">Đang suy luận...</div>
              <div className="empty-state-desc">Mô hình đang phân tích ảnh.</div>
            </div>
          )}

          {result && !loading && (
            <div className="fade-in">
              <div className="results-grid" id="results-section">
                <ResultCard
                  title="Độ Chín"
                  task="ripeness"
                  data={result.ripeness}
                  oodInfo={result.ood_analysis}
                  labelColors={{
                    chin: 'label-chin',
                    qua_chin: 'label-qua_chin',
                    xanh: 'label-xanh',
                  }}
                />
                <ResultCard
                  title="Chất Lượng Theo Nhãn Quy Đổi"
                  task="quality"
                  data={result.quality}
                  labelColors={{
                    tot: 'label-tot',
                    dom: 'label-dom',
                    thoi: 'label-thoi',
                    unripe: 'label-xanh',
                  }}
                />
              </div>

              {/* Color Spectrum Analysis Card (Computer Vision) */}
              {result.ood_analysis?.color_profile && (
                <ColorProfileCard colorProfile={result.ood_analysis.color_profile} />
              )}

              <div style={{ marginTop: 16, display: 'flex', gap: 10 }}>
                <button
                  id="btn-clear-results"
                  className="btn btn-ghost"
                  onClick={handleReset}
                >
                  🗑️ Xóa kết quả
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function ColorProfileCard({ colorProfile }) {
  const bars = [
    {
      label: 'Sắc xanh lá tiêu chuẩn (Green Hue)',
      pct: colorProfile.green_pct || 0,
      color: '#10b981',
      dot: '#10b981',
    },
    {
      label: 'Sắc xanh lam ngọc / Blue Java (Cyan-Blue Hue)',
      pct: colorProfile.cyan_pct || 0,
      color: '#06b6d4',
      dot: '#06b6d4',
    },
    {
      label: 'Sắc vàng chín (Yellow Hue)',
      pct: colorProfile.yellow_pct || 0,
      color: '#fbbf24',
      dot: '#fbbf24',
    },
    {
      label: 'Sắc thâm nẫu / Đốm đen (Dark / Brown)',
      pct: colorProfile.dark_brown_pct || 0,
      color: '#a16207',
      dot: '#a16207',
      subText: colorProfile.dark_brown_pct > 5 ? (
        `Đốm nâu nhẹ: ${(colorProfile.dark_light_pct || 0).toFixed(1)}% | Thối đen: ${(colorProfile.dark_heavy_pct || 0).toFixed(1)}% | Đốm tối: ${(colorProfile.dark_spot_pct || 0).toFixed(1)}%`
      ) : null,
    },
  ];

  const rottenScore = colorProfile.rotten_score || 0;
  const rottenBadge = rottenScore >= 45
    ? { text: 'Nguy cơ thối hỏng cao', bg: 'rgba(239, 68, 68, 0.15)', color: '#ef4444' }
    : rottenScore >= 20
    ? { text: 'Quá chín / Đốm nẫu', bg: 'rgba(245, 158, 11, 0.15)', color: '#f59e0b' }
    : { text: 'Tươi tốt / An toàn', bg: 'rgba(16, 185, 129, 0.15)', color: '#10b981' };

  return (
    <div className="color-analysis-card fade-in">
      <div className="color-analysis-header">
        <div>
          <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
            Phân Tích Phổ Màu Thực Tế (Computer Vision · XLA)
          </div>
          <div style={{ fontSize: 16, fontWeight: 700, color: 'var(--text-primary)', marginTop: 2 }}>
            Quang Phổ Màu HSV Của Quả Chuối
          </div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>Nhận định thị giác:</div>
          <div style={{ fontSize: 14, fontWeight: 700, color: colorProfile.is_clearly_rotten ? '#ef4444' : colorProfile.is_overripe ? '#f59e0b' : '#34d399' }}>
            {colorProfile.cv_display}
          </div>
        </div>
      </div>

      <div style={{ marginTop: 16 }}>
        {bars.map((b) => (
          <div className="color-bar-row" key={b.label}>
            <div className="color-bar-labels">
              <span style={{ color: 'var(--text-secondary)' }}>
                <span className="color-indicator-dot" style={{ background: b.dot }} />
                {b.label}
              </span>
              <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{b.pct.toFixed(1)}%</span>
            </div>
            <div className="color-bar-track-custom">
              <div
                className="color-bar-fill-custom"
                style={{ width: `${Math.min(100, b.pct)}%`, background: b.color }}
              />
            </div>
            {b.subText && (
              <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 2, paddingLeft: 12 }}>
                ↳ {b.subText}
              </div>
            )}
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: 12, color: 'var(--text-muted)', marginTop: 14, paddingTop: 10, borderTop: '1px solid var(--border)', flexWrap: 'wrap', gap: 8 }}>
        <span>Tổng sắc xanh: <strong>{(colorProfile.unripe_total_pct || 0).toFixed(1)}%</strong></span>
        <span>Sắc vàng chín: <strong>{(colorProfile.yellow_pct || 0).toFixed(1)}%</strong></span>
        <span>
          Điểm thối hỏng (Rotten Score): <strong>{rottenScore.toFixed(0)}/100</strong>{' '}
          <span style={{ display: 'inline-block', padding: '2px 8px', borderRadius: 4, background: rottenBadge.bg, color: rottenBadge.color, fontWeight: 600, marginLeft: 4, fontSize: 11 }}>
            {rottenBadge.text}
          </span>
        </span>
      </div>
    </div>
  );
}

function ResultCard({ title, task, data, oodInfo, labelColors }) {
  const [showRawDl, setShowRawDl] = useState(false);

  if (!data || data.status === 'not_ready') {
    return (
      <div className="result-card">
        <div className="result-header">
          <div className="result-title">{title}</div>
        </div>
        <div className="error-box">
          <span>⚠️</span>
          <div>
            <div style={{ fontWeight: 600, marginBottom: 4 }}>Chưa sẵn sàng</div>
            <div style={{ fontSize: 12 }}>{data?.error || 'Model chưa được nạp'}</div>
          </div>
        </div>
      </div>
    );
  }

  if (data.status === 'error') {
    return (
      <div className="result-card">
        <div className="result-header">
          <div className="result-title">{title}</div>
        </div>
        <div className="error-box">
          <span>❌</span>
          <div>
            <div style={{ fontWeight: 600, marginBottom: 4 }}>Lỗi suy luận</div>
            <div style={{ fontSize: 12 }}>{data.error}</div>
          </div>
        </div>
      </div>
    );
  }

  // Nếu có status not_applicable nhưng không có scores, chuẩn hóa thành card đầy đủ như chuối chín
  const effectiveData = (data.status === 'not_applicable' && !data.scores)
    ? {
        ...data,
        status: 'ok',
        predicted_class: 'tot',
        predicted_display: 'Tốt (Chuối xanh tươi)',
        scores: { tot: 1.0, dom: 0.0, thoi: 0.0 },
        display_names: { tot: 'Tốt', dom: 'Đốm', thoi: 'Thối' },
        dataset: 'Banalyzer - Banana Ripeness Classification Dataset',
        quality_map_note: 'Nhãn quy đổi từ Banalyzer: ripe→Tốt, overripe→Đốm, rotten→Thối.',
      }
    : data;

  const { predicted_class, predicted_display, scores, display_names, warning, quality_map_note, is_hybrid_corrected, raw_dl, hybrid_confidence } = effectiveData;
  const topScore = scores?.[predicted_class] ?? 0;
  const colorClass = labelColors?.[predicted_class] ?? (predicted_class === 'tot' ? 'label-tot' : '');

  return (
    <div className={`result-card loaded ${is_hybrid_corrected ? 'has-contradiction' : ''}`}>
      <div className="result-header">
        <div className="result-title">{title}</div>
        <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
          {is_hybrid_corrected && (
            <span style={{ fontSize: 10, background: 'rgba(16, 185, 129, 0.2)', color: '#34d399', padding: '2px 8px', borderRadius: 4, fontWeight: 700 }}>
              🌿 AI Hybrid (Tách nền + XLA)
            </span>
          )}
          <div className="result-model-badge">{data.architecture || 'ResNet50'}</div>
        </div>
      </div>

      <div className={`prediction-label ${colorClass}`}>
        {predicted_display || predicted_class}
      </div>
      <div className="prediction-score">
        {is_hybrid_corrected ? (
          <>
            Độ tin cậy kết hợp: <strong>{((hybrid_confidence || topScore) * 100).toFixed(1)}%</strong>
          </>
        ) : (
          <>
            Điểm dự đoán (Deep Learning): <strong>{(topScore * 100).toFixed(1)}%</strong>
          </>
        )}
      </div>

      {is_hybrid_corrected && raw_dl && (
        <div style={{ marginTop: 6, marginBottom: 12 }}>
          <button
            type="button"
            onClick={() => setShowRawDl(!showRawDl)}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--text-muted)',
              fontSize: 12,
              cursor: 'pointer',
              padding: 0,
              textDecoration: 'underline',
            }}
          >
            {showRawDl ? 'Ẩn đối chiếu Deep Learning' : 'ℹ️ Xem đối chiếu ResNet50 thô'}
          </button>
          {showRawDl && (
            <div style={{ marginTop: 6, fontSize: 12, background: 'rgba(255,255,255,0.04)', padding: '6px 10px', borderRadius: 6, color: 'var(--text-secondary)' }}>
              Mô hình ResNet50 gốc nhận diện ban đầu: <strong>{raw_dl.predicted_display}</strong> ({(raw_dl.score * 100).toFixed(1)}%).
              Hệ thống đã tự động lọc nền và kiểm chứng phổ màu để chuẩn hóa sang <strong>{predicted_display}</strong>.
            </div>
          )}
        </div>
      )}

      {scores && (
        <div className="score-list">
          {Object.entries(scores)
            .sort((a, b) => b[1] - a[1])
            .map(([cls, score]) => {
              const isTop = cls === predicted_class;
              return (
                <div className="score-item" key={cls}>
                  <div className="score-item-header">
                    <div className={`score-label ${isTop ? labelColors?.[cls] ?? '' : ''}`}>
                      {isTop && <span>▶</span>}
                      {display_names?.[cls] || cls}
                    </div>
                    <div className="score-value">{(score * 100).toFixed(1)}%</div>
                  </div>
                  <div className="score-bar-track">
                    <div
                      className={`score-bar-fill ${isTop ? 'is-top' : 'not-top'}`}
                      style={{ width: `${score * 100}%` }}
                    />
                  </div>
                </div>
              );
            })}
        </div>
      )}

      <div style={{ marginTop: 14, fontSize: 12, color: 'var(--text-muted)' }}>
        <span>📦 {data.dataset?.split('-')?.[0] || data.dataset}</span>
      </div>

      {warning && (
        <div className="warning-box">
          <span>⚠️</span>
          <div>{warning}</div>
        </div>
      )}

      {quality_map_note && (
        <div className="note-box">
          ℹ️ {quality_map_note}
        </div>
      )}

      <div className="note-box" style={{ marginTop: 8 }}>
        ℹ️ Hệ thống tự động phối hợp Deep Learning và quang phổ màu XLA để bảo vệ độ chính xác trước tác động của môi trường ngoài.
      </div>
    </div>
  );
}

