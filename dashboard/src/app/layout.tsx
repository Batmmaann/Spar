import './globals.css'

export const metadata = {
  title: 'SPAR',
  description: 'Upload match videos, analyze players, and view stats',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gradient-to-br from-gray-900 to-black text-white min-h-screen">
        {/* Header remains sticky and spans full width */}
        <header className="sticky top-0 z-50 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 shadow-lg w-full">
          <nav className="flex items-center justify-between px-6 py-4">
            <h1 className="text-3xl font-extrabold">SPAR</h1>
            <ul className="flex gap-6">
              <li><a href="/" className="hover:text-yellow-300 transition-colors">Home</a></li>
              <li><a href="/overview" className="hover:text-yellow-300 transition-colors">Overview</a></li>
              <li><a href="/players" className="hover:text-yellow-300 transition-colors">Players</a></li>
            </ul>
          </nav>
        </header>

        {/* Main content takes full width so the table can expand fully */}
        <main className="w-full px-6 py-10">
          {children}
        </main>

        <footer className="text-center text-gray-500 text-sm py-6 w-full">
          © 2025 SPAR
        </footer>
      </body>
    </html>
  )
}
