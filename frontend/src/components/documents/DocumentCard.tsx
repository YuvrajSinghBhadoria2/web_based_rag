import React from 'react';
import { FileText, Trash2, CheckCircle, AlertCircle } from 'lucide-react';
import type { Document } from '../../types';
import { useApp } from '../../context/AppContext';

interface DocumentCardProps {
  document: Document;
}

export const DocumentCard: React.FC<DocumentCardProps> = ({ document }) => {
  const { state, dispatch, handleDeleteDocument } = useApp();
  const isSelected = state.selectedDocuments.includes(document.id);

  const handleToggle = () => {
    dispatch({ type: 'TOGGLE_DOCUMENT_SELECTION', payload: document.id });
  };

  const handleDelete = async (e: React.MouseEvent) => {
    e.stopPropagation();
    await handleDeleteDocument(document.id);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <div
      onClick={handleToggle}
      className={`
        p-3 rounded-lg border cursor-pointer transition-all duration-200
        ${isSelected 
          ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' 
          : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'
        }
      `}
    >
      <div className="flex items-start gap-3">
        <div className={`
          w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0
          ${isSelected 
            ? 'bg-primary-100 dark:bg-primary-900/40' 
            : 'bg-gray-100 dark:bg-gray-700'
          }
        `}>
          {isSelected ? (
            <CheckCircle className="w-5 h-5 text-primary-600 dark:text-primary-400" />
          ) : (
            <FileText className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          )}
        </div>

        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
            {document.filename}
          </p>
          <div className="flex items-center gap-2 mt-1">
            <span className="text-xs text-gray-500 dark:text-gray-500">
              {formatDate(document.uploadDate)}
            </span>
            <span className="text-xs px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded">
              {document.chunkCount} chunks
            </span>
          </div>
        </div>

        <button
          onClick={handleDelete}
          className="p-1 hover:bg-red-100 dark:hover:bg-red-900/20 rounded transition-colors"
        >
          <Trash2 className="w-4 h-4 text-gray-400 hover:text-red-500" />
        </button>
      </div>

      {document.status !== 'ready' && (
        <div className="flex items-center gap-1 mt-2 text-xs text-amber-600 dark:text-amber-400">
          {document.status === 'processing' ? (
            <>
              <AlertCircle className="w-3 h-3" />
              <span>Processing...</span>
            </>
          ) : (
            <>
              <AlertCircle className="w-3 h-3" />
              <span>Error processing</span>
            </>
          )}
        </div>
      )}
    </div>
  );
};
