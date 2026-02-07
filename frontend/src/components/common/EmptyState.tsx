import React from 'react';
import { 
  Brain, 
  FileText, 
  Search, 
  MessageCircle,
  ArrowRight 
} from 'lucide-react';

export const EmptyState: React.FC = () => {
  const features = [
    {
      icon: <FileText className="w-5 h-5" />,
      title: 'Upload Documents',
      description: 'Drag and drop PDF files to add them to your knowledge base',
    },
    {
      icon: <Search className="w-5 h-5" />,
      title: 'Smart Search',
      description: 'Ask questions and get answers from your documents and the web',
    },
    {
      icon: <Brain className="w-5 h-5" />,
      title: 'AI Powered',
      description: 'Powered by Groq LLM for fast, accurate responses',
    },
    {
      icon: <MessageCircle className="w-5 h-5" />,
      title: 'Source Citations',
      description: 'Every answer includes sources so you can verify the information',
    },
  ];

  return (
    <div className="text-center py-16">
      <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-primary-100 dark:bg-primary-900/30 mb-6">
        <Brain className="w-10 h-10 text-primary-600 dark:text-primary-400" />
      </div>

      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        Welcome to RAG System
      </h2>
      
      <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-md mx-auto">
        Upload documents and ask questions to get AI-powered answers with source citations.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
        {features.map((feature, index) => (
          <div 
            key={index}
            className="flex items-start gap-3 p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 text-left"
          >
            <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
              <div className="text-primary-600 dark:text-primary-400">
                {feature.icon}
              </div>
            </div>
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white">
                {feature.title}
              </h3>
              <p className="text-sm text-gray-500 dark:text-gray-500 mt-1">
                {feature.description}
              </p>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 flex items-center justify-center gap-2 text-sm text-gray-500">
        <span>Start by uploading a document</span>
        <ArrowRight className="w-4 h-4" />
      </div>
    </div>
  );
};
