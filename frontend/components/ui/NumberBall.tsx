interface NumberBallProps {
  number: number;
  color?: string;
  size?: 'sm' | 'md' | 'lg';
  selected?: boolean;
  onClick?: () => void;
}

export default function NumberBall({
  number,
  color = '#930089',
  size = 'md',
  selected = false,
  onClick,
}: NumberBallProps) {
  const sizeClasses = {
    sm: 'w-10 h-10 text-sm',
    md: 'w-12 h-12 text-base',
    lg: 'w-16 h-16 text-lg',
  };

  return (
    <button
      onClick={onClick}
      disabled={!onClick}
      className={`
        ${sizeClasses[size]}
        rounded-full
        font-bold
        text-white
        flex
        items-center
        justify-center
        transition-all
        ${onClick ? 'cursor-pointer hover:scale-110' : 'cursor-default'}
        ${selected ? 'ring-4 ring-yellow-400 scale-110' : ''}
      `}
      style={{ backgroundColor: color }}
    >
      {number.toString().padStart(2, '0')}
    </button>
  );
}
