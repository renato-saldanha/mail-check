export interface AnalysisResponse {
  category: "Produtivo" | "Improdutivo";
  confidence: number | null;
  reply: string | null;
  needs_review: boolean;
  extracted_text: string | null;
}
