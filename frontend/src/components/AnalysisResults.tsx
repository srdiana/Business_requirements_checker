import { AnalysisResponse } from '../types';

interface AnalysisResultsProps {
  result: AnalysisResponse;
}

export function AnalysisResults({ result }: AnalysisResultsProps) {
  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold mb-4">Analysis Results</h2>
      
      <div className="bg-white rounded-lg shadow p-6">
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-gray-700">Summary</h3>
          <p className="text-gray-600">{result.summary}</p>
        </div>

        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-700">Detailed Analysis</h3>
          {result.errors.map((error, index) => {
            // Fallback: если каких-то полей нет, используем пустую строку
            const category = error.category || '';
            const location = error.location || '';
            const message = error.message || '';
            const suggestion = error.suggestion || '';
            const justification = (error as any).justification || '';
            // Особое оформление для ошибок LLM Output
            const isLLMError = category === 'LLM Output';
            return (
              <div
                key={index}
                className={`border-l-4 p-4 rounded ${isLLMError ? 'border-yellow-500 bg-yellow-50' : 'border-red-500 bg-red-50'}`}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <p className={`font-semibold ${isLLMError ? 'text-yellow-700' : 'text-red-700'}`}>{category || 'Error'}</p>
                    {location && <p className="text-sm text-gray-600">Location: {location}</p>}
                  </div>
                </div>
                <p className="mt-2 text-gray-700">{message}</p>
                {suggestion && (
                  <p className="mt-1 text-sm text-blue-600">
                    Suggestion: {suggestion}
                  </p>
                )}
                {justification && (
                  <p className="mt-1 text-xs text-gray-500 italic">
                    Justification: {justification}
                  </p>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
} 