import React, { createContext, useContext, useReducer, useCallback, useEffect } from 'react';
import type { 
  Document, 
  Answer, 
  QueryMode
} from '../types';
import { 
  uploadDocument, 
  getDocuments, 
  deleteDocument,
  querySystem
} from '../services/api';
import toast from 'react-hot-toast';

interface AppState {
  documents: Document[];
  selectedDocuments: string[];
  currentQuery: string;
  queryMode: QueryMode;
  isLoading: boolean;
  isUploading: boolean;
  uploadProgress: number;
  currentAnswer: Answer | null;
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  settingsOpen: boolean;
}

type Action =
  | { type: 'SET_DOCUMENTS'; payload: Document[] }
  | { type: 'ADD_DOCUMENT'; payload: Document }
  | { type: 'REMOVE_DOCUMENT'; payload: string }
  | { type: 'SET_SELECTED_DOCUMENTS'; payload: string[] }
  | { type: 'TOGGLE_DOCUMENT_SELECTION'; payload: string }
  | { type: 'SET_CURRENT_QUERY'; payload: string }
  | { type: 'SET_QUERY_MODE'; payload: QueryMode }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_UPLOADING'; payload: boolean }
  | { type: 'SET_UPLOAD_PROGRESS'; payload: number }
  | { type: 'SET_CURRENT_ANSWER'; payload: Answer | null }
  | { type: 'TOGGLE_SIDEBAR' }
  | { type: 'SET_THEME'; payload: 'light' | 'dark' }
  | { type: 'TOGGLE_SETTINGS' }
  | { type: 'CLEAR_RESULTS' };

const initialState: AppState = {
  documents: [],
  selectedDocuments: [],
  currentQuery: '',
  queryMode: 'hybrid',
  isLoading: false,
  isUploading: false,
  uploadProgress: 0,
  currentAnswer: null,
  sidebarOpen: true,
  theme: 'light',
  settingsOpen: false,
};

function appReducer(state: AppState, action: Action): AppState {
  switch (action.type) {
    case 'SET_DOCUMENTS':
      return { ...state, documents: action.payload };
    case 'ADD_DOCUMENT':
      return { ...state, documents: [action.payload, ...state.documents] };
    case 'REMOVE_DOCUMENT':
      return {
        ...state,
        documents: state.documents.filter(doc => doc.id !== action.payload),
        selectedDocuments: state.selectedDocuments.filter(id => id !== action.payload),
      };
    case 'SET_SELECTED_DOCUMENTS':
      return { ...state, selectedDocuments: action.payload };
    case 'TOGGLE_DOCUMENT_SELECTION':
      return {
        ...state,
        selectedDocuments: state.selectedDocuments.includes(action.payload)
          ? state.selectedDocuments.filter(id => id !== action.payload)
          : [...state.selectedDocuments, action.payload],
      };
    case 'SET_CURRENT_QUERY':
      return { ...state, currentQuery: action.payload };
    case 'SET_QUERY_MODE':
      return { ...state, queryMode: action.payload };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_UPLOADING':
      return { ...state, isUploading: action.payload };
    case 'SET_UPLOAD_PROGRESS':
      return { ...state, uploadProgress: action.payload };
    case 'SET_CURRENT_ANSWER':
      return { ...state, currentAnswer: action.payload };
    case 'TOGGLE_SIDEBAR':
      return { ...state, sidebarOpen: !state.sidebarOpen };
    case 'SET_THEME':
      return { ...state, theme: action.payload };
    case 'TOGGLE_SETTINGS':
      return { ...state, settingsOpen: !state.settingsOpen };
    case 'CLEAR_RESULTS':
      return { ...state, currentAnswer: null };
    default:
      return state;
  }
}

interface AppContextType {
  state: AppState;
  dispatch: React.Dispatch<Action>;
  handleUpload: (file: File) => Promise<void>;
  handleDeleteDocument: (documentId: string) => Promise<void>;
  handleQuery: () => Promise<void>;
  clearResults: () => void;
  toggleTheme: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null;
    if (savedTheme) {
      dispatch({ type: 'SET_THEME', payload: savedTheme });
      document.documentElement.classList.toggle('dark', savedTheme === 'dark');
    }

    loadDocuments();
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', state.theme === 'dark');
    localStorage.setItem('theme', state.theme);
  }, [state.theme]);

  const loadDocuments = useCallback(async () => {
    try {
      const response = await getDocuments();
      dispatch({ type: 'SET_DOCUMENTS', payload: response.documents });
    } catch (error) {
      console.error('Failed to load documents:', error);
    }
  }, []);

  const handleUpload = useCallback(async (file: File) => {
    dispatch({ type: 'SET_UPLOADING', payload: true });
    dispatch({ type: 'SET_UPLOAD_PROGRESS', payload: 0 });

    try {
      const response = await uploadDocument(file);
      
      dispatch({ type: 'SET_UPLOAD_PROGRESS', payload: 100 });
      
      const newDoc: Document = {
        id: response.document_id,
        filename: response.filename || file.name,
        uploadDate: new Date().toISOString(),
        chunkCount: response.chunks_created,
        status: 'ready',
      };

      dispatch({ type: 'ADD_DOCUMENT', payload: newDoc });
      toast.success(`Uploaded: ${file.name}`);
    } catch (error) {
      toast.error('Failed to upload file');
      console.error('Upload error:', error);
    } finally {
      dispatch({ type: 'SET_UPLOADING', payload: false });
      dispatch({ type: 'SET_UPLOAD_PROGRESS', payload: 0 });
    }
  }, []);

  const handleDeleteDocument = useCallback(async (documentId: string) => {
    try {
      await deleteDocument(documentId);
      dispatch({ type: 'REMOVE_DOCUMENT', payload: documentId });
      toast.success('Document deleted');
    } catch (error) {
      toast.error('Failed to delete document');
      console.error('Delete error:', error);
    }
  }, []);

  const handleQuery = useCallback(async () => {
    if (!state.currentQuery.trim()) {
      toast.error('Please enter a query');
      return;
    }

    dispatch({ type: 'SET_LOADING', payload: true });
    dispatch({ type: 'CLEAR_RESULTS' });

    try {
      const response = await querySystem(
        state.currentQuery, 
        state.queryMode,
        state.selectedDocuments.length > 0 ? state.selectedDocuments : undefined
      );

      const answer: Answer = {
        text: response.answer,
        sources: response.sources,
        confidence: response.confidence,
        mode: response.mode_used,
        timestamp: new Date().toISOString(),
        query: state.currentQuery,
      };

      dispatch({ type: 'SET_CURRENT_ANSWER', payload: answer });
    } catch (error) {
      toast.error('Failed to get answer');
      console.error('Query error:', error);
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, [state.currentQuery, state.queryMode, state.selectedDocuments]);

  const clearResults = useCallback(() => {
    dispatch({ type: 'CLEAR_RESULTS' });
    dispatch({ type: 'SET_CURRENT_QUERY', payload: '' });
  }, []);

  const toggleTheme = useCallback(() => {
    dispatch({ type: 'SET_THEME', payload: state.theme === 'light' ? 'dark' : 'light' });
  }, [state.theme]);

  return (
    <AppContext.Provider 
      value={{
        state,
        dispatch,
        handleUpload,
        handleDeleteDocument,
        handleQuery,
        clearResults,
        toggleTheme,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
}
