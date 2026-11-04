import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { timing, sample, totalDuration, textPlan, keyframes, emotionalSelector } from '../assets/text-motion/motion.mjs';
import { revealText } from '../assets/text-motion/web.mjs';
const near = (a,b,eps=1e-8) => assert.ok(Math.abs(a-b)<eps, `${a} != ${b}`);
const natural = {opacity:1,y:0,scaleY:1,rotation:0,blur:0};

test('one continuous clock across explicit wraps; preserve emoji, combining marks, whitespace', () => {
  const copy='Хочу 👩🏽‍🚀 кино.  \r\nС е\u0301лкой 👨‍👩‍👧‍👦!';
  const p=textPlan(copy);
  assert.equal(p.parts.map(x => x.break ?? x.units.map(u=>u.text).join('')).join(''),copy);
  const units=p.parts.flatMap(x=>x.units??[]);
  assert.deepEqual(units.map(u=>u.index),Array.from({length:p.unitCount},(_,i)=>i));
  assert.equal(units.filter(u=>u.text==='👩🏽‍🚀').length,1);
  assert.equal(units.filter(u=>u.text==='👨‍👩‍👧‍👦').length,1);
  assert.equal(units.filter(u=>u.text==='е\u0301').length,1);
  const wrap=p.parts.findIndex(x=>x.break);
  const before=p.parts[wrap-1].units.at(-1).index;
  const after=p.parts[wrap+1].units[0].index;
  assert.equal(after,before+1);
  const cfg=timing('emotional');
  near((cfg.firstDelay+after*cfg.stagger)-(cfg.firstDelay+before*cfg.stagger),.018);
});

test('Normal stays crisp, upright, monotonic and lands exactly', () => {
  let prev=0;
  for(let k=0;k<=300;k++){
    const p=sample('normal',.018+k/1000);
    assert.equal(p.blur,0); assert.equal(p.rotation,0); assert.equal(p.scaleY,1);
    assert.ok(p.opacity>=prev-1e-10);assert.ok(p.y>=0);
    prev=p.opacity;
  }
  assert.deepEqual(sample('normal',.318),natural);
  assert.ok(keyframes('normal').every(f=>!('filter'in f)));
});

test('Emotional preserves overshoot in motion while clamping material channels', () => {
  const elapsed=.018+.269*.300/.680;
  const p=sample('emotional',elapsed,0,{pixelsPerUnit:3});
  assert.ok(p.y<0);assert.ok(p.scaleY>1);assert.ok(p.rotation<0);
  assert.equal(p.opacity,1);assert.equal(p.blur,0);
  near(p.y,-6.2/3,.03);
  near(emotionalSelector(.180,.680),0);
  assert.deepEqual(sample('emotional',.318),natural);
  const initial=sample('emotional',0,0,{pixelsPerUnit:3});
  near(initial.y,32/3);near(initial.blur,10/3);near(initial.scaleY,.78);
});

test('same unit motion shifts only by stagger; total readiness and source clock stay distinct', () => {
  for(const style of ['normal','emotional']){
    const a=sample(style,.12,0),b=sample(style,.12+7*.018,7);
    for(const field of Object.keys(a))near(a[field],b[field]);
    near(totalDuration(61,style),1.398);assert.equal(totalDuration(0,style),0);
  }
  assert.equal(timing('normal',{preset:'source'}).duration,.5);
  assert.equal(timing('emotional',{preset:'source'}).duration,.68);
  assert.equal(timing('normal',{preset:'source'}).firstDelay,0);
  near(totalDuration(2,'emotional',{stagger:.03,duration:.4}),.46);
  assert.throws(()=>timing('emotional',{duration:0}));
  assert.throws(()=>sample('emotional',NaN));
  assert.throws(()=>timing('unknown'));
});

// Minimal DOM/WAAPI contract double: verifies lifecycle/data, not visual browser layout.
class Element {
  constructor(doc,type=1,text=''){this.ownerDocument=doc;this.nodeType=type;this.value=text;this.childNodes=[];this.style={};this.parentNode=null;}
  setAttribute(){}
  get textContent(){return this.nodeType===3?this.value:this.childNodes.map(c=>c.textContent).join('');}
  set textContent(v){this.replaceChildren(new Element(this.ownerDocument,3,v));}
  append(...nodes){for(const n of nodes){n.parentNode=this;this.childNodes.push(n);}}
  replaceChildren(...nodes){for(const n of this.childNodes)n.parentNode=null;this.childNodes=[];this.append(...nodes);}
  animate(frames,options){
    let done,fail;
    const a={frames,options,finished:new Promise((r,j)=>{done=r;fail=j;}),complete:()=>done(),cancel:()=>fail(new Error('cancelled'))};
    this.ownerDocument.animations.push(a);return a;
  }
}
const document=()=>({animations:[],createElement(name){const x=new Element(this);x.name=name;return x;}});

test('web completion restores original nodes; newlines add no delay slot and no double animation',async()=>{
  const doc=document(),host=new Element(doc);host.textContent='А👩‍🚀\nБ';const original=host.childNodes[0];
  const c=revealText(host,{style:'emotional'});
  assert.equal(doc.animations.length,3);
  doc.animations.forEach((a,i)=>near(a.options.delay,(i+1)*18));
  doc.animations.forEach(a=>a.complete());
  assert.deepEqual(await c.finished,{cancelled:false});
  assert.equal(host.childNodes[0],original);
  assert.equal(host.textContent,'А👩‍🚀\nБ');
});

test('web cancel/replacement never restores stale copy over an external app update',async()=>{
  const doc=document(),host=new Element(doc);host.textContent='Старое';
  const first=revealText(host);const second=revealText(host,{style:'emotional'});
  assert.deepEqual(await first.finished,{cancelled:true});
  host.textContent='Новое';second.cancel();
  assert.deepEqual(await second.finished,{cancelled:true});assert.equal(host.textContent,'Новое');
  const rich=new Element(doc);rich.append(doc.createElement('a'));
  assert.throws(()=>revealText(rich),/text-only/);
  const collapsed= document();
  collapsed.defaultView={getComputedStyle(){return {whiteSpace:'normal'};}};
  const multiline=new Element(collapsed);multiline.textContent='Two\nlines';
  assert.throws(()=>revealText(multiline),/Whitespace would change/);
  assert.equal(multiline.textContent,'Two\nlines');
});

test('Swift native core agrees with JS for both styles, clocks, delays and pixel units',t=>{
  if(process.platform!=='darwin'){t.skip('Apple Swift toolchain unavailable');return;}
  const compiler=spawnSync('xcrun',['--find','swiftc'],{encoding:'utf8'});
  if(compiler.status!==0){t.skip('Swift toolchain unavailable');return;}
  const dir=mkdtempSync(join(tmpdir(),'text-motion-parity-'));
  try{
    const main=join(dir,'main.swift'),binary=join(dir,'check');
    writeFileSync(main,`import Foundation
var output: [[String:Any]] = []
for style in [TextMotionStyle.normal, .emotional] {
 for preset in [TextMotionPreset.promo, .source] {
  let timing = TextMotionTiming(style: style, preset: preset, pixelsPerUnit: 3)
  for elapsed in [-1.0, 0, 0.018, 0.06, 0.09741176470588236, 0.1366764705882353, 0.318, 0.5, 0.7, 10] {
   for index in [0, 2, 7] {
    let p = TextMotion.sample(style: style, elapsed: elapsed, index: index, timing: timing)
    output.append(["style":style.rawValue,"preset":preset.rawValue,"elapsed":elapsed,"index":index,
      "opacity":p.opacity,"y":p.y,"scaleY":p.scaleY,"rotation":p.rotation,"blur":p.blur])
   }
  }
 }
}
print(String(data:try! JSONSerialization.data(withJSONObject:output), encoding:.utf8)!)
`);
    const core=resolve(dirname(fileURLToPath(import.meta.url)),'../assets/text-motion/TextMotion.swift');
    const sdk=spawnSync('xcrun',['--sdk','macosx','--show-sdk-path'],{encoding:'utf8'});
    assert.equal(sdk.status,0,sdk.stderr);
    const build=spawnSync('xcrun',['swiftc','-sdk',sdk.stdout.trim(),core,main,'-o',binary],{encoding:'utf8',timeout:30000});
    assert.equal(build.status,0,build.stderr);
    const run=spawnSync(binary,[],{encoding:'utf8',timeout:5000});assert.equal(run.status,0,run.stderr);
    const rows=JSON.parse(run.stdout);assert.equal(rows.length,120);
    for(const row of rows){
      const expected=sample(row.style,row.elapsed,row.index,{preset:row.preset,pixelsPerUnit:3});
      for(const key of Object.keys(natural))near(row[key],expected[key],1e-9);
    }
  }finally{rmSync(dir,{recursive:true,force:true});}
});
