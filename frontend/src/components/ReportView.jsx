import { motion } from 'framer-motion';
import { Shield, AlertTriangle, CheckCircle, MapPin, Star, Activity, Plus, Minus } from 'lucide-react';

const ReportView = ({ report }) => {
    if (!report) return null;

    const {
        hotel_info,
        safety_score,
        verdict,
        score_breakdown,
        infrastructure,
        ai_analysis,
        all_reviews
    } = report;

    const getScoreColor = (score) => {
        if (score >= 70) return 'var(--success)';
        if (score >= 40) return 'var(--warning)';
        return 'var(--danger)';
    };

    const scoreColor = getScoreColor(safety_score);

    // Parse verdict for badge
    let badgeClass = 'badge-moderate';
    if (verdict.toUpperCase().includes('SAFE')) badgeClass = 'badge-safe';
    if (verdict.toUpperCase().includes('UNSAFE')) badgeClass = 'badge-unsafe';

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col gap-4 mt-8"
            style={{ width: '100%', maxWidth: '900px', margin: '2rem auto' }}
        >
            {/* Header Info */}
            <div className="card">
                <div className="flex justify-between items-center" style={{ flexWrap: 'wrap', gap: '1rem' }}>
                    <div>
                        <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem' }} className="heading-gradient">
                            {hotel_info.name}
                        </h1>
                        <div className="flex items-center gap-2" style={{ color: 'var(--text-secondary)' }}>
                            <MapPin size={16} />
                            <span>{hotel_info.address}</span>
                        </div>
                        <div className="flex items-center gap-2 mt-4">
                            <span className="badge" style={{ backgroundColor: 'rgba(255,255,255,0.1)' }}>
                                ⭐ {hotel_info.rating} / 5
                            </span>
                            <span className="badge" style={{ backgroundColor: 'rgba(255,255,255,0.1)' }}>
                                💬 {hotel_info.total_reviews} Reviews
                            </span>
                        </div>
                    </div>

                    <div className="text-center">
                        <div className="score-circle" style={{ borderColor: scoreColor }}>
                            <span className="score-value" style={{ color: scoreColor }}>
                                {safety_score}
                            </span>
                            <span className="score-label">Safety Score</span>
                        </div>
                        <div className={`badge ${badgeClass} mt-4 inline-block`}>
                            {verdict}
                        </div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
                {/* Score Breakdown */}
                <div className="card">
                    <h3 className="flex items-center gap-2 mb-4" style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                        <Activity size={20} className="text-blue-500" />
                        Score Breakdown
                    </h3>
                    <div className="flex flex-col gap-2">
                        <div className="flex justify-between">
                            <span style={{ color: 'var(--text-secondary)' }}>Base Score</span>
                            <span>{score_breakdown.base_score}</span>
                        </div>
                        <div className="flex justify-between">
                            <span style={{ color: 'var(--text-secondary)' }}>Rating Bonus</span>
                            <span className="text-green-400">+{score_breakdown.rating_bonus}</span>
                        </div>
                        <div className="flex justify-between">
                            <span style={{ color: 'var(--text-secondary)' }}>Infrastructure Bonus</span>
                            <span className="text-green-400">+{score_breakdown.infrastructure_bonus}</span>
                        </div>
                        <div className="flex justify-between">
                            <span style={{ color: 'var(--text-secondary)' }}>Negative Review Penalty</span>
                            <span className="text-red-400">-{score_breakdown.negative_penalty}</span>
                        </div>
                    </div>
                </div>

                {/* Infrastructure */}
                <div className="card">
                    <h3 className="flex items-center gap-2 mb-4" style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                        <MapPin size={20} className="text-purple-500" />
                        Infrastructure (Nearby)
                    </h3>
                    <div className="flex flex-col gap-2">
                        <div className="flex justify-between">
                            <span style={{ color: 'var(--text-secondary)' }}>Police Stations</span>
                            <span>{infrastructure.police_stations}</span>
                        </div>
                        <div className="flex justify-between">
                            <span style={{ color: 'var(--text-secondary)' }}>Hospitals</span>
                            <span>{infrastructure.hospitals}</span>
                        </div>
                        <div className="flex justify-between">
                            <span style={{ color: 'var(--text-secondary)' }}>Street Lights (sampled)</span>
                            <span>{infrastructure.street_lights}</span>
                        </div>
                        <div className="flex justify-between">
                            <span style={{ color: 'var(--text-secondary)' }}>Roads Nearby</span>
                            <span>{infrastructure.roads_nearby}</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* AI Analysis */}
            <div className="card">
                <h3 className="flex items-center gap-2 mb-4" style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                    <Shield size={20} className="text-green-500" />
                    AI Safety Assessment
                </h3>

                {ai_analysis.error ? (
                    <div style={{ color: 'var(--danger)' }}>
                        <p><strong>Note:</strong> AI Analysis unavailable ({ai_analysis.error})</p>
                    </div>
                ) : (
                    <div>
                        <div className="mb-4">
                            <p style={{ fontSize: '1.2rem', fontWeight: 600 }}>
                                Assessment: <span style={{ color: ai_analysis.assessment === 'Safe' ? 'var(--success)' : 'var(--warning)' }}>{ai_analysis.assessment}</span>
                            </p>
                            <p style={{ color: 'var(--text-secondary)' }}>Confidence: {ai_analysis.confidence_score}%</p>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div style={{ backgroundColor: 'rgba(16, 185, 129, 0.1)', padding: '1rem', borderRadius: '8px' }}>
                                <h4 className="flex items-center gap-2 text-green-400 mb-2"><CheckCircle size={16} /> Positives</h4>
                                <ul style={{ paddingLeft: '1.5rem', margin: 0 }}>
                                    {ai_analysis.positives.map((item, i) => <li key={i}>{item}</li>)}
                                </ul>
                            </div>
                            <div style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', padding: '1rem', borderRadius: '8px' }}>
                                <h4 className="flex items-center gap-2 text-red-400 mb-2"><AlertTriangle size={16} /> Concerns</h4>
                                <ul style={{ paddingLeft: '1.5rem', margin: 0 }}>
                                    {ai_analysis.concerns.map((item, i) => <li key={i}>{item}</li>)}
                                </ul>
                            </div>
                        </div>

                        {ai_analysis.recommendations && (
                            <div className="mt-4">
                                <h4 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem' }}>Recommendations</h4>
                                <ul style={{ paddingLeft: '1.5rem', color: 'var(--text-secondary)' }}>
                                    {ai_analysis.recommendations.map((rec, i) => <li key={i}>{rec}</li>)}
                                </ul>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Reviews Sample */}
            {all_reviews && all_reviews.length > 0 && (
                <div className="card">
                    <h3 className="flex items-center gap-2 mb-4" style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                        <Star size={20} className="text-yellow-500" />
                        Recent Reviews Analysis
                    </h3>
                    <div className="flex flex-col gap-4" style={{ maxHeight: '800px', overflowY: 'auto' }}>
                        {all_reviews.map((rev, i) => (
                            <div key={i} style={{ backgroundColor: 'var(--bg-secondary)', padding: '1rem', borderRadius: '8px' }}>
                                <div className="flex justify-between items-center mb-2">
                                    <span className="badge" style={{
                                        backgroundColor: rev.source === 'Google Maps' ? 'rgba(66, 133, 244, 0.2)' :
                                            rev.source === 'Twitter/X' ? 'rgba(29, 161, 242, 0.2)' :
                                                'rgba(255, 87, 34, 0.2)',
                                        color: rev.source === 'Google Maps' ? '#4285f4' :
                                            rev.source === 'Twitter/X' ? '#1da1f2' :
                                                '#ff5722'
                                    }}>{rev.source}</span>
                                    {rev.rating && <span style={{ color: '#ffd700' }}>⭐ {rev.rating}</span>}
                                </div>
                                <p style={{ fontStyle: 'italic', color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: '1.5' }}>
                                    "{rev.text.length > 400 ? rev.text.substring(0, 400) + '...' : rev.text}"
                                </p>
                                {rev.link && (
                                    <a href={rev.link} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--accent-primary)', fontSize: '0.8rem', display: 'block', marginTop: '0.5rem' }}>
                                        View Source →
                                    </a>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

        </motion.div>
    );
};

export default ReportView;
