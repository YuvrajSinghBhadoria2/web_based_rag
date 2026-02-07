import axios from 'axios';
import type { 
  QueryResponse, 
  UploadResponse, 
  DocumentsListResponse,
  QueryMode 
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  maxRedirects: 5,
});

export const uploadDocument = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post<UploadResponse>('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const querySystem = async (
  query: string, 
  mode: QueryMode,
  documentIds?: string[]
): Promise<QueryResponse> => {
  const response = await api.post<QueryResponse>('/query/', {
    query,
    mode,
    document_ids: documentIds,
  });

  return response.data;
};

export const getDocuments = async (): Promise<DocumentsListResponse> => {
  const response = await api.get<DocumentsListResponse>('/documents/');
  return response.data;
};

export const deleteDocument = async (documentId: string): Promise<void> => {
  await api.delete(`/documents/${documentId}/`);
};

export const healthCheck = async (): Promise<{ status: string }> => {
  const response = await api.get('/health/');
  return response.data;
};

export default api;
