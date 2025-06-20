export interface Error {
  category: string;
  location: string;
  message: string;
  suggestion: string;
}

export interface AnalysisResponse {
  errors: Error[];
  summary: string;
} 