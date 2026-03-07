'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { encryptMessage } from '@/lib/api';
import { EncryptedPacket, EmotionVector } from '@/lib/types';

interface MessageInputProps {
  onEncryptStart: () => void;
  onEncryptComplete: (packet: EncryptedPacket, emotions: EmotionVector) => void;
}

export default function MessageInput({ onEncryptStart, onEncryptComplete }: MessageInputProps) {
  const [message, setMessage] = useState('');
  const [secret, setSecret] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!message.trim() || !secret.trim()) {
      setError('Please enter both message and secret key');
      return;
    }

    setError('');
    setLoading(true);
    onEncryptStart();

    try {
      const packet = await encryptMessage({
        message: message.trim(),
        user_secret: secret,
      });

      // Extract emotion vector from packet
      const emotions: EmotionVector = packet.emotion_signature;

      // Simulate analysis time for better UX
      setTimeout(() => {
        onEncryptComplete(packet, emotions);
        setLoading(false);
      }, 1500);
    } catch (err: any) {
      setError(err.message || 'Encryption failed');
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="w-full max-w-2xl"
    >
      <form onSubmit={handleSubmit} className="glass-card p-8 space-y-6">
        <div>
          <label className="block text-sm font-medium mb-2">Your Message</label>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message here..."
            className="glass-input w-full h-40 resize-none"
            maxLength={10000}
          />
          <div className="text-right text-sm text-white/50 mt-2">
            {message.length} / 10000 characters
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Secret Key</label>
          <input
            type="password"
            value={secret}
            onChange={(e) => setSecret(e.target.value)}
            placeholder="Enter your secret key..."
            className="glass-input w-full"
          />
          <p className="text-xs text-white/50 mt-2">
            This key will be used to encrypt your message. Keep it safe!
          </p>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-red-500/20 border border-red-500/50 rounded-lg p-3 text-sm"
          >
            {error}
          </motion.div>
        )}

        <button
          type="submit"
          disabled={loading || !message.trim() || !secret.trim()}
          className="glass-button w-full py-4 font-semibold text-lg disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? '🔐 Encrypting...' : '🔐 Encrypt Message'}
        </button>
      </form>
    </motion.div>
  );
}
