'use client';

import { motion } from 'framer-motion';

export default function EmotionAnalysisScreen() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="w-full max-w-2xl glass-card p-12 flex flex-col items-center justify-center"
    >
      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          rotate: [0, 360],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        className="text-8xl mb-6"
      >
        🧠
      </motion.div>
      
      <h2 className="text-2xl font-bold mb-2">Analyzing Emotions...</h2>
      <p className="text-white/70 text-center">
        Our AI is detecting the emotional signature of your message
      </p>

      <div className="flex gap-2 mt-8">
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            className="w-3 h-3 bg-white rounded-full"
            animate={{
              scale: [1, 1.5, 1],
              opacity: [0.3, 1, 0.3],
            }}
            transition={{
              duration: 1,
              repeat: Infinity,
              delay: i * 0.2,
            }}
          />
        ))}
      </div>
    </motion.div>
  );
}
