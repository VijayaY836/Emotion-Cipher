'use client';

import { motion } from 'framer-motion';
import { DecryptionResult, EmotionVector } from '@/lib/types';
import EmotionBars from './EmotionBars';

interface DecryptionResultScreenProps {
  result: DecryptionResult;
  onReset: () => void;
}

export default function DecryptionResultScreen({
  result,
  onReset,
}: DecryptionResultScreenProps) {
  const originalEmotions: EmotionVector = result.original_emotions as EmotionVector;
  const detectedEmotions: EmotionVector = result.detected_emotions as EmotionVector;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="w-full max-w-4xl space-y-6"
    >
      {/* Success Header */}
      <div className="glass-card p-6 text-center">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 200 }}
          className="text-6xl mb-4"
        >
          {result.emotion_verified ? '✅' : '⚠️'}
        </motion.div>
        <h2 className="text-3xl font-bold mb-2">Message Decrypted!</h2>
        <div className={`inline-block px-4 py-2 rounded-full ${
          result.emotion_verified 
            ? 'bg-green-500/20 border border-green-500/50' 
            : 'bg-yellow-500/20 border border-yellow-500/50'
        }`}>
          {result.emotion_verified 
            ? '✓ Emotion Verified' 
            : '⚠ Emotion Mismatch Detected'}
        </div>
      </div>

      {/* Decrypted Message */}
      <div className="glass-card p-6">
        <h3 className="text-xl font-semibold mb-4">Original Message</h3>
        <div className="bg-black/30 rounded-lg p-6">
          <p className="text-lg leading-relaxed">{result.message}</p>
        </div>
      </div>

      {/* Emotion Comparison */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <h3 className="text-xl font-semibold mb-4">Original Emotions</h3>
          <p className="text-sm text-white/70 mb-4">
            Emotions detected when the message was encrypted
          </p>
          <EmotionBars emotions={originalEmotions} animated={false} />
        </div>

        <div className="glass-card p-6">
          <h3 className="text-xl font-semibold mb-4">Re-analyzed Emotions</h3>
          <p className="text-sm text-white/70 mb-4">
            Emotions detected from the decrypted message
          </p>
          <EmotionBars emotions={detectedEmotions} animated={false} />
        </div>
      </div>

      {/* Verification Info */}
      <div className="glass-card p-6">
        <h3 className="text-xl font-semibold mb-4">About Emotion Verification</h3>
        <p className="text-white/70 leading-relaxed">
          {result.emotion_verified ? (
            <>
              The emotional signature matches! This means the decrypted message's emotions 
              are consistent with the original emotions detected during encryption. 
              This provides additional confidence that the message hasn't been tampered with.
            </>
          ) : (
            <>
              The emotional signatures don't match perfectly. This could mean the message 
              was modified, or there's natural variation in emotion detection. The message 
              was still decrypted successfully, but the emotional context may have changed.
            </>
          )}
        </p>
      </div>

      {/* Actions */}
      <div className="flex justify-center">
        <button
          onClick={onReset}
          className="glass-button px-8 py-3 font-medium"
        >
          🔄 Decrypt Another Message
        </button>
      </div>
    </motion.div>
  );
}
