import React, { useState } from 'react';
import { Globe, FileText, Copy, Check, ExternalLink } from 'lucide-react';
import type { Source } from '../../types';

interface SourceCardProps {
  source: Source;
}

export const SourceCard: React.FC<SourceCardProps> = ({ source }) => {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(source.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getIcon = () => {
    return source.type === 'web' ? (
      <Globe className="w-4 h-4 text-blue-500" />
    ) : (
      <FileText className="w-4 h-4 text-amber-500" />
    );
  };

  const getTypeLabel = () => {
    return source.type === 'web' ? 'Web' : 'Document';
  };

  const formatReference = (ref: string) => {
    if (ref.startsWith('http')) {
      try {
        const url = new URL(ref);
        return url.hostname + url.pathname;
      } catch {
        return ref;
      }
    }
    return ref;
  };

  return (
    <div className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
      <div 
        onClick={() => setExpanded(!expanded)}
        className="p-3 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
      >
        <div className="flex items-start gap-2">
          {getIcon()}
          
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <span className="text-xs font-medium text-gray-700 dark:text-gray-300 truncate">
                {source.title}
              </span>
              <span className="text-xs px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded">
                {getTypeLabel()}
              </span>
            </div>
            
            <p className="text-xs text-gray-500 dark:text-gray-500 mt-1 truncate">
              {formatReference(source.reference)}
            </p>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={handleCopy}
              className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded transition-colors"
              title="Copy content"
            >
              {copied ? (
                <Check className="w-3 h-3 text-green-500" />
              ) : (
                <Copy className="w-3 h-3 text-gray-400" />
              )}
            </button>

            {source.reference.startsWith('http') && (
              <a
                href={source.reference}
                target="_blank"
                rel="noopener noreferrer"
                onClick={e => e.stopPropagation()}
                className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded transition-colors"
                title="Open source"
              >
                <ExternalLink className="w-3 h-3 text-gray-400" />
              </a>
            )}
          </div>
        </div>
      </div>

      {expanded && (
        <div className="px-3 pb-3">
          <div className="pl-6 border-l-2 border-gray-200 dark:border-gray-700">
            <p className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
              {source.content}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
