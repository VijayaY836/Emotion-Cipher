import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'EMOTION CIPHER',
  description: 'Encrypt your messages with emotions. Decrypt with feelings.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
