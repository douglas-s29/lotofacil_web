import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between items-center">
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold text-gray-900">
              🍀 Lotofácil Web
            </Link>
          </div>
          <div className="hidden md:flex md:space-x-8">
            <Link
              href="/"
              className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900 hover:text-gray-600"
            >
              Home
            </Link>
            <Link
              href="/gerador"
              className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
            >
              Gerador
            </Link>
            <Link
              href="/estatisticas"
              className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
            >
              Estatísticas
            </Link>
            <Link
              href="/conferidor"
              className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
            >
              Conferidor
            </Link>
            <Link
              href="/salvos"
              className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
            >
              Salvos
            </Link>
          </div>
        </div>
      </nav>
    </header>
  );
}
