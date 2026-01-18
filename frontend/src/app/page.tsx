"use client";

import { useState } from "react";
import { EmailForm } from "@/components/EmailForm";
import { ResultCard } from "@/components/ResultCard";
import { AnalysisResponse } from "@/types";

export default function Home() {
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = (data: AnalysisResponse) => {
    setResult(data);
    setErrorMessage("");
  };

  const handleError = (error: string) => {
    setErrorMessage(error);
  };

  const handleReset = () => {
    setResult(null);
    setErrorMessage("");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-2xl mx-auto px-4 py-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <svg
                className="w-4 h-4 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
            </div>
            <span className="font-semibold text-lg text-gray-900">
              M-AI-l Check
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-2xl mx-auto px-4 py-8">
        {/* Titulo */}
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">
            Classificador de Emails
          </h1>
          <p className="text-gray-600 mt-2">
            Analise emails automaticamente e receba sugestões de resposta com IA.
          </p>
        </div>

        {/* Mensagem de Erro */}
        {errorMessage && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-700">{errorMessage}</p>
          </div>
        )}

        {/* Conteudo */}
        {!result ? (
          <EmailForm
            onSubmit={handleSubmit}
            onError={handleError}
            isLoading={isLoading}
            setIsLoading={setIsLoading}
          />
        ) : (
          <ResultCard result={result} onReset={handleReset} />
        )}

        {/* Footer */}
        <div className="text-center mt-8 text-xs text-gray-400">
          <p>Formatos aceitos: .txt e .pdf (máx. 5MB) ou texto direto.</p>
          <p className="mt-1">Powered by Gemini AI</p>
        </div>
      </main>
    </div>
  );
}
