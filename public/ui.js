export function renderUI(state,aff){
  const b=document.getElementById('badges');
  b.innerHTML=[badge(state.mode.toUpperCase()),state.badges?.uncertain?badge('不確実'):'',state.badges?.family_not_recommended?badge('家族非推奨'):'' ].join('');
  document.getElementById('tonight').innerHTML=`<h2>今夜の空</h2>
    <p>おすすめ度(OVS): <strong>${state.tonight.ovs}</strong> / 安全度: <strong>${state.tonight.safety}</strong></p>${rareBanner(state)}`;
  const unsafe=state.tonight.safety<3;
  if(!unsafe) renderPhotoCoach(state);
  renderQuests(state); renderBingo(); renderBundles(aff,unsafe); renderPostcard(state);
}
const badge=t=>`<span class="badge">${t}</span>`;
function rareBanner(s){const o=s.tonight.ovs, k=s.tonight.safety, th=s.thresholds||{}; const p=th.platinum?.ovs_min??90, ps=th.platinum?.safety_min??4;
  if(o>=p&&k>=ps) return '<div class="badge">PLATINUM NIGHT</div>';
  if(o>=85&&k>=3) return '<div class="badge">GOLD NIGHT</div>'; return '';
}
function renderPhotoCoach(s){document.getElementById('photo-coach').innerHTML=`<h2>ナイト・フォト・コーチ</h2>
<p>今夜の条件に基づく推奨：ISO 3200 / SS 8s / WB 3800K（例）。${s.tonight.moon_pct<5?'新月域で星が濃く見えます。':'月明かりに注意。'}</p>`;}
function renderQuests(s){document.getElementById('quests').innerHTML=`<h2>Sky Quests</h2><ul>
<li>夏の大三角を見つける</li>${s.tonight.iss?.visible?'<li>ISSを3分追尾</li>':''}</ul>`;}
function renderBingo(){document.getElementById('bingo').innerHTML=`<h2>Star Bingo</h2><p>流れ星/人工衛星を見つけたら1タップ記録（ダミー）。</p>`;}
function renderBundles(aff,unsafe){
  const wrap=document.getElementById('bundles'); if(unsafe){wrap.innerHTML='<h2>買い物導線</h2><p>安全度が低いため表示を停止中。</p>'; return;}
  const items=(aff.bundles||[]).filter(b=>b.ok).map(b=>`<li><strong>${b.title}</strong></li>`).join('');
  wrap.innerHTML=`<h2>買い物導線</h2><ul>${items||'<li>今夜に合うバンドルはありません。</li>'}</ul>`;
}
function renderPostcard(s){document.getElementById('postcard').innerHTML=`<h2>ご当地ポストカード</h2><p>星図と雲ヒートを端末内で合成（簡易表示）。</p>`;}
