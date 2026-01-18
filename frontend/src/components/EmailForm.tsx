"use client";

import { useState } from "react";
import { AnalysisResponse } from "@/types";

interface EmailFormProps {
  onSubmit: (result: AnalysisResponse) => void;
  onError: (error: string) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

type TabType = "file" | "text";

export function EmailForm({
  onSubmit,
  onError,
  isLoading,
  setIsLoading,
}: EmailFormProps) {
  const [activeTab, setActiveTab] = useState<TabType>("file");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [text, setText] = useState("");
  const [error, setError] = useState("");

  // Validacao simples
  const validateText = () => {
    if (text.length < 10) {
      setError("O texto deve ter pelo menos 10 caracteres.");
      return false;
    }
    if (text.length > 50000) {
      setError("O texto não pode exceder 50.000 caracteres.");
      return false;
    }
    setError("");
    return true;
  };

  const validateFile = () => {
    if (!selectedFile) {
      setError("Selecione um arquivo.");
      return false;
    }
    const validTypes = ["text/plain", "application/pdf"];
    if (!validTypes.includes(selectedFile.type)) {
      setError("Formato inválido. Use .txt ou .pdf");
      return false;
    }
    if (selectedFile.size > 5 * 1024 * 1024) {
      setError("Arquivo muito grande. Máximo 5MB.");
      return false;
    }
    setError("");
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    // Valida conforme o modo
    if (activeTab === "file" && !validateFile()) return;
    if (activeTab === "text" && !validateText()) return;

    setIsLoading(true);

    try {
      const formData = new FormData();

      if (activeTab === "file" && selectedFile) {
        formData.append("file", selectedFile);
      } else {
        formData.append("text", text);
      }

      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Erro ao analisar.");
      }

      onSubmit(data);
      // Limpa os campos
      setSelectedFile(null);
      setText("");
    } catch (err) {
      onError(err instanceof Error ? err.message : "Erro desconhecido.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    setSelectedFile(file);
    setError("");
  };

  const canSubmit =
    activeTab === "file" ? selectedFile !== null : text.length >= 10;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      {/* Tabs */}
      <div className="flex border-b border-gray-200 mb-6">
        <button
          type="button"
          onClick={() => setActiveTab("file")}
          disabled={isLoading}
          className={`flex-1 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === "file"
              ? "border-blue-500 text-blue-600"
              : "border-transparent text-gray-500 hover:text-gray-700"
          } ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
        >
          Arquivo
        </button>
        <button
          type="button"
          onClick={() => setActiveTab("text")}
          disabled={isLoading}
          className={`flex-1 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === "text"
              ? "border-blue-500 text-blue-600"
              : "border-transparent text-gray-500 hover:text-gray-700"
          } ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
        >
          Texto
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Tab Arquivo */}
        {activeTab === "file" && (
          <div className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors">
              <input
                type="file"
                accept=".txt,.pdf"
                onChange={handleFileChange}
                disabled={isLoading}
                className="hidden"
                id="file-input"
              />
              <label
                htmlFor="file-input"
                className="cursor-pointer block"
              >
                {selectedFile ? (
                  <div>
                    <p className="font-medium text-gray-900">
                      {selectedFile.name}
                    </p>
                    <p className="text-sm text-gray-500 mt-1">
                      {(selectedFile.size / 1024).toFixed(1)} KB
                    </p>
                    <p className="text-xs text-blue-500 mt-2">
                      Clique para trocar
                    </p>
                  </div>
                ) : (
                  <div>
                    <p className="text-gray-600">
                      Clique para selecionar um arquivo
                    </p>
                    <p className="text-sm text-gray-400 mt-1">
                      .txt ou .pdf (máx. 5MB)
                    </p>
                  </div>
                )}
              </label>
            </div>
          </div>
        )}

        {/* Tab Texto */}
        {activeTab === "text" && (
          <div className="space-y-2">
            <textarea
              value={text}
              onChange={(e) => {
                setText(e.target.value);
                setError("");
              }}
              placeholder="Cole o texto do email aqui..."
              disabled={isLoading}
              rows={8}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
            />
            <div className="flex justify-between text-xs text-gray-500">
              <span>Mínimo 10 caracteres</span>
              <span>{text.length.toLocaleString("pt-BR")} / 50.000</span>
            </div>
          </div>
        )}

        {/* Erro */}
        {error && (
          <p className="mt-4 text-sm text-red-600">{error}</p>
        )}

        {/* Botão Submit */}
        <button
          type="submit"
          disabled={!canSubmit || isLoading}
          className="w-full mt-6 py-3 px-4 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? (
            <span className="flex items-center justify-center gap-2">
              <svg
                className="animate-spin h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Analisando...
            </span>
          ) : (
            "Analisar Email"
          )}
        </button>
      </form>
    </div>
  );
}
