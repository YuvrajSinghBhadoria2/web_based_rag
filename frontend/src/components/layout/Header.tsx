import React from 'react';
import { 
  Brain, 
  Settings, 
  Menu,
  Sun,
  Moon 
} from 'lucide-react';
import { useApp } from '../../context/AppContext';
import { ModeSelector } from '../query/ModeSelector';

export const Header: React.FC = () => {
  const { state, dispatch, toggleTheme } = useApp();

  return (
    <header className="fixed top-0 left-0 right-0 h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 z-50 flex items-center justify-between px-4">
      <div className="flex items-center gap-4">
        <button 
          onClick={() => dispatch({ type: 'TOGGLE_SIDEBAR' })}
          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg lg:hidden"
        >
          <Menu className="w-5 h-5 text-gray-600 dark:text-gray-300" />
        </button>
        
        <div className="flex items-center gap-2">
          <Brain className="w-8 h-8 text-primary-600" />
          <span className="text-xl font-bold text-gray-900 dark:text-white">
            RAG System
          </span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <ModeSelector />
        
        <button
          onClick={toggleTheme}
          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
        >
          {state.theme === 'light' ? (
            <Moon className="w-5 h-5 text-gray-600" />
          ) : (
            <Sun className="w-5 h-5 text-yellow-500" />
          )}
        </button>

        <button
          onClick={() => dispatch({ type: 'TOGGLE_SETTINGS' })}
          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
        >
          <Settings className="w-5 h-5 text-gray-600 dark:text-gray-300" />
        </button>
      </div>
    </header>
  );
};
