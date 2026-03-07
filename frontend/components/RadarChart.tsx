'use client';

import { Radar, RadarChart as RechartsRadar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import { EmotionVector, EMOTION_COLORS, EMOTION_LABELS } from '@/lib/types';

interface RadarChartProps {
  emotions: EmotionVector;
}

export default function RadarChart({ emotions }: RadarChartProps) {
  const data = Object.entries(emotions).map(([emotion, value]) => ({
    emotion: EMOTION_LABELS[emotion as keyof EmotionVector],
    value: value * 100,
    fullMark: 100,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <RechartsRadar data={data}>
        <PolarGrid stroke="#667eea" strokeWidth={2} />
        <PolarAngleAxis 
          dataKey="emotion" 
          tick={{ fill: '#1a1a2e', fontSize: 13, fontWeight: 600 }}
        />
        <PolarRadiusAxis 
          angle={90} 
          domain={[0, 100]}
          tick={{ fill: '#667eea', fontSize: 11, fontWeight: 500 }}
        />
        <Radar
          name="Emotions"
          dataKey="value"
          stroke="#667eea"
          strokeWidth={3}
          fill="#764ba2"
          fillOpacity={0.6}
        />
      </RechartsRadar>
    </ResponsiveContainer>
  );
}
