import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();

    // Faz a requisição para o backend
    const response = await fetch(`${BACKEND_URL}/api/feedback`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        { detail: data.detail || "Erro ao enviar feedback." },
        { status: response.status }
      );
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error("Erro no proxy de feedback:", error);
    return NextResponse.json(
      { detail: "Erro de conexão com o servidor." },
      { status: 500 }
    );
  }
}
