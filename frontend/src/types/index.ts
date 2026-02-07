export type QueryMode = 'web' | 'pdf' | 'hybrid' | 'restricted';

export interface Document {
  id: string;
  filename: string;
  uploadDate: string;
  chunkCount: number;
  status: 'processing' | 'ready' | 'error';
}

export interface Source {
  type: 'pdf' | 'web';
  title: string;
  content: string;
  reference: string;
  score?: number;
}

export interface Answer {
  text: string;
  sources: Source[];
  confidence: number;
  mode: QueryMode;
  timestamp: string;
  query: string;
}

export interface QueryResponse {
  answer: string;
  sources: Source[];
  confidence: number;
  mode_used: QueryMode;
}

export interface UploadResponse {
  document_id: string;
  status: string;
  chunks_created: number;
  filename: string;
}

export interface DocumentsListResponse {
  documents: Document[];
}

export interface AppSettings {
  topK: number;
  chunkSize: number;
  theme: 'light' | 'dark';
}
