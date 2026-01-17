import { useState } from 'react';
import SearchForm from './components/SearchForm';
import ReportView from './components/ReportView';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (hotelName, location) => {
    setLoading(true);
    setError(null);
    setReport(null);

    try {
      const response = await axios.post('http://localhost:5001/api/analyze', {
        hotel_name: hotelName,
        location: location || undefined
      });
      setReport(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || 'Failed to analyze. Please check the backend connection.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <header style={{ textAlign: 'center', marginBottom: '3rem', paddingTop: '2rem' }}>
        <h1 className="heading-gradient" style={{ fontSize: '3rem', margin: 0 }}>SafeStay AI</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1.2rem' }}>
          Advanced Hotel Safety Analysis using Google Gemini
        </p>
      </header>

      <main>
        <SearchForm onSearch={handleSearch} isLoading={loading} />

        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="card"
            style={{ maxWidth: '600px', margin: '2rem auto', borderColor: 'var(--danger)', color: 'var(--danger)', textAlign: 'center' }}
          >
            <h3>Analysis Failed</h3>
            <p>{error}</p>
          </motion.div>
        )}

        <AnimatePresence>
          {report && <ReportView report={report} />}
        </AnimatePresence>
      </main>

      <footer style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)', marginTop: '4rem' }}>
        <p>&copy; 2026 SafeStay AI. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
