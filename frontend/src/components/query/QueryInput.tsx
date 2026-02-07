import React, { useState, useCallback, useRef, useEffect } from 'react';
import { Send, Sparkles, X } from 'lucide-react';
import { useApp } from '../../context/AppContext';

const sampleQueries = [
  "What is the main topic of my documents?",
  "Summarize the key findings",
  "Extract important dates and events",
];

export const QueryInput: React.FC = () => {
  const { state, handleQuery, dispatch, clearResults } = useApp();
  const [showSamples, setShowSamples] = useState(true);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleQuery();
      }
    },
    [handleQuery]
  );

  const handleSubmit = useCallback(() => {
    handleQuery();
  }, [handleQuery]);

  const autoResize = useCallback(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  }, []);

  useEffect(() => {
    autoResize();
  }, [state.currentQuery, autoResize]);

  const handleClear = () => {
    clearResults();
    setShowSamples(true);
  };

  return (
    <div className="space-y-4">
      <div className="card p-1">
        <div className="flex items-start gap-2">
          <textarea
            ref={textareaRef}
            value={state.currentQuery}
            onChange={e => {
              dispatch({ type: 'SET_CURRENT_QUERY', payload: e.target.value });
              if (e.target.value && showSamples) {
                setShowSamples(false);
              }
            }}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your documents..."
            className="flex-1 min-h-[120px] max-h-[200px] p-4 bg-transparent text-gray-900 dark:text-white placeholder-gray-500 resize-none focus:outline-none"
            disabled={state.isLoading}
          />

          {state.currentQuery && (
            <button
              onClick={handleClear}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors mt-1"
            >
              <X className="w-4 h-4 text-gray-400" />
            </button>
          )}
        </div>

        <div className="flex items-center justify-between px-4 pb-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-gray-400" />
            <span className="text-xs text-gray-500 dark:text-gray-500">
              Press Enter to submit, Shift+Enter for new line
            </span>
          </div>

          <button
            onClick={handleSubmit}
            disabled={!state.currentQuery.trim() || state.isLoading}
            className="btn-primary flex items-center gap-2"
          >
            {state.isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Submit</span>
              </>
            )}
          </button>
        </div>
      </div>

      {showSamples && !state.currentQuery && (
        <div className="flex flex-wrap gap-2">
          <span className="text-xs text-gray-500 dark:text-gray-500 py-1">
            Try:
          </span>
          {sampleQueries.map((query, index) => (
            <button
              key={index}
              onClick={() => {
                dispatch({ type: 'SET_CURRENT_QUERY', payload: query });
                setShowSamples(false);
              }}
              className="text-xs px-3 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            >
              {query}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
