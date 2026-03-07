/**
 * API client for EMOTION CIPHER backend
 */
import axios from 'axios';
import { EncryptedPacket, DecryptionResult, AnalyzeResponse } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface EncryptRequest {
  message: string;
  user_secret: string;
}

export interface DecryptRequest {
  encrypted_packet: EncryptedPacket;
  user_secret: string;
}

export interface AnalyzeRequest {
  message: string;
}

export const encryptMessage = async (request: EncryptRequest): Promise<EncryptedPacket> => {
  try {
    const response = await api.post('/api/encrypt', request);
    // Parse the JSON string returned by the API
    const packet = typeof response.data.encrypted_packet === 'string' 
      ? JSON.parse(response.data.encrypted_packet)
      : response.data.encrypted_packet;
    return packet;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Encryption failed');
  }
};

export const decryptMessage = async (request: DecryptRequest): Promise<DecryptionResult> => {
  try {
    const response = await api.post('/api/decrypt', request);
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Decryption failed');
  }
};

export const analyzeEmotion = async (request: AnalyzeRequest): Promise<AnalyzeResponse> => {
  try {
    const response = await api.post('/api/analyze', request);
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Analysis failed');
  }
};
