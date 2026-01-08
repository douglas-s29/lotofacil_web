'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Header from '@/components/ui/Header';
import Footer from '@/components/ui/Footer';
import { apiClient, LotteryConfig } from '@/lib/api/client';
import { LOTTERY_CONFIGS } from '@/lib/utils';

export default function Home() {
  const [lotteries, setLotteries] = useState<LotteryConfig[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadLotteries() {
      try {
        const data = await apiClient.getLotteries();
        setLotteries(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Erro ao carregar loterias');
      } finally {
        setLoading(false);
      }
    }

    loadLotteries();
  }, []);

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-purple-600 to-purple-800 text-white">
          <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
            <div className="text-center">
              <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
                Lotofácil Web
              </h1>
              <p className="mt-4 text-xl text-purple-100">
                Análise estatística e geração inteligente de combinações para loterias
              </p>
              <div className="mt-8 flex justify-center gap-4">
                <Link
                  href="/gerador"
                  className="rounded-md bg-white px-6 py-3 text-base font-semibold text-purple-600 shadow-sm hover:bg-purple-50"
                >
                  Gerar Números
                </Link>
                <Link
                  href="/estatisticas"
                  className="rounded-md bg-purple-500 px-6 py-3 text-base font-semibold text-white shadow-sm hover:bg-purple-400"
                >
                  Ver Estatísticas
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Lotteries Section */}
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">
            Selecione uma Loteria
          </h2>

          {loading && (
            <div className="text-center py-12">
              <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-purple-600 border-r-transparent"></div>
              <p className="mt-4 text-gray-600">Carregando loterias...</p>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
              <p className="font-semibold">Erro ao carregar loterias</p>
              <p className="text-sm">{error}</p>
              <p className="text-sm mt-2">
                Certifique-se de que o backend está em execução em {process.env.NEXT_PUBLIC_API_URL}
              </p>
            </div>
          )}

          {!loading && !error && lotteries.length === 0 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 text-yellow-800">
              <p className="font-semibold">Nenhuma loteria configurada</p>
              <p className="text-sm">Execute o script de inicialização do banco de dados.</p>
            </div>
          )}

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {lotteries.map((lottery) => {
              const config = LOTTERY_CONFIGS[lottery.lottery_type as keyof typeof LOTTERY_CONFIGS];
              return (
                <Link
                  key={lottery.id}
                  href={`/gerador?lottery=${lottery.lottery_type}`}
                  className="group relative overflow-hidden rounded-lg bg-white shadow-md transition-all hover:shadow-xl"
                >
                  <div
                    className="h-2"
                    style={{ backgroundColor: lottery.primary_color }}
                  />
                  <div className="p-6">
                    <h3 className="text-xl font-bold text-gray-900 group-hover:text-purple-600">
                      {config?.displayName || lottery.lottery_type}
                    </h3>
                    <p className="mt-2 text-sm text-gray-600">
                      {lottery.description || `${lottery.numbers_to_pick} números de ${lottery.total_numbers}`}
                    </p>
                    <div className="mt-4 flex items-center text-sm text-gray-500">
                      <span className="font-medium">{lottery.total_numbers} números</span>
                      <span className="mx-2">•</span>
                      <span>{lottery.numbers_to_pick} por aposta</span>
                    </div>
                  </div>
                  <div
                    className="absolute bottom-0 left-0 h-1 w-full transform scale-x-0 transition-transform group-hover:scale-x-100"
                    style={{ backgroundColor: lottery.primary_color }}
                  />
                </Link>
              );
            })}
          </div>
        </div>

        {/* Features Section */}
        <div className="bg-gray-100 py-12">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
              Recursos
            </h2>
            <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
              <div className="text-center">
                <div className="mx-auto h-12 w-12 text-purple-600 mb-4">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900">Estatísticas</h3>
                <p className="mt-2 text-sm text-gray-600">
                  Análise completa de frequência e atraso de números
                </p>
              </div>
              <div className="text-center">
                <div className="mx-auto h-12 w-12 text-purple-600 mb-4">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900">Gerador</h3>
                <p className="mt-2 text-sm text-gray-600">
                  Gere combinações inteligentes baseadas em filtros
                </p>
              </div>
              <div className="text-center">
                <div className="mx-auto h-12 w-12 text-purple-600 mb-4">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900">Conferidor</h3>
                <p className="mt-2 text-sm text-gray-600">
                  Verifique seus jogos contra os resultados
                </p>
              </div>
              <div className="text-center">
                <div className="mx-auto h-12 w-12 text-purple-600 mb-4">
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-900">Salvos</h3>
                <p className="mt-2 text-sm text-gray-600">
                  Salve suas combinações favoritas
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
