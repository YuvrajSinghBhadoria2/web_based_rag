import React from 'react';
import { Globe, FileText, GitMerge, Lock } from 'lucide-react';
import { useApp } from '../../context/AppContext';
import type { QueryMode } from '../../types';

const modes: { id: QueryMode; label: string; icon: React.ReactNode; description: string }[] = [
  {
    id: 'web',
    label: 'Web Search',
    icon: <Globe className="w-4 h-4" />,
    description: 'Search the web for information',
  },
  {
    id: 'pdf',
    label: 'PDF Only',
    icon: <FileText className="w-4 h-4" />,
    description: 'Query only uploaded documents',
  },
  {
    id: 'hybrid',
    label: 'Hybrid',
    icon: <GitMerge className="w-4 h-4" />,
    description: 'Combine web and document search',
  },
  {
    id: 'restricted',
    label: 'Restricted',
    icon: <Lock className="w-4 h-4" />,
    description: 'Safe mode with content filtering',
  },
];

export const ModeSelector: React.FC = () => {
  const { state, dispatch } = useApp();

  return (
    <div className="flex items-center gap-1 bg-gray-100 dark:bg-gray-800 p-1 rounded-lg">
      {modes.map(mode => (
        <button
          key={mode.id}
          onClick={() => dispatch({ type: 'SET_QUERY_MODE', payload: mode.id })}
          className={`
            mode-tab ${state.queryMode === mode.id ? 'mode-tab-active' : 'mode-tab-inactive'}
          `}
          title={mode.description}
        >
          {mode.icon}
          <span className="hidden sm:inline text-sm">{mode.label}</span>
        </button>
      ))}
    </div>
  );
};
