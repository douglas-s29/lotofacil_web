'use client';

import { useState } from 'react';
import Header from '@/components/ui/Header';
import Footer from '@/components/ui/Footer';
import NumberBall from '@/components/ui/NumberBall';
import Card from '@/components/ui/Card';
import { apiClient, CheckerResponse } from '@/lib/api/client';
import { LOTTERY_CONFIGS, formatDate } from '@/lib/utils';

export default function Conferidor() {
  const [lotteryType, setLotteryType] = useState('LOTOFACIL');
  const [selectedNumbers, setSelectedNumbers] = useState<number[]>([]);
  const [contestNumber, setContestNumber] = useState('');
  const [result, setResult] = useState<CheckerResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const lotteryConfig = LOTTERY_CONFIGS[lotteryType as keyof typeof LOTTERY_CONFIGS];
  const totalNumbers = lotteryType === 'LOTOFACIL' ? 25 : lotteryType === 'MEGA_SENA' ? 60 : 80;

  const toggleNumber = (num: number) => {
    setSelectedNumbers((prev) =>
      prev.includes(num) ? prev.filter((n) => n !== num) : [...prev, num]
    );
  };

  const handleCheck = async () => {
    if (selectedNumbers.length === 0) {
      setError('Selecione pelo menos um número');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.checkCombination({
        lottery_type: lotteryType,
        numbers: selectedNumbers,
        contest_number: contestNumber ? parseInt(contestNumber) : undefined,
      });
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao conferir números');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1 bg-gray-50 py-8">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">
            Conferidor de Resultados
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

                {/* Contest Number */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Concurso (opcional)
                  </label>
                  <input
                    type="number"
                    value={contestNumber}
                    onChange={(e) => setContestNumber(e.target.value)}
                    placeholder="Deixe vazio para o último"
                    className="w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    Se não informado, será comparado com o último sorteio
                  </p>
                </div>

                {/* Check Button */}
                <button
                  onClick={handleCheck}
                  disabled={loading || selectedNumbers.length === 0}
                  className="w-full bg-purple-600 text-white py-3 rounded-md font-semibold hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  {loading ? 'Conferindo...' : 'Conferir Números'}
                </button>

                <div className="mt-4 text-sm text-gray-600">
                  <p>Números selecionados: {selectedNumbers.length}</p>
                </div>
              </Card>
            </div>

            {/* Number Selection and Results */}
            <div className="lg:col-span-2 space-y-6">
              {/* Number Selection */}
              <Card title="Selecione seus números" color={lotteryConfig?.color}>
                <div className="grid grid-cols-5 sm:grid-cols-8 md:grid-cols-10 gap-2">
                  {Array.from({ length: totalNumbers }, (_, i) => i + 1).map((num) => (
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
                  <div className="mt-4 flex justify-between items-center">
                    <button
                      onClick={() => setSelectedNumbers([])}
                      className="text-sm text-purple-600 hover:text-purple-800"
                    >
                      Limpar seleção
                    </button>
                  </div>
                )}
              </Card>

              {/* Error Message */}
              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
                  <p className="font-semibold">Erro</p>
                  <p className="text-sm">{error}</p>
                </div>
              )}

              {/* Results */}
              {result && (
                <Card
                  title={result.is_winner ? '🎉 Parabéns!' : 'Resultado'}
                  color={lotteryConfig?.color}
                >
                  {result.found ? (
                    <>
                      <div className="mb-6">
                        <div className="grid grid-cols-2 gap-4 mb-4">
                          <div>
                            <p className="text-sm text-gray-600">Concurso</p>
                            <p className="text-lg font-semibold text-gray-900">
                              #{result.contest_number}
                            </p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-600">Data</p>
                            <p className="text-lg font-semibold text-gray-900">
                              {result.draw_date ? formatDate(result.draw_date) : '-'}
                            </p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-600">Acertos</p>
                            <p
                              className={`text-2xl font-bold ${
                                result.is_winner ? 'text-green-600' : 'text-gray-900'
                              }`}
                            >
                              {result.match_count}
                            </p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-600">Status</p>
                            <p
                              className={`text-lg font-semibold ${
                                result.is_winner ? 'text-green-600' : 'text-gray-600'
                              }`}
                            >
                              {result.is_winner ? 'Premiado!' : 'Não premiado'}
                            </p>
                          </div>
                        </div>
                      </div>

                      <div className="space-y-4">
                        <div>
                          <p className="text-sm font-medium text-gray-700 mb-2">
                            Números Sorteados
                          </p>
                          <div className="flex flex-wrap gap-2">
                            {result.drawn_numbers?.map((num) => (
                              <NumberBall
                                key={num}
                                number={num}
                                color={lotteryConfig?.color}
                                size="md"
                              />
                            ))}
                          </div>
                        </div>

                        <div>
                          <p className="text-sm font-medium text-gray-700 mb-2">
                            Seus Números
                          </p>
                          <div className="flex flex-wrap gap-2">
                            {result.user_numbers.map((num) => (
                              <NumberBall
                                key={num}
                                number={num}
                                color={
                                  result.matches.includes(num)
                                    ? '#10b981'
                                    : '#6b7280'
                                }
                                size="md"
                              />
                            ))}
                          </div>
                        </div>

                        {result.matches.length > 0 && (
                          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                            <p className="text-sm font-medium text-green-900 mb-2">
                              Números Acertados ({result.matches.length})
                            </p>
                            <div className="flex flex-wrap gap-2">
                              {result.matches.map((num) => (
                                <NumberBall
                                  key={num}
                                  number={num}
                                  color="#10b981"
                                  size="md"
                                />
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </>
                  ) : (
                    <div className="text-center py-8">
                      <p className="text-gray-600">
                        Nenhum resultado encontrado para este concurso.
                      </p>
                    </div>
                  )}
                </Card>
              )}

              {/* Initial State */}
              {!result && !error && (
                <div className="bg-white rounded-lg shadow-md p-12 text-center">
                  <div className="mx-auto h-16 w-16 text-gray-400 mb-4">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
                      />
                    </svg>
                  </div>
                  <p className="text-gray-600">
                    Selecione seus números e clique em &quot;Conferir Números&quot;
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
