import React from 'react';
import { X, Sliders, Moon, Sun, Trash2, ExternalLink } from 'lucide-react';
import { useApp } from '../../context/AppContext';

export const SettingsModal: React.FC = () => {
  const { state, dispatch, toggleTheme } = useApp();

  if (!state.settingsOpen) return null;

  const handleClose = () => {
    dispatch({ type: 'TOGGLE_SETTINGS' });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div 
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={handleClose}
      />
      
      <div className="relative bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-md mx-4 animate-slide-up">
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-2">
            <Sliders className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              Settings
            </h2>
          </div>
          <button
            onClick={handleClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        <div className="p-4 space-y-6">
          <div className="space-y-4">
            <h3 className="text-sm font-medium text-gray-900 dark:text-white uppercase tracking-wide">
              Appearance
            </h3>
            
            <button
              onClick={toggleTheme}
              className="w-full flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
            >
              <div className="flex items-center gap-3">
                {state.theme === 'light' ? (
                  <Sun className="w-5 h-5 text-amber-500" />
                ) : (
                  <Moon className="w-5 h-5 text-blue-500" />
                )}
                <span className="text-sm font-medium text-gray-900 dark:text-white">
                  {state.theme === 'light' ? 'Light Mode' : 'Dark Mode'}
                </span>
              </div>
              <span className="text-xs text-gray-500">
                Toggle theme
              </span>
            </button>
          </div>

          <div className="space-y-4">
            <h3 className="text-sm font-medium text-gray-900 dark:text-white uppercase tracking-wide">
              API Configuration
            </h3>
            
            <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <p className="text-xs text-blue-700 dark:text-blue-400">
                API endpoints are configured via environment variables.
                See the backend .env file for configuration.
              </p>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-sm font-medium text-gray-900 dark:text-white uppercase tracking-wide">
              Data Management
            </h3>
            
            <button
              className="w-full flex items-center justify-between p-3 bg-red-50 dark:bg-red-900/20 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors"
              onClick={() => {
                if (confirm('Are you sure you want to clear all documents?')) {
                  // Implementation would go here
                }
              }}
            >
              <div className="flex items-center gap-3">
                <Trash2 className="w-5 h-5 text-red-500" />
                <span className="text-sm font-medium text-red-700 dark:text-red-400">
                  Clear All Documents
                </span>
              </div>
            </button>
          </div>
        </div>

        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>RAG System v1.0.0</span>
            <a 
              href="https://github.com/your-repo/rag-system"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 hover:text-primary-600 transition-colors"
            >
              <ExternalLink className="w-3 h-3" />
              <span>View on GitHub</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};
