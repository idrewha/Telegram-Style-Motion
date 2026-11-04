import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {sample, textPlan} from './motion.mjs';

// editorial composition-space text, not a replacement for recorded UI text.
export const MotionText = ({text, style = 'normal', timing = {}, fontFamily = 'Arial',
  fontSize = 64, fontWeight = 600, color = '#ffffff', align = 'left'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const plan = textPlan(text);
  return <div style={{fontFamily, fontSize, fontWeight, color, textAlign: align,
    lineHeight: 1.25, whiteSpace: 'pre-wrap', overflowWrap: 'normal'}}>
    {plan.parts.map((part, p) => part.break ? <br key={p}/> :
      <span key={p} style={{display: 'inline-block', whiteSpace: 'pre'}}>
        {part.units.map(unit => {
          const v = sample(style, frame/fps, unit.index, timing);
          return <span key={unit.index} style={{display: 'inline-block',
            opacity: v.opacity, transformOrigin: '50% 55%',
            transform: `translateY(${v.y}px) rotate(${v.rotation}deg) scaleY(${v.scaleY})`,
            ...(style === 'emotional' ? {filter: `blur(${v.blur}px)`} : {})}}>{unit.text}</span>;
        })}
      </span>)}
  </div>;
};
