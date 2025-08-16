// public/ui.js

/** メインエントリ：各カードを描画 */
export function renderUI(state, aff) {
  renderTonight(state);
  renderQuests(state);
  renderBingo();
  renderPhotoCoach(state);
  renderBundles(aff);         // ← ★買い物導線（リンク表示）
  renderPostcard();
}

/* ---------- 以下、各セクション描画 ---------- */

function renderTonight(state) {
  const box = byId('tonight');
  if (!box) return;
  const t = state?.tonight || {};
  const ovs = num(t.ovs, 0);
  const safety = num(t.safety, 0);

  const level =
    ovs >= (state?.thresholds?.platinum?.ovs_min ?? 90) ? 'PLATINUM NIGHT' :
    ovs >= (state?.thresholds?.gold?.ovs_min ?? 85)      ? 'GOLD NIGHT' :
                                                            'NORMAL';

  box.innerHTML = `
    <h2>今夜の空</h2>
    <p>おすすめ度(OVS): <strong>${ovs}</strong> / 安全度: <strong>${safety}</strong></p>
    <button class="badge">${level}</button>
  `;
}

function renderQuests(state) {
  const box = byId('quests');
  if (!box) return;
  box.innerHTML = `
    <h2>Sky Quests</h2>
    <ul>
      <li>夏の大三角を見つける</li>
      <li>${state?.tonight?.iss?.visible ? 'ISSを3分追尾' : '人工衛星を1つ見つける'}</li>
    </ul>
  `;
}

function renderBingo() {
  const box = byId('bingo');
  if (!box) return;
  box.innerHTML = `
    <h2>Star Bingo</h2>
    <p>流れ星/人工衛星を見つけたら1タップ記録（ダミー）。</p>
  `;
}

function renderPhotoCoach(state) {
  const box = byId('photo-coach');
  if (!box) return;
  // 簡易レコメンド（ダミー）
  box.innerHTML = `
    <h2>ナイト・フォト・コーチ</h2>
    <p>今夜の条件に基づく推奨：ISO 3200 / SS 8s / WB 3800K（例）。新月域で星が濃く見えます。</p>
  `;
}

/**
 * ★買い物導線：affiliates.json の bundles を「リンク付き」で描画
 * - b.url があればそれを使用
 * - 無ければ catalog の最初の item の URL
 * - どちらも無ければ Amazon 検索にフォールバック
 */
function renderBundles(aff) {
  const box = byId('bundles');
  if (!box) return;

  const bundles = Array.isArray(aff?.bundles) ? aff.bundles : [];
  const catalog = aff?.catalog || {};

  box.innerHTML = `
    <h2>買い物導線</h2>
    <ul id="bundle-list" style="padding-left:1.2em; margin:0.4em 0;"></ul>
  `;

  const ul = byId('bundle-list');
  if (!bundles.length) {
    ul.innerHTML = `<li>（準備中）</li>`;
    return;
  }

  bundles.forEach(b => {
    const li = document.createElement('li');
    const a  = document.createElement('a');

    const title = b.title || b.id;
    const firstItem = (b.items && b.items[0]) || '';
    const urlFromCatalog = catalog[firstItem]?.url;
    const fallbackSearch  = `https://www.amazon.co.jp/s?k=${encodeURIComponent(title)}`;

    a.textContent = title;
    a.href = b.url || urlFromCatalog || fallbackSearch;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';

    li.appendChild(a);
    ul.appendChild(li);
  });
}

function renderPostcard() {
  const box = byId('postcard');
  if (!box) return;
  box.innerHTML = `
    <h2>ご当地ポストカード</h2>
    <p>星図と雲ヒートを端末内で合成（簡易表示）。</p>
  `;
}

/* ---------- 小物ユーティリティ ---------- */
function byId(id) { return document.getElementById(id); }
function num(v, d=0) { const n = Number(v); return Number.isFinite(n) ? n : d; }
