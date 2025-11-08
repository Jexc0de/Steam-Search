import { useState } from 'react';
import styles from './MainPage.module.css';

export default function MainPage() {
  const [maxResults, setMaxResults] = useState(50);
  const [results, setResults] = useState([]);
  const [trieTime, setTrieTime] = useState(null);
  const [heapTime, setHeapTime] = useState(null);
  const [query, setQuery] = useState('');
  const [attribute, setAttribute] = useState('');

  async function handleTrieSearch() {
    if (!query.trim()) return;
    const res = await fetch(`http://127.0.0.1:5000/search/trie?q=${encodeURIComponent(query)}&limit=${maxResults}`);
    const data = await res.json();
    setTrieTime(data.time_ms);
    setResults(data.results || []);
  }

  async function handleHeapSearch() {
    if (!attribute) return;
    const res = await fetch(`http://127.0.0.1:5000/search/heap?sort_by=${attribute}&limit=${maxResults}`);
    const data = await res.json();
    setHeapTime(data.time_ms);
    setResults(data.results || []);
  }

  return (
    
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>Game Recommendation Engine</h1>
        <div className={styles.timeStats}>
          <div>Trie Search: {trieTime ? `${trieTime} ms` : '—'}</div>
          <div>Heap Search: {heapTime ? `${heapTime} ms` : '—'}</div>
        </div>
      </header>

      <main className={styles.main}>
        <section className={styles.searchSection}>
          <h2 className={styles.sectionTitle}>Search by Name</h2>
          <div className={styles.searchBar}>
            <input
              type="text"
              placeholder="Enter game name..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button onClick={handleTrieSearch}>🔍</button>
          </div>

      <div className={styles.maxResults}>
        <label>Max Results:</label>
          <input
            type="number"
            min="1"
            max="10000"
            value={maxResults}
            onChange={(e) => setMaxResults(e.target.value)}
          />
      </div>

          <h2 className={styles.sectionTitle}>Sort by Attribute</h2>
          <div className={styles.attributeMenu}>
            <select value={attribute} onChange={(e) => setAttribute(e.target.value)}>
              <option value="">Select Attribute</option>
              <option value="review_high">Highest Review %</option>
              <option value="review_low">Lowest Review %</option>
              <option value="price_high">Highest Price</option>
              <option value="price_low">Lowest Price</option>
            </select>
            <button onClick={handleHeapSearch}>Compare</button>
          </div>
        </section>

        <section className={styles.resultsSection}>
          <div className={styles.recHeader}>
            <h2>Search Results</h2>
          </div>

          <div className={styles.grid}>
  {results.length > 0 ? (
    results.map((r, i) => (
      
      <div key={i} className={styles.card}>
        <div className={styles.cardImage}>
          {r.appid ? (
            <img
              src={r.header}
              alt={r.name}
              style={{ width: '100%', borderRadius: '4px' }}
              onError={(e) => (e.target.style.display = 'none')}
            />
          ) : (
            <span>[Picture]</span>
          )}
        </div>

        <div className={styles.cardText}>
          <strong>{r.name || '[Title]'}</strong>
          
          {r.price !== undefined && r.price !== null && !isNaN(r.price) &&(
            <div>Price: ${Number(r.price).toFixed(2)}</div>
          )}
          {r.review_percent !== undefined && (
            <div>Review: {r.review_percent ?? "No score"}{r.review_percent != null && "%"}</div>
          )}
        </div>
      </div>
    ))
  ) : (
    <p
      style={{
        gridColumn: '1 / -1',
        textAlign: 'center',
        color: '#979797ff',
      }}
    >
      No results found
    </p>
  )}
</div>

        </section>
      </main>
    </div>
  );
}
