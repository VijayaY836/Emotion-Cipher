'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import MessageInput from '@/components/MessageInput';
import EmotionAnalysisScreen from '@/components/EmotionAnalysisScreen';
import EncryptionResultScreen from '@/components/EncryptionResultScreen';
import DecryptionInput from '@/components/DecryptionInput';
import DecryptionResultScreen from '@/components/DecryptionResultScreen';
import { EncryptedPacket, DecryptionResult, EmotionVector } from '@/lib/types';

type Screen = 'input' | 'analyzing' | 'result' | 'decrypt-input' | 'decrypt-result';

export default function Home() {
  const [screen, setScreen] = useState<Screen>('input');
  const [mode, setMode] = useState<'encrypt' | 'decrypt'>('encrypt');
  const [emotions, setEmotions] = useState<EmotionVector | null>(null);
  const [encryptedPacket, setEncryptedPacket] = useState<EncryptedPacket | null>(null);
  const [decryptionResult, setDecryptionResult] = useState<DecryptionResult | null>(null);
  const [useImageBg, setUseImageBg] = useState(true);

  const handleEncryptStart = () => {
    setScreen('analyzing');
  };

  const handleEncryptComplete = (packet: EncryptedPacket, emotionVector: EmotionVector) => {
    setEncryptedPacket(packet);
    setEmotions(emotionVector);
    setScreen('result');
  };

  const handleDecryptComplete = (result: DecryptionResult) => {
    setDecryptionResult(result);
    setScreen('decrypt-result');
  };

  const handleReset = () => {
    setScreen(mode === 'encrypt' ? 'input' : 'decrypt-input');
    setEmotions(null);
    setEncryptedPacket(null);
    setDecryptionResult(null);
  };

  const handleModeSwitch = (newMode: 'encrypt' | 'decrypt') => {
    setMode(newMode);
    setScreen(newMode === 'encrypt' ? 'input' : 'decrypt-input');
    setEmotions(null);
    setEncryptedPacket(null);
    setDecryptionResult(null);
  };

  return (
    <main className={`min-h-screen relative overflow-hidden ${useImageBg ? 'bg-image' : 'bg-gradient'}`}>
      {/* Background Toggle Button */}
      <motion.button
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 0.6 }}
        onClick={() => setUseImageBg(!useImageBg)}
        className="fixed top-8 right-8 z-50 bg-toggle-button px-5 py-3 text-sm font-semibold flex items-center gap-2 shadow-xl hover:shadow-2xl transition-all duration-300"
        title={useImageBg ? "Switch to Gradient" : "Switch to Image"}
      >
        <span className="text-xl">{useImageBg ? '🎨' : '🖼️'}</span>
        <span className="hidden sm:inline text-white">
          {useImageBg ? 'Gradient' : 'Image'}
        </span>
      </motion.button>

      {/* Animated background particles */}
      <div className="particles">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="particle"
            style={{
              width: Math.random() * 10 + 5 + 'px',
              height: Math.random() * 10 + 5 + 'px',
              left: Math.random() * 100 + '%',
              top: Math.random() * 100 + '%',
              animationDelay: Math.random() * 20 + 's',
              animationDuration: Math.random() * 10 + 15 + 's',
            }}
          />
        ))}
      </div>

      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center p-4 md:p-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <motion.div
            animate={{
              scale: [1, 1.1, 1],
              rotate: [0, 5, -5, 0],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
            className="text-8xl mb-6"
          >
            🎭
          </motion.div>
          <h1 className="text-6xl md:text-7xl font-black mb-4 leading-tight text-gray-900 drop-shadow-lg">
            EMOTION CIPHER
          </h1>
          <p className="text-xl md:text-2xl font-medium text-gray-700 max-w-2xl mx-auto mb-6">
            Encrypt your messages with emotions. Decrypt with feelings.
          </p>
          <div className="flex gap-3 justify-center flex-wrap">
            <span className="emotion-badge">
              <span className="text-2xl">🔐</span>
              <span style={{ color: '#667eea' }}>AES-256</span>
            </span>
            <span className="emotion-badge">
              <span className="text-2xl">🤖</span>
              <span style={{ color: '#764ba2' }}>AI Powered</span>
            </span>
            <span className="emotion-badge">
              <span className="text-2xl">💝</span>
              <span style={{ color: '#f093fb' }}>Privacy + Empathy</span>
            </span>
          </div>
        </motion.div>

        {/* Mode Toggle */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="flex gap-4 mb-8"
        >
          <button
            onClick={() => handleModeSwitch('encrypt')}
            className={`glass-button px-8 py-4 font-semibold text-lg transition-all ${
              mode === 'encrypt' ? 'ring-4 ring-purple-300' : 'opacity-70'
            }`}
          >
            🔐 Encrypt
          </button>
          <button
            onClick={() => handleModeSwitch('decrypt')}
            className={`glass-button px-8 py-4 font-semibold text-lg transition-all ${
              mode === 'decrypt' ? 'ring-4 ring-purple-300' : 'opacity-70'
            }`}
          >
            🔓 Decrypt
          </button>
        </motion.div>

        {/* Screens */}
        <AnimatePresence mode="wait">
          {screen === 'input' && (
            <MessageInput
              key="input"
              onEncryptStart={handleEncryptStart}
              onEncryptComplete={handleEncryptComplete}
            />
          )}

          {screen === 'analyzing' && (
            <EmotionAnalysisScreen key="analyzing" />
          )}

          {screen === 'result' && encryptedPacket && emotions && (
            <EncryptionResultScreen
              key="result"
              encryptedPacket={encryptedPacket}
              emotions={emotions}
              onReset={handleReset}
            />
          )}

          {screen === 'decrypt-input' && (
            <DecryptionInput
              key="decrypt-input"
              onDecryptComplete={handleDecryptComplete}
            />
          )}

          {screen === 'decrypt-result' && decryptionResult && (
            <DecryptionResultScreen
              key="decrypt-result"
              result={decryptionResult}
              onReset={handleReset}
            />
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}
