import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "M-AI-l Check | Classificador de Emails",
  description:
    "Classifique emails automaticamente como Produtivo ou Improdutivo e receba sugestões de resposta com inteligência artificial.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
        {children}
      </body>
    </html>
  );
}
