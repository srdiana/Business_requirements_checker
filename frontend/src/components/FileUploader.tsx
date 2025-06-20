import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { ArrowPathIcon } from '@heroicons/react/24/outline';

interface FileUploaderProps {
  onAnalyze: (template: File, requirements: File) => void;
  isLoading: boolean;
}

export function FileUploader({ onAnalyze, isLoading }: FileUploaderProps) {
  const [template, setTemplate] = useState<File | null>(null);
  const [requirements, setRequirements] = useState<File | null>(null);

  const onTemplateDrop = useCallback((acceptedFiles: File[]) => {
    setTemplate(acceptedFiles[0]);
  }, []);

  const onRequirementsDrop = useCallback((acceptedFiles: File[]) => {
    setRequirements(acceptedFiles[0]);
  }, []);

  const { getRootProps: getTemplateRootProps, getInputProps: getTemplateInputProps } = useDropzone({
    onDrop: onTemplateDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxFiles: 1
  });

  const { getRootProps: getRequirementsRootProps, getInputProps: getRequirementsInputProps } = useDropzone({
    onDrop: onRequirementsDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxFiles: 1
  });

  const handleAnalyze = () => {
    if (template && requirements) {
      onAnalyze(template, requirements);
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h2 className="text-xl font-semibold mb-4">Template Document</h2>
          <div
            {...getTemplateRootProps()}
            className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-500"
          >
            <input {...getTemplateInputProps()} />
            {template ? (
              <p className="text-green-600">{template.name}</p>
            ) : (
              <p>Drag & drop a template file here, or click to select</p>
            )}
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4">Requirements Document</h2>
          <div
            {...getRequirementsRootProps()}
            className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-500"
          >
            <input {...getRequirementsInputProps()} />
            {requirements ? (
              <p className="text-green-600">{requirements.name}</p>
            ) : (
              <p>Drag & drop a requirements file here, or click to select</p>
            )}
          </div>
        </div>
      </div>

      <button
        onClick={handleAnalyze}
        disabled={!template || !requirements || isLoading}
        className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {isLoading ? (
          <>
            <ArrowPathIcon className="animate-spin -ml-1 mr-3 h-5 w-5" />
            Analyzing...
          </>
        ) : (
          'Analyze Documents'
        )}
      </button>
    </div>
  );
} 