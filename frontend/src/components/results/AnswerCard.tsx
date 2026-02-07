import React from 'react';
import { Clock, Globe, FileText, GitMerge, Lock } from 'lucide-react';
import type { Answer, QueryMode } from '../../types';
import { ConfidenceIndicator } from './ConfidenceIndicator';

interface AnswerCardProps {
  answer: Answer;
}

const modeIcons: Record<QueryMode, React.ReactNode> = {
  web: <Globe className="w-3 h-3" />,
  pdf: <FileText className="w-3 h-3" />,
  hybrid: <GitMerge className="w-3 h-3" />,
  restricted: <Lock className="w-3 h-3" />,
};

const modeLabels: Record<QueryMode, string> = {
  web: 'Web Search',
  pdf: 'PDF Only',
  hybrid: 'Hybrid',
  restricted: 'Restricted',
};

export const AnswerCard: React.FC<AnswerCardProps> = ({ answer }) => {
  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
    });
  };

  return (
    <div className="card overflow-hidden">
      <div className="border-b border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-900/50">
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
          Question:
        </p>
        <p className="text-lg font-medium text-gray-900 dark:text-white">
          {answer.query}
        </p>
      </div>

      <div className="p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {modeIcons[answer.mode]}
            <span className="text-xs font-medium text-gray-600 dark:text-gray-400 uppercase">
              {modeLabels[answer.mode]}
            </span>
          </div>
          
          <div className="flex items-center gap-4">
            <ConfidenceIndicator confidence={answer.confidence} />
            <div className="flex items-center gap-1 text-xs text-gray-500">
              <Clock className="w-3 h-3" />
              <span>{formatTime(answer.timestamp)}</span>
            </div>
          </div>
        </div>

        <div className="prose prose-gray dark:prose-invert max-w-none">
          <p className="text-gray-800 dark:text-gray-200 leading-relaxed whitespace-pre-wrap">
            {answer.text}
          </p>
        </div>
      </div>
    </div>
  );
};
