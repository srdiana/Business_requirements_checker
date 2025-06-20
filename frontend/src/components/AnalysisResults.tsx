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
          {result.errors.map((error, index) => (
            <div
              key={index}
              className="border-l-4 border-red-500 bg-red-50 p-4 rounded"
            >
              <div className="flex justify-between items-start">
                <div>
                  <p className="font-semibold text-red-700">{error.category}</p>
                  <p className="text-sm text-gray-600">Location: {error.location}</p>
                </div>
              </div>
              <p className="mt-2 text-gray-700">{error.message}</p>
              <p className="mt-1 text-sm text-blue-600">
                Suggestion: {error.suggestion}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} 