import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, Loader2 } from 'lucide-react';
import { useApp } from '../../context/AppContext';

export const FileUpload: React.FC = () => {
  const { state, handleUpload } = useApp();

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      const pdfFile = acceptedFiles.find(file => file.type === 'application/pdf');
      if (pdfFile) {
        handleUpload(pdfFile);
      }
    },
    [handleUpload]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
  });

  return (
    <div className="space-y-4">
      <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wide">
        Upload Documents
      </h3>
      
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all duration-200
          ${isDragActive 
            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' 
            : 'border-gray-300 dark:border-gray-600 hover:border-primary-400 hover:bg-gray-50 dark:hover:bg-gray-700/50'
          }
        `}
      >
        <input {...getInputProps()} />
        
        {state.isUploading ? (
          <div className="flex flex-col items-center gap-2">
            <Loader2 className="w-10 h-10 text-primary-500 animate-spin" />
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Processing... {state.uploadProgress}%
            </p>
            <div className="w-full max-w-xs bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                className="bg-primary-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${state.uploadProgress}%` }}
              />
            </div>
          </div>
        ) : isDragActive ? (
          <div className="flex flex-col items-center gap-2">
            <FileText className="w-10 h-10 text-primary-500" />
            <p className="text-sm font-medium text-primary-600 dark:text-primary-400">
              Drop your PDF here
            </p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-2">
            <Upload className="w-10 h-10 text-gray-400" />
            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Drag & drop a PDF
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-500">
              or click to browse
            </p>
          </div>
        )}
      </div>

      <p className="text-xs text-gray-500 dark:text-gray-500 text-center">
        Supports PDF files up to 10MB
      </p>
    </div>
  );
};
