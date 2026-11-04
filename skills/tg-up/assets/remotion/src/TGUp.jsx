import React from 'react';
import {AbsoluteFill, Sequence, staticFile} from 'remotion';
import {Video, Audio} from '@remotion/media';
import {MotionText} from './MotionText';

export const TGUp = ({base, texts = [], audio = [], durationInFrames}) =>
  <AbsoluteFill style={{backgroundColor: '#000'}}>
    <Video src={staticFile(base.src)} muted={base.muted}
      durationInFrames={durationInFrames} objectFit="contain" style={{width: '100%', height: '100%'}}/>
    {texts.map(t => <Sequence key={t.id} name={t.id} from={t.from}
      durationInFrames={t.duration} layout="none">
      <div style={{position: 'absolute', left: t.x, top: t.y, width: t.width}}>
        <MotionText {...t}/>
      </div>
    </Sequence>)}
    {audio.map(a => <Sequence key={a.id} name={a.id} from={a.from}
      durationInFrames={a.duration}>
      <Audio src={staticFile(a.src)} trimBefore={a.trimBefore} volume={a.volume}/>
    </Sequence>)}
  </AbsoluteFill>;
