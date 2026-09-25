import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");

  const searchMedicines = async () => {
    if (!query.trim()) {
      setResults([]);
      setSearched(false);
      setError("");
      return;
    }

    setLoading(true);
    setSearched(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/search?q=${encodeURIComponent(query)}`
      );

      if (!response.ok) {
        throw new Error("Backend request failed");
      }

      const data = await response.json();
      setResults(data.results || []);
    } catch (err) {
      console.error(err);
      setError(
        "Could not connect to the backend. Make sure FastAPI is running on port 8000."
      );
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      searchMedicines();
    }
  };

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <p className="tag">💊 MEDICINE PRICE COMPARISON</p>

          <h1>
            Find Medicine.
            <br />
            Compare Prices.
          </h1>

          <p className="subtitle">
            Search medicines and compare prices across different pharmacies.
          </p>

          <div className="search-box">
            <input
              type="text"
              placeholder="Enter medicine name..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
            />

            <button onClick={searchMedicines}>
              🔍 Search
            </button>
          </div>
        </div>
      </header>

      <main className="container">
        {loading && (
          <div className="message">
            🔄 Searching medicines...
          </div>
        )}

        {error && (
          <div className="error">
            ⚠️ {error}
          </div>
        )}

        {!loading && !error && searched && results.length === 0 && (
          <div className="message">
            😕 No medicine found for "{query}"
          </div>
        )}

        {!loading && results.length > 0 && (
          <section>
            <div className="results-header">
              <h2>Search Results</h2>
              <span>{results.length} result(s)</span>
            </div>

            <div className="medicine-list">
              {results.map((medicine, index) => (
                <div className="medicine-card" key={index}>
                  <div className="medicine-top">
                    <div>
                      <h3>{medicine.medicine_name}</h3>

                      <p className="dosage">
                        💊 {medicine.dosage_form_strength}
                      </p>
                    </div>

                    <div className="unit">
                      {medicine.unit}
                    </div>
                  </div>

                  <div className="price-info">
                    <div>
                      <span>NPPA Ceiling Price</span>
                      <strong>
                        ₹{Number(medicine.nppa_ceiling_price).toFixed(2)}
                      </strong>
                    </div>

                    <div>
                      <span>Pharmacy Price</span>
                      <strong>
                        ₹{Number(medicine.price).toFixed(2)}
                      </strong>
                    </div>

                    <div>
                      <span>Discount</span>
                      <strong className="discount">
                        {Number(medicine.discount_pct).toFixed(1)}%
                      </strong>
                    </div>
                  </div>

                  <div className="pharmacy">
                    <div>
                      <span className="label">🏪 Pharmacy</span>
                      <strong>{medicine.pharmacy_name}</strong>
                    </div>

                    <div className="location">
                      📍 {medicine.latitude}, {medicine.longitude}
                    </div>
                  </div>

                  <div className="synthetic">
                    Synthetic demo price — not a real-time pharmacy price
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;