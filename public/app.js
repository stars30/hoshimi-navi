import { renderUI } from './ui.js';
if('serviceWorker' in navigator) navigator.serviceWorker.register('/worker.js');

const stateUrl='/data/site_state.json', affUrl='/data/affiliates.json';

async function loadJSON(u){const r=await fetch(u,{cache:'no-store'});if(!r.ok)throw new Error('fetch failed:'+u);return r.json();}

(async()=>{
  try{
    const [state,aff]=await Promise.all([loadJSON(stateUrl),loadJSON(affUrl)]);
    renderUI(state,aff);
    document.getElementById('lastmod').textContent=new Date(state.lastmod).toLocaleString();
    initSpeedGuard(state);
  }catch(e){
    console.error(e);
    document.querySelector('main').innerHTML='<div class="card">データ読み込みに失敗。オフラインの可能性があります。</div>';
  }
})();

function initSpeedGuard(state){
  const car=document.getElementById('car-window');
  const mainSections=[...document.querySelectorAll('main .card')].filter(el=>el.id!=='car-window');
  const setDriving=(on)=>{car.classList.toggle('hidden',!on);mainSections.forEach(el=>el.style.display=on?'none':'');};
  if(navigator.geolocation){
    navigator.geolocation.watchPosition(
      p=>{const v=p.coords.speed; if(typeof v==='number'&&v>0.5)setDriving(true); else setDriving(false);},
      _=>setDriving(false),{enableHighAccuracy:true,maximumAge:5000,timeout:10000}
    );
  }
  document.getElementById('btn-tts')?.addEventListener('click',()=>{
    const s=new SpeechSynthesisUtterance(makeTTS(state)); s.lang='ja-JP'; speechSynthesis.speak(s);
  });
}
function makeTTS(state){const t=state.tonight; return `本日の観測おすすめ度は${t.ovs}点。安全度は${t.safety}です。${t.iss?.visible?'このあとISSが見えます。':''}`;}
