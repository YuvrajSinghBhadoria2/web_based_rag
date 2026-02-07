import React from 'react';
import { useApp } from '../../context/AppContext';
import { QueryInput } from '../query/QueryInput';
import { ResultsDisplay } from '../results/ResultsDisplay';
import { EmptyState } from '../common/EmptyState';

export const MainContent: React.FC = () => {
  const { state } = useApp();

  return (
    <main className="pt-16 min-h-screen">
      <div className={`flex-1 p-6 ${state.sidebarOpen ? 'ml-80' : 'ml-0'}`}>
        <div className="max-w-4xl mx-auto space-y-6">
          <QueryInput />

          {state.currentAnswer ? (
            <ResultsDisplay answer={state.currentAnswer} />
          ) : (
            <EmptyState />
          )}
        </div>
      </div>
    </main>
  );
};
