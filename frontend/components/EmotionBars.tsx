'use client';

import { motion } from 'framer-motion';
import { EmotionVector, EMOTION_COLORS, EMOTION_LABELS } from '@/lib/types';

interface EmotionBarsProps {
  emotions: EmotionVector;
  animated?: boolean;
}

export default function EmotionBars({ emotions, animated = true }: EmotionBarsProps) {
  const emotionEntries = Object.entries(emotions) as [keyof EmotionVector, number][];

  return (
    <div className="space-y-4">
      {emotionEntries.map(([emotion, value], index) => (
        <div key={emotion} className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm font-semibold" style={{ color: EMOTION_COLORS[emotion] }}>
              {EMOTION_LABELS[emotion]}
            </span>
            <span className="text-sm text-gray-700 font-medium">
              {(value * 100).toFixed(1)}%
            </span>
          </div>
          <div className="h-3 bg-gray-200 rounded-full overflow-hidden border border-gray-300">
            <motion.div
              className="h-full rounded-full"
              style={{ backgroundColor: EMOTION_COLORS[emotion] }}
              initial={animated ? { width: 0 } : { width: `${value * 100}%` }}
              animate={{ width: `${value * 100}%` }}
              transition={{
                duration: 0.8,
                delay: animated ? index * 0.1 : 0,
                ease: 'easeOut',
              }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
