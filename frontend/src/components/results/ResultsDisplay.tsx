import React from 'react';
import { AnswerCard } from './AnswerCard';
import { SourcesList } from './SourcesList';
import type { Answer } from '../../types';

interface ResultsDisplayProps {
  answer?: Answer;
}

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ answer }) => {
  if (!answer) return null;

  return (
    <div className="space-y-6 animate-fade-in">
      <AnswerCard answer={answer} />
      <SourcesList sources={answer.sources} />
    </div>
  );
};
