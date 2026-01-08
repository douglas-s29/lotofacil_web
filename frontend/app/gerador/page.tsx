'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Header from '@/components/ui/Header';
import Footer from '@/components/ui/Footer';
import NumberBall from '@/components/ui/NumberBall';
import Card from '@/components/ui/Card';
import { apiClient, LotteryConfig, GeneratorResponse } from '@/lib/api/client';
import { LOTTERY_CONFIGS } from '@/lib/utils';

export default function Gerador() {
  const searchParams = useSearchParams();
  const initialLottery = searchParams.get('lottery') || 'LOTOFACIL';

  const [lotteryType, setLotteryType] = useState(initialLottery);
  const [config, setConfig] = useState<LotteryConfig | null>(null);
  const [numbersCount, setNumbersCount] = useState(15);
  const [gamesCount, setGamesCount] = useState(5);
  const [selectedNumbers, setSelectedNumbers] = useState<number[]>([]);
  const [includeFrequent, setIncludeFrequent] = useState(false);
  const [includeDelayed, setIncludeDelayed] = useState(false);
  const [mixStrategy, setMixStrategy] = useState(true);
  const [result, setResult] = useState<GeneratorResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadConfig() {
      try {
        const data = await apiClient.getLottery(lotteryType);
        setConfig(data);
        setNumbersCount(data.numbers_to_pick);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Erro ao carregar configuração');
      }
    }

    loadConfig();
  }, [lotteryType]);

  const toggleNumber = (num: number) => {
    setSelectedNumbers((prev) =>
      prev.includes(num) ? prev.filter((n) => n !== num) : [...prev, num]
    );
  };

  const handleGenerate = async () => {
    if (!config) return;

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.generateCombinations({
        lottery_type: lotteryType,
        numbers_count: numbersCount,
        games_count: gamesCount,
        fixed_numbers: selectedNumbers.length > 0 ? selectedNumbers : undefined,
        include_frequent: includeFrequent,
        include_delayed: includeDelayed,
        mix_strategy: mixStrategy,
      });
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao gerar combinações');
    } finally {
      setLoading(false);
    }
  };

  const lotteryConfig = LOTTERY_CONFIGS[lotteryType as keyof typeof LOTTERY_CONFIGS];

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1 bg-gray-50 py-8">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">
            Gerador de Números
          </h1>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Configuration Panel */}
            <div className="lg:col-span-1">
              <Card title="Configurações" color={lotteryConfig?.color}>
                {/* Lottery Selection */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Loteria
                  </label>
                  <select
                    value={lotteryType}
                    onChange={(e) => {
                      setLotteryType(e.target.value);
                      setSelectedNumbers([]);
                      setResult(null);
                    }}
                    className="w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                  >
                    {Object.entries(LOTTERY_CONFIGS).map(([key, val]) => (
                      <option key={key} value={key}>
                        {val.displayName}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Numbers Count */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Números por jogo: {numbersCount}
                  </label>
                  <input
                    type="range"
                    min={config?.min_bet_numbers || config?.numbers_to_pick || 6}
                    max={config?.max_bet_numbers || config?.numbers_to_pick || 20}
                    value={numbersCount}
                    onChange={(e) => setNumbersCount(parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>

                {/* Games Count */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Quantidade de jogos: {gamesCount}
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="50"
                    value={gamesCount}
                    onChange={(e) => setGamesCount(parseInt(e.target.value))}
                    className="w-full"
                  />
                </div>

                {/* Filters */}
                <div className="mb-6 space-y-3">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={includeFrequent}
                      onChange={(e) => setIncludeFrequent(e.target.checked)}
                      className="rounded text-purple-600 focus:ring-purple-500"
                    />
                    <span className="ml-2 text-sm text-gray-700">Incluir frequentes</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={includeDelayed}
                      onChange={(e) => setIncludeDelayed(e.target.checked)}
                      className="rounded text-purple-600 focus:ring-purple-500"
                    />
                    <span className="ml-2 text-sm text-gray-700">Incluir atrasados</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={mixStrategy}
                      onChange={(e) => setMixStrategy(e.target.checked)}
                      className="rounded text-purple-600 focus:ring-purple-500"
                    />
                    <span className="ml-2 text-sm text-gray-700">Misturar estratégias</span>
                  </label>
                </div>

                {/* Generate Button */}
                <button
                  onClick={handleGenerate}
                  disabled={loading}
                  className="w-full bg-purple-600 text-white py-3 rounded-md font-semibold hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  {loading ? 'Gerando...' : 'Gerar Combinações'}
                </button>
              </Card>

              {/* Fixed Numbers */}
              {config && (
                <Card title="Números Fixos (Opcional)" color={lotteryConfig?.color} className="mt-6">
                  <p className="text-sm text-gray-600 mb-4">
                    Selecione números que devem aparecer em todas as combinações
                  </p>
                  <div className="grid grid-cols-5 gap-2">
                    {Array.from({ length: config.total_numbers }, (_, i) => i + 1).map((num) => (
                      <NumberBall
                        key={num}
                        number={num}
                        color={lotteryConfig?.color}
                        size="sm"
                        selected={selectedNumbers.includes(num)}
                        onClick={() => toggleNumber(num)}
                      />
                    ))}
                  </div>
                  {selectedNumbers.length > 0 && (
                    <button
                      onClick={() => setSelectedNumbers([])}
                      className="mt-4 text-sm text-purple-600 hover:text-purple-800"
                    >
                      Limpar seleção
                    </button>
                  )}
                </Card>
              )}
            </div>

            {/* Results Panel */}
            <div className="lg:col-span-2">
              {error && (
                <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
                  <p className="font-semibold">Erro</p>
                  <p className="text-sm">{error}</p>
                </div>
              )}

              {result && (
                <Card title="Combinações Geradas" color={lotteryConfig?.color}>
                  <div className="space-y-4">
                    {result.combinations.map((combination, idx) => (
                      <div
                        key={idx}
                        className="bg-gray-50 rounded-lg p-4 border border-gray-200"
                      >
                        <div className="flex items-center justify-between mb-3">
                          <span className="text-sm font-semibold text-gray-700">
                            Jogo {idx + 1}
                          </span>
                          <button className="text-xs text-purple-600 hover:text-purple-800">
                            Salvar
                          </button>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {combination.map((num) => (
                            <NumberBall
                              key={num}
                              number={num}
                              color={lotteryConfig?.color}
                              size="md"
                            />
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="mt-6 flex gap-4">
                    <button className="flex-1 bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-50">
                      Copiar Tudo
                    </button>
                    <button className="flex-1 bg-white border border-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-50">
                      Exportar PDF
                    </button>
                  </div>
                </Card>
              )}

              {!result && !error && (
                <div className="bg-white rounded-lg shadow-md p-12 text-center">
                  <div className="mx-auto h-16 w-16 text-gray-400 mb-4">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 10V3L4 14h7v7l9-11h-7z"
                      />
                    </svg>
                  </div>
                  <p className="text-gray-600">
                    Configure os parâmetros e clique em &quot;Gerar Combinações&quot;
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
