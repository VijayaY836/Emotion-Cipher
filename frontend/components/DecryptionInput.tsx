'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { decryptMessage } from '@/lib/api';
import { DecryptionResult, EncryptedPacket } from '@/lib/types';

interface DecryptionInputProps {
  onDecryptComplete: (result: DecryptionResult) => void;
}

export default function DecryptionInput({ onDecryptComplete }: DecryptionInputProps) {
  const [encryptedText, setEncryptedText] = useState('');
  const [secret, setSecret] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!encryptedText.trim() || !secret.trim()) {
      setError('Please enter both encrypted text and secret key');
      return;
    }

    setError('');
    setLoading(true);

    try {
      let packet: EncryptedPacket;
      
      // Check if it's the new format (EC1:...) or old JSON format
      if (encryptedText.trim().startsWith('EC1:')) {
        // Parse new compact format: EC1:encrypted_text:iv:base64_emotions
        const parts = encryptedText.trim().split(':');
        if (parts.length !== 4) {
          throw new Error('Invalid encrypted text format');
        }
        
        const [, encrypted_text, iv, emotionsBase64] = parts;
        const emotion_signature = JSON.parse(atob(emotionsBase64));
        
        packet = {
          encrypted_text,
          iv,
          emotion_signature,
          dominant_emotions: [],
          emotional_intensity: 0
        };
      } else {
        // Try parsing as JSON (backward compatibility)
        packet = JSON.parse(encryptedText);
      }
      
      // Validate packet structure
      if (!packet.encrypted_text || !packet.iv || !packet.emotion_signature) {
        throw new Error('Invalid encrypted packet structure');
      }

      const result = await decryptMessage({
        encrypted_packet: packet,
        user_secret: secret,
      });

      onDecryptComplete(result);
    } catch (err: any) {
      if (err instanceof SyntaxError) {
        setError('Invalid format. Please paste a valid encrypted text.');
      } else {
        setError(err.message || 'Decryption failed');
      }
    } finally {
      setLoading(false);
    }
  };

  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      setEncryptedText(text);
    } catch (err) {
      setError('Failed to read from clipboard');
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
          <div className="flex justify-between items-center mb-2">
            <label className="block text-sm font-medium">Encrypted Text</label>
            <button
              type="button"
              onClick={handlePaste}
              className="text-sm text-white/70 hover:text-white transition-colors"
            >
              📋 Paste from Clipboard
            </button>
          </div>
          <textarea
            value={encryptedText}
            onChange={(e) => setEncryptedText(e.target.value)}
            placeholder='EC1:9x@T!azKP#13qWv$:...'
            className="glass-input w-full h-32 resize-none font-mono text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Secret Key</label>
          <input
            type="password"
            value={secret}
            onChange={(e) => setSecret(e.target.value)}
            placeholder="Enter the secret key..."
            className="glass-input w-full"
          />
          <p className="text-xs text-white/50 mt-2">
            Use the same key that was used to encrypt the message
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
          disabled={loading || !encryptedText.trim() || !secret.trim()}
          className="glass-button w-full py-4 font-semibold text-lg disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? '🔓 Decrypting...' : '🔓 Decrypt Message'}
        </button>
      </form>
    </motion.div>
  );
}
