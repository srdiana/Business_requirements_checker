import { FileUploader } from './components/FileUploader';
import { AnalysisResults } from './components/AnalysisResults';
import { ErrorAlert } from './components/ErrorAlert';
import { useFileAnalysis } from './hooks/useFileAnalysis';

function App() {
  const { isLoading, error, setError, result, analyzeFiles } = useFileAnalysis();

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-8">
          Business Requirements Checker
        </h1>
        
        {error && <ErrorAlert message={error} onClose={() => setError(null)} />}
        
        <FileUploader onAnalyze={analyzeFiles} isLoading={isLoading} />
        
        {result && <AnalysisResults result={result} />}
      </div>
    </div>
  );
}

export default App; 