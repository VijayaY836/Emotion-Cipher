'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { EncryptedPacket, EmotionVector } from '@/lib/types';
import EmotionBars from './EmotionBars';
import EmotionAura from './EmotionAura';
import RadarChart from './RadarChart';

interface EncryptionResultScreenProps {
  encryptedPacket: EncryptedPacket;
  emotions: EmotionVector;
  onReset: () => void;
}

export default function EncryptionResultScreen({
  encryptedPacket,
  emotions,
  onReset,
}: EncryptionResultScreenProps) {
  const [copied, setCopied] = useState(false);

  // Create a compact encrypted string that includes all necessary data
  const encryptedString = `EC1:${encryptedPacket.encrypted_text}:${encryptedPacket.iv}:${btoa(JSON.stringify(encryptedPacket.emotion_signature))}`;

  const handleCopy = () => {
    navigator.clipboard.writeText(encryptedString);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const packetJson = JSON.stringify(encryptedPacket, null, 2);
    const blob = new Blob([packetJson], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'encrypted-message.json';
    a.click();
    URL.revokeObjectURL(url);
  };

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
          ✨
        </motion.div>
        <h2 className="text-3xl font-bold mb-2 text-gray-800">Message Encrypted!</h2>
        <p className="text-gray-600">
          Your message has been encrypted with its emotional signature
        </p>
      </div>

      {/* Emotion Visualization */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">Emotion Analysis</h3>
          <EmotionBars emotions={emotions} />
        </div>

        <div className="glass-card p-6 flex flex-col items-center">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">Emotional Aura</h3>
          <EmotionAura emotions={emotions} size={180} />
          <div className="mt-4 text-center">
            <p className="text-sm text-gray-600">Dominant Emotions</p>
            <p className="font-medium text-gray-800">
              {encryptedPacket.dominant_emotions.join(', ') || 'Neutral'}
            </p>
          </div>
        </div>
      </div>

      {/* Radar Chart */}
      <div className="glass-card p-6">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">Emotional Profile</h3>
        <RadarChart emotions={emotions} />
      </div>

      {/* Encrypted Text */}
      <div className="glass-card p-6">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">Encrypted Text</h3>
        <div className="bg-gray-800 rounded-lg p-4 font-mono text-sm break-all border-2 border-purple-300">
          <p className="text-green-400 font-semibold">
            {encryptedString}
          </p>
        </div>

        <div className="flex gap-4 mt-4">
          <button
            onClick={handleCopy}
            className="glass-button flex-1 py-3 font-medium"
          >
            {copied ? '✓ Copied!' : '📋 Copy Encrypted Text'}
          </button>
        </div>
        
        <p className="text-xs text-gray-600 mt-3 text-center">
          Share this encrypted text with anyone. They'll need your secret key to decrypt it.
        </p>
      </div>

      {/* Actions */}
      <div className="flex justify-center">
        <button
          onClick={onReset}
          className="glass-button px-8 py-3 font-medium"
        >
          🔄 Encrypt Another Message
        </button>
      </div>
    </motion.div>
  );
}
