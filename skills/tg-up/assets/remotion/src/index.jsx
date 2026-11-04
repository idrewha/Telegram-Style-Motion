import React from 'react';
import {registerRoot, Composition} from 'remotion';
import {TGUp} from './TGUp';
import defaults from '../props.json';

const Root = () => <Composition id="TGUp" component={TGUp}
  width={defaults.width} height={defaults.height} fps={defaults.fps}
  durationInFrames={defaults.durationInFrames} defaultProps={defaults}
  calculateMetadata={({props}) => ({width: props.width, height: props.height,
    fps: props.fps, durationInFrames: props.durationInFrames})} />;
registerRoot(Root);
