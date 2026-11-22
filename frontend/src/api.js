// API service - giao tiếp với FastAPI backend
const API_BASE = '/api';

/**
 * Kiểm tra trạng thái backend và model
 */
export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

/**
 * Lấy danh sách model
 */
export async function fetchModels() {
  const res = await fetch(`${API_BASE}/models`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

/**
 * Gửi ảnh để phân tích
 * @param {File} file
 * @returns {Promise<object>}
 */
export async function predictImage(file) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

/**
 * Lấy dữ liệu thực nghiệm từ CSV
 */
export async function fetchExperiments() {
  const res = await fetch(`${API_BASE}/experiments`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}
