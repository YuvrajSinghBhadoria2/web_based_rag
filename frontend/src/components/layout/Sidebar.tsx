import React from 'react';
import { useApp } from '../../context/AppContext';
import { FileUpload } from '../documents/FileUpload';
import { DocumentList } from '../documents/DocumentList';

export const Sidebar: React.FC = () => {
  const { state } = useApp();

  if (!state.sidebarOpen) return null;

  return (
    <aside className="fixed left-0 top-16 bottom-0 w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col z-40">
      <div className="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-thin">
        <FileUpload />
        <DocumentList />
      </div>
    </aside>
  );
};
