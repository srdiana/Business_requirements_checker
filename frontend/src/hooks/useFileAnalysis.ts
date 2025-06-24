import { useState } from 'react';
import { AnalysisResponse } from '../types';
import { api } from '../utils/api';

export function useFileAnalysis() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResponse | null>(null);

  const analyzeFiles = async (template: File, requirements: File) => {
    setIsLoading(true);
    setError(null);
    try {
      const analysisResult = await api.analyzeDocuments(template, requirements);
      setResult(analysisResult);
    } catch (error: any) {
      // Если detail — объект, строка или массив, показываем его, иначе стандартное сообщение
      if (error?.response?.data?.detail) {
        setError(
          typeof error.response.data.detail === 'string'
            ? error.response.data.detail
            : JSON.stringify(error.response.data.detail)
        );
      } else if (error instanceof Error) {
        setError(error.message);
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return {
    isLoading,
    error,
    setError,
    result,
    analyzeFiles,
  };
} 