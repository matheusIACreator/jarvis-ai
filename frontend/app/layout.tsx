import type { Metadata } from "next"
import "./globals.css"
export const metadata: Metadata = {
  title: "J.A.R.V.I.S. | Interface neural",
  description:
    "Seu assistente pessoal. Voz, conversas e memória em um só lugar.",
}
export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="pt-BR" className="dark">
      <body>{children}</body>
    </html>
  )
}
