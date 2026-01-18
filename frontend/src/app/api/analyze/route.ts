import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get("file");
    const text = formData.get("text");

    // Determina qual endpoint usar baseado no que foi enviado
    let endpoint = "";
    const backendFormData = new FormData();

    if (file && file instanceof File) {
      endpoint = "/api/analyze/file";
      backendFormData.append("file", file);
    } else if (text && typeof text === "string") {
      endpoint = "/api/analyze/text";
      backendFormData.append("text", text);
    } else {
      return NextResponse.json(
        { detail: "Envie um arquivo ou texto para análise." },
        { status: 400 }
      );
    }

    // Faz a requisição para o backend
    const response = await fetch(`${BACKEND_URL}${endpoint}`, {
      method: "POST",
      body: backendFormData,
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        { detail: data.detail || "Erro ao processar." },
        { status: response.status }
      );
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error("Erro no proxy:", error);
    return NextResponse.json(
      { detail: "Erro de conexão com o servidor. Tente novamente." },
      { status: 500 }
    );
  }
}
