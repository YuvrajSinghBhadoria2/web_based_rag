import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Globe, FileText } from 'lucide-react';
import { SourceCard } from './SourceCard';
import type { Source } from '../../types';

interface SourcesListProps {
  sources: Source[];
}

export const SourcesList: React.FC<SourcesListProps> = ({ sources }) => {
  const [expanded, setExpanded] = useState(true);

  if (sources.length === 0) return null;

  const pdfSources = sources.filter(s => s.type === 'pdf');
  const webSources = sources.filter(s => s.type === 'web');

  return (
    <div className="card overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-4 py-3 flex items-center justify-between bg-gray-50 dark:bg-gray-900/50 hover:bg-gray-100 dark:hover:bg-gray-900/70 transition-colors"
      >
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-gray-900 dark:text-white">
            Sources
          </span>
          <span className="text-xs text-gray-500 dark:text-gray-500">
            ({sources.length} {sources.length === 1 ? 'source' : 'sources'})
          </span>
        </div>

        {expanded ? (
          <ChevronUp className="w-4 h-4 text-gray-500" />
        ) : (
          <ChevronDown className="w-4 h-4 text-gray-500" />
        )}
      </button>

      {expanded && (
        <div className="divide-y divide-gray-200 dark:divide-gray-700">
          {pdfSources.length > 0 && (
            <div className="p-4 space-y-2">
              <div className="flex items-center gap-2 text-xs font-medium text-gray-600 dark:text-gray-400 uppercase">
                <FileText className="w-3 h-3" />
                <span>Documents ({pdfSources.length})</span>
              </div>
              {pdfSources.map((source, index) => (
                <SourceCard key={`pdf-${index}`} source={source} />
              ))}
            </div>
          )}

          {webSources.length > 0 && (
            <div className="p-4 space-y-2">
              <div className="flex items-center gap-2 text-xs font-medium text-gray-600 dark:text-gray-400 uppercase">
                <Globe className="w-3 h-3" />
                <span>Web ({webSources.length})</span>
              </div>
              {webSources.map((source, index) => (
                <SourceCard key={`web-${index}`} source={source} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
