import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

// IP do visitante, repassado ao backend para o limite de uso
function getClientIp(request: NextRequest) {
  const forwarded = request.headers.get("x-forwarded-for") || "";
  return forwarded.split(",")[0].trim() || request.headers.get("x-real-ip") || "";
}

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();

    // Faz a requisição para o backend
    const response = await fetch(`${BACKEND_URL}/api/feedback`, {
      method: "POST",
      headers: { "x-client-ip": getClientIp(request) },
      body: formData,
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      return NextResponse.json(
        {
          detail:
            typeof data.detail === "string"
              ? data.detail
              : "Erro ao enviar feedback.",
        },
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
