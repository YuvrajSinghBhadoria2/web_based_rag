import React from 'react';
import { FileText, Search } from 'lucide-react';
import { useApp } from '../../context/AppContext';
import { DocumentCard } from './DocumentCard';

export const DocumentList: React.FC = () => {
  const { state } = useApp();

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wide">
          Documents
        </h3>
        <span className="text-xs text-gray-500 dark:text-gray-500">
          {state.documents.length} file{state.documents.length !== 1 ? 's' : ''}
        </span>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          placeholder="Search documents..."
          className="w-full pl-10 pr-4 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
      </div>

      <div className="space-y-2 max-h-96 overflow-y-auto scrollbar-thin">
        {state.documents.length === 0 ? (
          <div className="text-center py-8">
            <FileText className="w-12 h-12 mx-auto text-gray-300 dark:text-gray-600 mb-3" />
            <p className="text-sm text-gray-500 dark:text-gray-500">
              No documents uploaded
            </p>
            <p className="text-xs text-gray-400 dark:text-gray-600 mt-1">
              Upload PDFs to get started
            </p>
          </div>
        ) : (
          state.documents.map(doc => (
            <DocumentCard key={doc.id} document={doc} />
          ))
        )}
      </div>
    </div>
  );
};
