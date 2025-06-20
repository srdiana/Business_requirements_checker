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
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An unexpected error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return {
    isLoading,
    error,
    result,
    analyzeFiles,
  };
} 