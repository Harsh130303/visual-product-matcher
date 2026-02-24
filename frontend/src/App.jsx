import React, { useState, useEffect } from 'react';
import './index.css';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

function App() {
  const [products, setProducts] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [imageUrl, setImageUrl] = useState('');
  const [preview, setPreview] = useState(null);
  const [similarityThreshold, setSimilarityThreshold] = useState(0.5);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const res = await fetch(`${API_BASE}/products`);
      const data = await res.json();
      setProducts(data);
    } catch (err) {
      console.error('Failed to fetch products', err);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPreview(URL.createObjectURL(file));
      handleSearch(file);
    }
  };

  const handleUrlSearch = () => {
    if (imageUrl) {
      setPreview(imageUrl);
      handleSearch(null, imageUrl);
    }
  };

  const handleSearch = async (file, url) => {
    setLoading(true);
    setError(null);
    setSearchResults([]);

    const formData = new FormData();
    if (file) formData.append('file', file);
    if (url) formData.append('image_url', url);

    try {
      const res = await fetch(`${API_BASE}/search`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error('Search failed');

      const data = await res.json();
      setSearchResults(data.results);
    } catch (err) {
      setError('Failed to find similar products. Please check the image and try again.');
    } finally {
      setLoading(false);
    }
  };

  const filteredResults = searchResults.filter(r => r.similarity >= similarityThreshold);
  const displayProducts = searchResults.length > 0 ? filteredResults : products;

  return (
    <div className="container">
      <header>
        <h1>Visual Product Matcher</h1>
        <p>Find visually similar products from our curated catalog</p>
      </header>

      <div className="search-section">
        <div className="input-group">
          <div className="upload-area" onClick={() => document.getElementById('fileInput').click()}>
            <p>📸 Click to upload product image</p>
            <input
              id="fileInput"
              type="file"
              hidden
              accept="image/*"
              onChange={handleFileUpload}
            />
          </div>

          <div className="url-input-container">
            <input
              type="text"
              placeholder="Or paste image URL..."
              value={imageUrl}
              onChange={(e) => setImageUrl(e.target.value)}
            />
            <button onClick={handleUrlSearch}>Search</button>
          </div>
        </div>

        {preview && (
          <div className="preview-container">
            <p className="preview-label">Comparing against:</p>
            <img src={preview} alt="Preview" className="preview-image" />
          </div>
        )}

        {searchResults.length > 0 && (
          <div className="filter-section">
            <label className="filter-label">
              Similarity Threshold: {(similarityThreshold * 100).toFixed(0)}%
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={similarityThreshold}
              onChange={(e) => setSimilarityThreshold(parseFloat(e.target.value))}
              style={{ width: '100%' }}
            />
          </div>
        )}
      </div>

      {loading && (
        <div className="loader">
          <div className="spinner"></div>
        </div>
      )}

      {error && <p className="error-message">{error}</p>}

      <div className="results-grid">
        {displayProducts.map((product) => (
          <div key={product.id} className="product-card">
            <img src={product.image_url} alt={product.name} className="product-image" />
            <div className="product-info">
              <div className="product-name">{product.name}</div>
              <div className="product-category">{product.category}</div>
              {product.similarity !== undefined && (
                <div className="similarity-badge">
                  {(product.similarity * 100).toFixed(1)}% Match
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
