'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/ui/Header';
import Footer from '@/components/ui/Footer';
import NumberBall from '@/components/ui/NumberBall';
import Card from '@/components/ui/Card';
import { apiClient, NumberStatistics } from '@/lib/api/client';
import { LOTTERY_CONFIGS } from '@/lib/utils';

export default function Estatisticas() {
  const [lotteryType, setLotteryType] = useState('LOTOFACIL');
  const [allStats, setAllStats] = useState<NumberStatistics[]>([]);
  const [frequent, setFrequent] = useState<NumberStatistics[]>([]);
  const [delayed, setDelayed] = useState<NumberStatistics[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStatistics();
  }, [lotteryType]);

  const loadStatistics = async () => {
    setLoading(true);
    setError(null);

    try {
      const [all, freq, del] = await Promise.all([
        apiClient.getStatistics(lotteryType),
        apiClient.getMostFrequent(lotteryType, 10),
        apiClient.getMostDelayed(lotteryType, 10),
      ]);
      setAllStats(all);
      setFrequent(freq);
      setDelayed(del);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar estatísticas');
    } finally {
      setLoading(false);
    }
  };

  const lotteryConfig = LOTTERY_CONFIGS[lotteryType as keyof typeof LOTTERY_CONFIGS];
  const maxFrequency = Math.max(...allStats.map((s) => s.frequency), 1);

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1 bg-gray-50 py-8">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Estatísticas</h1>

            {/* Lottery Selector */}
            <select
              value={lotteryType}
              onChange={(e) => setLotteryType(e.target.value)}
              className="rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
            >
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
              <p className="mt-4 text-gray-600">Carregando estatísticas...</p>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800 mb-6">
              <p className="font-semibold">Erro</p>
              <p className="text-sm">{error}</p>
            </div>
          )}

          {!loading && !error && (
            <>
              {/* Top Statistics */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                {/* Most Frequent */}
                <Card title="🔥 Mais Frequentes" color={lotteryConfig?.color}>
                  <p className="text-sm text-gray-600 mb-4">
                    Números que mais aparecem nos sorteios
                  </p>
                  <div className="space-y-3">
                    {frequent.map((stat, idx) => (
                      <div
                        key={stat.id}
                        className="flex items-center justify-between bg-gray-50 rounded-lg p-3"
                      >
                        <div className="flex items-center gap-3">
                          <span className="text-sm font-semibold text-gray-500 w-6">
                            #{idx + 1}
                          </span>
                          <NumberBall
                            number={stat.number}
                            color={lotteryConfig?.color}
                            size="sm"
                          />
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-semibold text-gray-900">
                            {stat.frequency} vezes
                          </p>
                          <p className="text-xs text-gray-500">
                            Atraso: {stat.delay}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* Most Delayed */}
                <Card title="⏰ Mais Atrasados" color={lotteryConfig?.color}>
                  <p className="text-sm text-gray-600 mb-4">
                    Números que não saem há mais tempo
                  </p>
                  <div className="space-y-3">
                    {delayed.map((stat, idx) => (
                      <div
                        key={stat.id}
                        className="flex items-center justify-between bg-gray-50 rounded-lg p-3"
                      >
                        <div className="flex items-center gap-3">
                          <span className="text-sm font-semibold text-gray-500 w-6">
                            #{idx + 1}
                          </span>
                          <NumberBall
                            number={stat.number}
                            color={lotteryConfig?.color}
                            size="sm"
                          />
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-semibold text-gray-900">
                            {stat.delay} concursos
                          </p>
                          <p className="text-xs text-gray-500">
                            Freq: {stat.frequency}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>
              </div>

              {/* All Statistics Table */}
              <Card title="📊 Todas as Estatísticas" color={lotteryConfig?.color}>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Número
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Frequência
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Atraso
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Atraso Máximo
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Atraso Médio
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {allStats.map((stat) => (
                        <tr key={stat.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <NumberBall
                              number={stat.number}
                              color={lotteryConfig?.color}
                              size="sm"
                            />
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center">
                              <span className="mr-2 font-medium">{stat.frequency}</span>
                              <div className="flex-1 bg-gray-200 rounded-full h-2 w-24">
                                <div
                                  className="h-2 rounded-full"
                                  style={{
                                    width: `${(stat.frequency / maxFrequency) * 100}%`,
                                    backgroundColor: lotteryConfig?.color,
                                  }}
                                />
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {stat.delay}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {stat.max_delay}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {stat.average_delay.toFixed(1)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Card>
            </>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}
