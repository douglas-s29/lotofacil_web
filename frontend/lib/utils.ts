/**
 * Lottery type configurations
 */
export const LOTTERY_CONFIGS = {
  MEGA_SENA: {
    name: 'Mega-Sena',
    color: '#209869',
    displayName: 'Mega-Sena',
  },
  LOTOFACIL: {
    name: 'Lotofácil',
    color: '#930089',
    displayName: 'Lotofácil',
  },
  QUINA: {
    name: 'Quina',
    color: '#260085',
    displayName: 'Quina',
  },
  DUPLA_SENA: {
    name: 'Dupla Sena',
    color: '#A61324',
    displayName: 'Dupla Sena',
  },
  SUPER_SETE: {
    name: 'Super Sete',
    color: '#A8CF45',
    displayName: 'Super Sete',
  },
} as const;

export type LotteryType = keyof typeof LOTTERY_CONFIGS;

/**
 * Format currency to BRL
 */
export function formatCurrency(value: number | string): string {
  const numValue = typeof value === 'string' ? parseFloat(value) : value;
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(numValue);
}

/**
 * Format date to Brazilian format
 */
export function formatDate(date: string | Date): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('pt-BR').format(d);
}

/**
 * Get session key from localStorage or generate new one
 */
export function getSessionKey(): string {
  if (typeof window === 'undefined') return '';
  
  let sessionKey = localStorage.getItem('session_key');
  if (!sessionKey) {
    sessionKey = Math.random().toString(36).substring(2, 15) + 
                  Math.random().toString(36).substring(2, 15);
    localStorage.setItem('session_key', sessionKey);
  }
  return sessionKey;
}
