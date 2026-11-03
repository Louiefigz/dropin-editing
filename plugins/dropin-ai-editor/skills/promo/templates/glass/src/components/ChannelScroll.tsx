import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { loadFont as loadPoppins } from '@remotion/google-fonts/Poppins';
import { COLORS } from '../constants';
import { GlassPanel } from './GlassPanel';

const { fontFamily: poppins } = loadPoppins();

// Sample long-form MIDS grid. Placeholder ids: each loads public/clips/yt_long/<id>.jpg. Replace them with
// your own channel's videos and runtimes.
const THUMBS = [
  { id: 'thumb_01', d: '8:31' }, { id: 'thumb_02', d: '9:04' }, { id: 'thumb_03', d: '7:13' },
  { id: 'thumb_04', d: '7:06' }, { id: 'thumb_05', d: '9:40' }, { id: 'thumb_06', d: '1:27' },
  { id: 'thumb_07', d: '13:58' }, { id: 'thumb_08', d: '8:00' }, { id: 'thumb_09', d: '5:15' },
  { id: 'thumb_10', d: '5:18' }, { id: 'thumb_11', d: '8:55' }, { id: 'thumb_12', d: '34:17' },
  { id: 'thumb_13', d: '10:58' }, { id: 'thumb_14', d: '11:36' }, { id: 'thumb_15', d: '4:55' },
  { id: 'thumb_16', d: '2:03' },
];

export const ChannelScroll: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - 2, fps, config: { damping: 200, stiffness: 100, mass: 0.6 } });
  const scroll = frame * 6; // px/frame upward scroll

  const COLS = 3, cw = 300, ch = 169, gap = 14;
  const cells = Array.from({ length: 30 }, (_, i) => THUMBS[i % THUMBS.length]);

  return (
    <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center' }}>
      <GlassPanel radius={18} sheen={false} style={{ width: 980, height: 880, padding: 0, display: 'flex', flexDirection: 'column', opacity: s, transform: `scale(${interpolate(s, [0, 1], [0.97, 1])})` }}>
        {/* browser bar */}
        <div style={{ height: 46, flexShrink: 0, display: 'flex', alignItems: 'center', gap: 9, padding: '0 16px', borderBottom: '1px solid rgba(255,255,255,0.10)', background: 'rgba(255,255,255,0.05)' }}>
          {['#ff5f56', '#ffbd2e', '#27c93f'].map((c) => <div key={c} style={{ width: 11, height: 11, borderRadius: '50%', background: c, opacity: 0.85 }} />)}
          <div style={{ marginLeft: 'auto', marginRight: 'auto', fontFamily: poppins, fontWeight: 400, fontSize: 14, color: 'rgba(255,255,255,0.6)' }}>youtube.com/@Highlights</div>
        </div>
        {/* channel header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, padding: '16px 22px', flexShrink: 0, borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
          <div style={{ width: 56, height: 56, borderRadius: '50%', background: `linear-gradient(135deg, ${COLORS.indigo}, ${COLORS.lavender})`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: poppins, fontWeight: 800, fontSize: 24, color: '#fff' }}>M</div>
          <div>
            <div style={{ fontFamily: poppins, fontWeight: 700, fontSize: 24, color: '#fff' }}>Highlights</div>
            <div style={{ fontFamily: poppins, fontWeight: 400, fontSize: 15, color: 'rgba(255,255,255,0.55)' }}>@Highlights · Videos · the highlights channel</div>
          </div>
          <div style={{ marginLeft: 'auto', display: 'flex', gap: 20, fontFamily: poppins, fontWeight: 600, fontSize: 15 }}>
            <span style={{ color: 'rgba(255,255,255,0.5)' }}>Home</span>
            <span style={{ color: 'rgba(255,255,255,0.5)' }}>Shorts</span>
            <span style={{ color: '#fff', borderBottom: '2px solid #fff', paddingBottom: 4 }}>Videos</span>
          </div>
        </div>
        {/* scrolling shorts grid */}
        <div style={{ flex: 1, position: 'relative', overflow: 'hidden' }}>
          <div style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: 16, display: 'grid', gridTemplateColumns: `repeat(${COLS}, ${cw}px)`, gap, justifyContent: 'center', transform: `translateY(${-scroll}px)` }}>
            {cells.map((c, i) => {
              return (
                <div key={i} style={{ width: cw, height: ch, borderRadius: 10, overflow: 'hidden', background: '#000', position: 'relative', border: '1px solid rgba(255,255,255,0.06)' }}>
                  <Img src={staticFile(`clips/yt_long/${c.id}.jpg`)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                  <div style={{ position: 'absolute', bottom: 8, right: 8, display: 'flex', alignItems: 'center', gap: 5, fontFamily: poppins, fontWeight: 600, fontSize: 13, color: '#fff', background: 'rgba(0,0,0,0.78)', borderRadius: 5, padding: '3px 7px' }}>
                    {c.d}
                  </div>
                </div>
              );
            })}
          </div>
          {/* top fade so cards enter softly */}
          <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 40, background: 'linear-gradient(180deg, rgba(16,18,34,0.9), transparent)' }} />
        </div>
      </GlassPanel>
    </AbsoluteFill>
  );
};
