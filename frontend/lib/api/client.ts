/**
 * API Client for Lotofácil Web
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface LotteryConfig {
  id: number;
  lottery_type: string;
  total_numbers: number;
  numbers_to_pick: number;
  min_bet_numbers?: number;
  max_bet_numbers?: number;
  primary_color: string;
  description: string;
}

export interface Draw {
  id: number;
  lottery_type: string;
  contest_number: number;
  draw_date: string;
  numbers: number[];
  numbers_second_draw?: number[];
  prize_amount?: string;
  winners_count?: number;
  accumulated: boolean;
  next_estimated_prize?: string;
  created_at: string;
  updated_at?: string;
}

export interface NumberStatistics {
  id: number;
  lottery_type: string;
  number: number;
  frequency: number;
  last_draw_contest?: number;
  delay: number;
  max_delay: number;
  average_delay: number;
  last_updated: string;
}

export interface UserCombination {
  id: number;
  lottery_type: string;
  name: string;
  numbers: number[];
  session_key?: string;
  created_at: string;
  is_favorite: boolean;
}

export interface GeneratorRequest {
  lottery_type: string;
  numbers_count: number;
  games_count: number;
  fixed_numbers?: number[];
  include_frequent?: boolean;
  include_delayed?: boolean;
  mix_strategy?: boolean;
}

export interface GeneratorResponse {
  lottery_type: string;
  combinations: number[][];
  metadata: {
    numbers_per_game: number;
    total_games: number;
    fixed_numbers: number[];
    include_frequent: boolean;
    include_delayed: boolean;
  };
}

export interface CheckerRequest {
  lottery_type: string;
  numbers: number[];
  contest_number?: number;
}

export interface CheckerResponse {
  found: boolean;
  contest_number?: number;
  draw_date?: string;
  drawn_numbers?: number[];
  user_numbers: number[];
  matches: number[];
  match_count: number;
  is_winner: boolean;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `API error: ${response.status}`);
    }

    return response.json();
  }

  // Lottery endpoints
  async getLotteries(): Promise<LotteryConfig[]> {
    return this.fetchApi<LotteryConfig[]>('/api/lotteries/');
  }

  async getLottery(lotteryType: string): Promise<LotteryConfig> {
    return this.fetchApi<LotteryConfig>(`/api/lotteries/${lotteryType}`);
  }

  async getDraws(lotteryType: string, limit: number = 20, offset: number = 0): Promise<Draw[]> {
    return this.fetchApi<Draw[]>(`/api/lotteries/${lotteryType}/draws?limit=${limit}&offset=${offset}`);
  }

  async getLatestDraw(lotteryType: string): Promise<Draw> {
    return this.fetchApi<Draw>(`/api/lotteries/${lotteryType}/draws/latest`);
  }

  async getDraw(lotteryType: string, contestNumber: number): Promise<Draw> {
    return this.fetchApi<Draw>(`/api/lotteries/${lotteryType}/draws/${contestNumber}`);
  }

  // Statistics endpoints
  async getStatistics(lotteryType: string, limit?: number): Promise<NumberStatistics[]> {
    const url = limit 
      ? `/api/statistics/${lotteryType}?limit=${limit}`
      : `/api/statistics/${lotteryType}`;
    return this.fetchApi<NumberStatistics[]>(url);
  }

  async getMostFrequent(lotteryType: string, limit: number = 10): Promise<NumberStatistics[]> {
    return this.fetchApi<NumberStatistics[]>(`/api/statistics/${lotteryType}/frequent?limit=${limit}`);
  }

  async getMostDelayed(lotteryType: string, limit: number = 10): Promise<NumberStatistics[]> {
    return this.fetchApi<NumberStatistics[]>(`/api/statistics/${lotteryType}/delayed?limit=${limit}`);
  }

  async calculateStatistics(lotteryType: string): Promise<{ message: string }> {
    return this.fetchApi<{ message: string }>(`/api/statistics/${lotteryType}/calculate`, {
      method: 'POST',
    });
  }

  // Generator endpoints
  async generateCombinations(request: GeneratorRequest): Promise<GeneratorResponse> {
    return this.fetchApi<GeneratorResponse>('/api/generator/generate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async validateCombination(lotteryType: string, numbers: number[]): Promise<{
    valid: boolean;
    errors: string[];
    warnings: string[];
  }> {
    return this.fetchApi(`/api/generator/validate?lottery_type=${lotteryType}`, {
      method: 'POST',
      body: JSON.stringify(numbers),
    });
  }

  // Checker endpoints
  async checkCombination(request: CheckerRequest): Promise<CheckerResponse> {
    return this.fetchApi<CheckerResponse>('/api/checker/check', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // User combinations endpoints
  async getUserCombinations(
    lotteryType?: string,
    sessionKey?: string,
    limit: number = 50
  ): Promise<UserCombination[]> {
    const params = new URLSearchParams();
    if (lotteryType) params.append('lottery_type', lotteryType);
    if (sessionKey) params.append('session_key', sessionKey);
    params.append('limit', limit.toString());

    return this.fetchApi<UserCombination[]>(`/api/combinations/?${params.toString()}`);
  }

  async createUserCombination(combination: {
    lottery_type: string;
    name: string;
    numbers: number[];
    session_key?: string;
    is_favorite?: boolean;
  }): Promise<UserCombination> {
    return this.fetchApi<UserCombination>('/api/combinations/', {
      method: 'POST',
      body: JSON.stringify(combination),
    });
  }

  async getUserCombination(combinationId: number): Promise<UserCombination> {
    return this.fetchApi<UserCombination>(`/api/combinations/${combinationId}`);
  }

  async deleteUserCombination(combinationId: number): Promise<{ message: string }> {
    return this.fetchApi<{ message: string }>(`/api/combinations/${combinationId}`, {
      method: 'DELETE',
    });
  }

  async toggleFavorite(combinationId: number): Promise<UserCombination> {
    return this.fetchApi<UserCombination>(`/api/combinations/${combinationId}/favorite`, {
      method: 'PUT',
    });
  }
}

// Export a singleton instance
export const apiClient = new ApiClient();
