"use client";

import { useState } from "react";
import { AnalysisResponse } from "@/types";

interface ResultCardProps {
  result: AnalysisResponse;
  onReset: () => void;
}

export function ResultCard({ result, onReset }: ResultCardProps) {
  const [copied, setCopied] = useState(false);

  const isProdutivo = result.category === "Produtivo";
  const confidencePercent = result.confidence
    ? Math.round(result.confidence * 100)
    : null;

  const handleCopy = async () => {
    if (!result.reply) return;

    try {
      await navigator.clipboard.writeText(result.reply);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      console.error("Falha ao copiar");
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {/* Icone */}
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center ${
                isProdutivo ? "bg-green-100" : "bg-yellow-100"
              }`}
            >
              {isProdutivo ? (
                <svg
                  className="w-5 h-5 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              ) : (
                <svg
                  className="w-5 h-5 text-yellow-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M20 12H4"
                  />
                </svg>
              )}
            </div>

            <div>
              <h3 className="font-semibold text-gray-900">
                Resultado da Análise
              </h3>
              <p className="text-sm text-gray-500">
                Email classificado com sucesso
              </p>
            </div>
          </div>

          {/* Badge */}
          <span
            className={`px-3 py-1 rounded-full text-sm font-medium ${
              isProdutivo
                ? "bg-green-100 text-green-700"
                : "bg-yellow-100 text-yellow-700"
            }`}
          >
            {result.category}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-6 space-y-4">
        {/* Barra de Confiança */}
        {confidencePercent !== null && (
          <div>
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-500">Confiança</span>
              <span className="font-medium">{confidencePercent}%</span>
            </div>
            <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full transition-all ${
                  isProdutivo ? "bg-green-500" : "bg-yellow-500"
                }`}
                style={{ width: `${confidencePercent}%` }}
              />
            </div>
          </div>
        )}

        {/* Resposta Sugerida */}
        {result.reply && (
          <div>
            <h4 className="text-sm font-medium text-gray-500 mb-2">
              Resposta Sugerida
            </h4>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
                {result.reply}
              </p>
            </div>
          </div>
        )}

        {/* Aviso de Revisão */}
        {result.needs_review && (
          <div className="flex items-start gap-3 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <svg
              className="w-5 h-5 text-yellow-600 shrink-0 mt-0.5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            <div>
              <p className="text-sm font-medium text-yellow-800">
                Requer Revisão Manual
              </p>
              <p className="text-xs text-yellow-600 mt-0.5">
                A classificação pode ser ambígua. Verifique antes de usar.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Footer - Botões */}
      <div className="p-6 border-t border-gray-100 flex flex-col sm:flex-row gap-3">
        <button
          onClick={handleCopy}
          disabled={!result.reply || copied}
          className="flex-1 py-2.5 px-4 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {copied ? "Copiado!" : "Copiar Resposta"}
        </button>

        <button
          onClick={onReset}
          className="flex-1 py-2.5 px-4 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
        >
          Nova Análise
        </button>
      </div>
    </div>
  );
}
