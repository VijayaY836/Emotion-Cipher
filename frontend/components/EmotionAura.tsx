'use client';

import { motion } from 'framer-motion';
import { EmotionVector, EMOTION_COLORS } from '@/lib/types';
import { useMemo } from 'react';

interface EmotionAuraProps {
  emotions: EmotionVector;
  size?: number;
}

export default function EmotionAura({ emotions, size = 200 }: EmotionAuraProps) {
  const dominantEmotion = useMemo(() => {
    const entries = Object.entries(emotions) as [keyof EmotionVector, number][];
    const sorted = entries.sort((a, b) => b[1] - a[1]);
    return sorted[0][0];
  }, [emotions]);

  const dominantColor = EMOTION_COLORS[dominantEmotion];

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      {/* Outer glow */}
      <motion.div
        className="absolute rounded-full"
        style={{
          width: size,
          height: size,
          background: `radial-gradient(circle, ${dominantColor}40 0%, transparent 70%)`,
        }}
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.6, 0.8, 0.6],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
      
      {/* Middle glow */}
      <motion.div
        className="absolute rounded-full"
        style={{
          width: size * 0.7,
          height: size * 0.7,
          background: `radial-gradient(circle, ${dominantColor}60 0%, transparent 70%)`,
        }}
        animate={{
          scale: [1, 1.15, 1],
          opacity: [0.7, 0.9, 0.7],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
      
      {/* Inner core */}
      <motion.div
        className="absolute rounded-full"
        style={{
          width: size * 0.4,
          height: size * 0.4,
          backgroundColor: dominantColor,
          boxShadow: `0 0 ${size * 0.3}px ${dominantColor}80`,
        }}
        animate={{
          scale: [1, 1.1, 1],
        }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
    </div>
  );
}
