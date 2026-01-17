import { useState } from 'react';
import { Search } from 'lucide-react';
import { motion } from 'framer-motion';

const SearchForm = ({ onSearch, isLoading }) => {
    const [hotelName, setHotelName] = useState('');
    const [location, setLocation] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (hotelName.trim()) {
            onSearch(hotelName, location);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card"
            style={{ maxWidth: '600px', margin: '0 auto', padding: '2.5rem' }}
        >
            <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem', textAlign: 'center' }}>
                Analyze Hotel Safety
            </h2>
            <form onSubmit={handleSubmit} className="flex flex-col" style={{ gap: '1.5rem' }}>
                <div>
                    <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>
                        Hotel Name
                    </label>
                    <input
                        type="text"
                        className="input-field"
                        placeholder="e.g. Radisson Kharadi"
                        value={hotelName}
                        onChange={(e) => setHotelName(e.target.value)}
                        required
                    />
                </div>

                <div style={{ marginTop: '0.5rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>
                        Location Bias (Optional)
                    </label>
                    <input
                        type="text"
                        className="input-field"
                        placeholder="e.g. Pune, India"
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                    />
                </div>

                <button
                    type="submit"
                    className="btn justify-center mt-4"
                    disabled={isLoading || !hotelName.trim()}
                    style={{ width: '100%' }}
                >
                    {isLoading ? (
                        <>
                            <div className="loading-spinner"></div>
                            Analyzing...
                        </>
                    ) : (
                        <>
                            <Search size={20} />
                            Start Safety Analysis
                        </>
                    )}
                </button>
            </form>
        </motion.div>
    );
};

export default SearchForm;
