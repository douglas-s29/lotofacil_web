'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/ui/Header';
import Footer from '@/components/ui/Footer';
import NumberBall from '@/components/ui/NumberBall';
import Card from '@/components/ui/Card';
import { apiClient, UserCombination } from '@/lib/api/client';
import { LOTTERY_CONFIGS, getSessionKey, formatDate } from '@/lib/utils';

export default function Salvos() {
  const [combinations, setCombinations] = useState<UserCombination[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLottery, setSelectedLottery] = useState<string | undefined>(undefined);

  useEffect(() => {
    loadCombinations();
  }, [selectedLottery]);

  const loadCombinations = async () => {
    setLoading(true);
    setError(null);

    try {
      const sessionKey = getSessionKey();
      const data = await apiClient.getUserCombinations(
        selectedLottery,
        sessionKey
      );
      setCombinations(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar combinações');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Deseja realmente excluir esta combinação?')) {
      return;
    }

    try {
      await apiClient.deleteUserCombination(id);
      setCombinations((prev) => prev.filter((c) => c.id !== id));
    } catch (err) {
      alert('Erro ao excluir combinação');
    }
  };

  const handleToggleFavorite = async (id: number) => {
    try {
      const updated = await apiClient.toggleFavorite(id);
      setCombinations((prev) =>
        prev.map((c) => (c.id === id ? updated : c))
      );
    } catch (err) {
      alert('Erro ao atualizar favorito');
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1 bg-gray-50 py-8">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-3xl font-bold text-gray-900">
              Combinações Salvas
            </h1>

            {/* Filter by Lottery */}
            <select
              value={selectedLottery || ''}
              onChange={(e) => setSelectedLottery(e.target.value || undefined)}
              className="rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
            >
              <option value="">Todas as loterias</option>
              {Object.entries(LOTTERY_CONFIGS).map(([key, val]) => (
                <option key={key} value={key}>
                  {val.displayName}
                </option>
              ))}
            </select>
          </div>

          {loading && (
            <div className="text-center py-12">
              <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-purple-600 border-r-transparent"></div>
              <p className="mt-4 text-gray-600">Carregando combinações...</p>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800 mb-6">
              <p className="font-semibold">Erro</p>
              <p className="text-sm">{error}</p>
            </div>
          )}

          {!loading && !error && combinations.length === 0 && (
            <div className="bg-white rounded-lg shadow-md p-12 text-center">
              <div className="mx-auto h-16 w-16 text-gray-400 mb-4">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
                  />
                </svg>
              </div>
              <p className="text-gray-600 mb-4">
                Você ainda não tem combinações salvas.
              </p>
              <a
                href="/gerador"
                className="inline-block bg-purple-600 text-white px-6 py-3 rounded-md font-semibold hover:bg-purple-700"
              >
                Gerar Combinações
              </a>
            </div>
          )}

          {!loading && !error && combinations.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {combinations.map((combination) => {
                const lotteryConfig = LOTTERY_CONFIGS[
                  combination.lottery_type as keyof typeof LOTTERY_CONFIGS
                ];
                return (
                  <Card
                    key={combination.id}
                    color={lotteryConfig?.color}
                    className="relative"
                  >
                    {/* Header */}
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h3 className="font-semibold text-gray-900">
                            {combination.name || 'Sem nome'}
                          </h3>
                          {combination.is_favorite && (
                            <span className="text-yellow-500">⭐</span>
                          )}
                        </div>
                        <p className="text-sm text-gray-600">
                          {lotteryConfig?.displayName}
                        </p>
                        <p className="text-xs text-gray-500">
                          {formatDate(combination.created_at)}
                        </p>
                      </div>

                      {/* Actions */}
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleToggleFavorite(combination.id)}
                          className="text-gray-400 hover:text-yellow-500"
                          title="Marcar como favorito"
                        >
                          <svg
                            className="h-5 w-5"
                            fill={combination.is_favorite ? 'currentColor' : 'none'}
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
                            />
                          </svg>
                        </button>
                        <button
                          onClick={() => handleDelete(combination.id)}
                          className="text-gray-400 hover:text-red-500"
                          title="Excluir"
                        >
                          <svg
                            className="h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                            />
                          </svg>
                        </button>
                      </div>
                    </div>

                    {/* Numbers */}
                    <div className="flex flex-wrap gap-2">
                      {combination.numbers.sort((a, b) => a - b).map((num) => (
                        <NumberBall
                          key={num}
                          number={num}
                          color={lotteryConfig?.color}
                          size="sm"
                        />
                      ))}
                    </div>

                    {/* Footer Actions */}
                    <div className="mt-4 pt-4 border-t border-gray-200 flex gap-2">
                      <a
                        href={`/conferidor?lottery=${combination.lottery_type}&numbers=${combination.numbers.join(',')}`}
                        className="flex-1 text-center text-sm text-purple-600 hover:text-purple-800 font-medium"
                      >
                        Conferir
                      </a>
                      <button className="flex-1 text-sm text-purple-600 hover:text-purple-800 font-medium">
                        Copiar
                      </button>
                    </div>
                  </Card>
                );
              })}
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}
